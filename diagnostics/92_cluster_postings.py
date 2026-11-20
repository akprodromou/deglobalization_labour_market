"""
Month 4, step 3: cluster the postings of ONE board into occupation clusters (runs on Colab; the Mac has no torch).

Two inputs are clustered and compared:
  A  the cleaned job title (multilingual-e5; title-less postings use the first 150 characters of the description)
  D  the same title embedding + the ESCO skill vector of the FULL text (script 69b, local extractor, threshold 0.6)
     + the pruned Lightcast phrase block (script 91, only terms with selected=1 in lexicon/lightcast_block_terms.csv).
     Skills and Lightcast terms are tf-idf weighted and reduced with TruncatedSVD; every block is L2-normalised, so
     the title keeps weight 1, ESCO skills --w-skills (0.5) and Lightcast terms --w-lc (0.3).
     v2/v3: before weighting, every skill/term passes a filter. v1 (no filter) clustered on extractor false positives
     and generic skills ("sell bicycles" on postmen, "assume responsibility"). The filter is now the LAPLACIAN SCORE
     (He, Cai and Niyogi 2005; --filter ls): an item is kept when the postings that carry it are neighbours on a
     k-nearest-neighbour graph of the title embeddings. The own coherence filter of the first runs is still available
     (--filter coherence). v3 also drops very common ESCO skills first (--max-df tukey, see script 125).
Method for both: UMAP (10 dimensions, cosine, min_dist 0) -> HDBSCAN (McInnes et al.), all postings of the board,
the Month 3 tags are NOT used here (they are joined afterwards by script 93).
Ablation and checks:
  * k-means with the same k as HDBSCAN found, on the same UMAP space: agreement (AMI) on the non-noise postings
  * stability: the whole UMAP + HDBSCAN is repeated with --seeds 3 seeds; ARI between seeds on postings clustered in both
  * HDBSCAN relative validity and noise share (compare A against D)
  * named emerging occupations: regex on the cleaned title (English, Swedish, German, French); reported, never forced

Outputs (--out, default data/cluster):
  labels_<board>_<A|D>.jsonl     {"id","day","cluster","prob"}   cluster -1 = noise
  metrics_<board>_<A|D>.json
  clusters_<board>_<A|D>.md      the largest clusters with their most central titles, ESCO skills, Lightcast terms,
                                 and the named-occupation table
Run:  python -m diagnostics.92_cluster_postings --board jobbland --input A D
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

NAMED = {
    "trade compliance officer": r"trade compliance|customs compliance|sanctions? compliance|compliance officer.*(trade|export|customs)|"
                                r"handelskompliance|tullkompliance|zoll.{0,12}compliance|conformit\w+ (douan|export)",
    "export control specialist": r"export[- ]?control|exportkontroll|exportkontrolle|ausfuhrkontroll|contr[oô]le des exportations|\bdual[- ]use\b",
    "supply chain resilience analyst": r"supply[- ]chain.{0,20}(risk|resilien)|resilien.{0,20}supply|leveranskedje.{0,20}(risk|resilien)",
    "semiconductor process engineer": r"(semiconductor|halvledar|halbleiter|semi-?conducteur|wafer|cleanroom).{0,40}(process|engineer|ingenj|ingenieur|ing[eé]nieur)|"
                                      r"(process|engineer|ingenj|ingenieur|ing[eé]nieur).{0,40}(semiconductor|halvledar|halbleiter|semi-?conducteur|wafer)",
    "battery cell technician": r"^(?!.*\b(?:solar|solcell\w*|solceller)\b).*(?:(batter|akku|accumulateur).{0,30}(cell|zell|technician|tekniker|techniker|technicien|operat|process)|"
                               r"(cell|zell|technician|tekniker|techniker|technicien|operator).{0,30}(batter|akku|accumulateur))",
    "critical materials specialist": r"critical (raw )?material|kritiska (råvaror|material)|kritische rohstoffe|rare earth|sällsynta jordartsmetaller|"
                                     r"mati[eè]res? (premi[eè]res? )?critiques",
    "reshoring program manager": r"reshoring|onshoring|nearshoring|supply chain locali[sz]ation|re-?industriali[sz]|relocali[sz]ation",
}
NAMED_RX = {k: re.compile(v, re.I) for k, v in NAMED.items()}


# ---------------------------------------------------------------- loading
def load_jsonl(p):
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def text_a(r):
    t = (r.get("title_clean") or "").strip() if r.get("has_title") else ""
    return t or (r.get("desc_start") or "").strip() or "unknown"


def embed_titles(texts, model_name, cache, mock=False, batch=256):
    if cache and Path(cache).exists():
        e = np.load(cache)
        if len(e) == len(texts):
            print(f"  embeddings loaded from {cache}")
            return e
    if mock:
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer
        x = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4), min_df=2).fit_transform(texts)
        e = TruncatedSVD(min(64, x.shape[1] - 1), random_state=0).fit_transform(x)
    else:
        from sentence_transformers import SentenceTransformer
        m = SentenceTransformer(model_name, device="cuda")
        m.half()
        e = m.encode(["query: " + t for t in texts], batch_size=batch, normalize_embeddings=True, show_progress_bar=True)
    e = e / np.maximum(np.linalg.norm(e, axis=1, keepdims=True), 1e-9)
    e = e.astype("float32")
    if cache:
        Path(cache).parent.mkdir(parents=True, exist_ok=True)
        np.save(cache, e)
    return e


def coherence_filter(docs, e, min_n, min_lift, seed=0):
    """Keep a skill/term only if the postings that carry it have title embeddings that agree with each other more
    than a random set of the same size does. This removes (a) extractor false positives ("sell bicycles" on postmen,
    "feed concrete mixer" on IT consultants) and (b) generic skills ("assume responsibility") that carry no occupation
    signal. coherence = length of the mean title embedding of the posting set (1 = identical titles); lift = coherence
    minus the same number for 5 random sets of equal size."""
    rng = np.random.default_rng(seed)
    # e5 embeddings are anisotropic (any two titles have cosine ~0.8), so a mean vector is long for ANY set and every
    # item looked coherent (v2 first run: all lifts 0.00-0.04). Centre on the board mean and re-normalise first.
    e = e - e.mean(axis=0, keepdims=True)
    e = e / np.maximum(np.linalg.norm(e, axis=1, keepdims=True), 1e-9)
    where = defaultdict(list)
    for i, d in enumerate(docs):
        for t in set(d):
            where[t].append(i)
    n_all = len(docs)
    stats = {}
    base_cache = {}
    for t, idx in where.items():
        n = len(idx)
        if n < min_n:
            continue
        coh = float(np.linalg.norm(e[idx].mean(axis=0)))
        key = min(n, 2000) // 5 * 5
        if key not in base_cache:
            k = max(key, 5)
            base_cache[key] = float(np.mean([np.linalg.norm(e[rng.choice(n_all, k, replace=False)].mean(axis=0)) for _ in range(5)]))
        stats[t] = (n, coh, coh - base_cache[key])
    keep = {t for t, (n, c, l) in stats.items() if l >= min_lift}
    return keep, stats


def coherence_report(name, stats, keep, labels):
    top = sorted(stats.items(), key=lambda kv: -kv[1][0])[:40]
    md = [f"### {name}: {len(stats):,} items with enough postings, {len(keep):,} kept (lift >= threshold), {len(stats) - len(keep):,} dropped", "",
          "| item | postings | coherence | lift | decision |", "|---|---|---|---|---|"]
    for t, (n, c, l) in top:
        md.append(f"| {labels.get(t, t)[:50]} | {n:,} | {c:.2f} | {l:+.2f} | {'kept' if t in keep else 'DROPPED'} |")
    return "\n".join(md) + "\n"


def knn_graph(e, k=5, chunk=2048):
    """Nearest-neighbour graph of the postings for the Laplacian Score (He, Cai and Niyogi 2005).
    An edge joins i and j if i is among the k nearest neighbours of j or j among those of i (title embedding, cosine).
    Weights S_ij = exp(-||x_i - x_j||^2 / t); ||x_i - x_j||^2 = 2 - 2 cos for unit vectors; t = mean squared distance
    over the edges between postings whose titles differ (the paper leaves t as 'a suitable constant')."""
    import scipy.sparse as sp
    n = len(e)
    idx = np.zeros((n, k), dtype=np.int64)
    d2 = np.zeros((n, k), dtype=np.float64)
    try:
        import torch
        dev = "cuda" if torch.cuda.is_available() else "cpu"
        E = torch.from_numpy(np.ascontiguousarray(e, dtype=np.float32)).to(dev)
        for s in range(0, n, chunk):
            sim = E[s:s + chunk] @ E.T
            rows = torch.arange(sim.shape[0], device=dev)
            sim[rows, rows + s] = -3.0  # no self edge
            v, i = sim.topk(k, dim=1)
            idx[s:s + chunk] = i.cpu().numpy()
            d2[s:s + chunk] = (2.0 - 2.0 * v.double()).clamp(min=0).cpu().numpy()
    except ImportError:
        from sklearn.neighbors import NearestNeighbors
        nn = NearestNeighbors(n_neighbors=k + 1, metric="cosine", algorithm="brute", n_jobs=-1).fit(e)
        dist, ia = nn.kneighbors(e)
        mask = ia != np.arange(n)[:, None]
        mask[mask.all(axis=1), -1] = False  # self not among the neighbours (duplicate titles): drop the farthest
        idx = ia[mask].reshape(n, k)
        d2 = 2.0 * dist[mask].reshape(n, k)
    pos = d2[d2 > 1e-6]  # many postings have an identical title (distance 0): they must not pull t towards 0
    t = float(pos.mean()) if pos.size else 1.0
    w = np.exp(-d2 / t)
    S = sp.csr_matrix((w.ravel(), (np.repeat(np.arange(n), k), idx.ravel())), shape=(n, n))
    S = S.maximum(S.T).tocsr()  # 'i in kNN(j) or j in kNN(i)'; the weight depends only on the distance, so it is symmetric
    d = np.asarray(S.sum(axis=1)).ravel()
    return {"S": S, "d": d, "t": t, "k": k}


def laplacian_scores(graph, docs, items):
    """Laplacian Score of every item (equation 1 of the paper). The feature of an item is 1 in the postings that carry
    it and 0 elsewhere. L = f~' L f~ / f~' D f~ with f~ = f - (f'D1 / 1'D1) 1; a LOW score means the item respects the
    graph (its postings are neighbours). For a 0/1 feature: f'Df = f'd and f'Sf is a sum over the edges."""
    import scipy.sparse as sp
    S, d = graph["S"], graph["d"]
    col = {t: j for j, t in enumerate(items)}
    r, c = [], []
    for i, x in enumerate(docs):
        for t in set(x):
            j = col.get(t)
            if j is not None:
                r.append(i)
                c.append(j)
    F = sp.csr_matrix((np.ones(len(r)), (r, c)), shape=(len(docs), len(items)))
    fd = np.asarray(F.T @ d).ravel()
    fSf = np.asarray(F.multiply(S @ F).sum(axis=0)).ravel()
    dtot = float(d.sum())
    num = fd - fSf
    den = fd - fd ** 2 / dtot
    return np.where(den > 1e-12, num / np.where(den > 1e-12, den, 1.0), np.nan)


def laplacian_filter(docs, graph, min_n, ls_max):
    """Keep an item (ESCO skill or Lightcast term) if it has at least min_n postings and a Laplacian Score below ls_max."""
    cnt = Counter(t for x in docs for t in set(x))
    items = [t for t, c in cnt.items() if c >= min_n]
    if not items:
        return set(), {}
    L = laplacian_scores(graph, docs, items)
    stats = {t: (cnt[t], float(L[j])) for j, t in enumerate(items) if not np.isnan(L[j])}
    keep = {t for t, (n, s) in stats.items() if s < ls_max}
    return keep, stats


def laplacian_report(name, stats, keep, labels, docs, ls_max):
    sc = np.array([v[1] for v in stats.values()]) if stats else np.array([0.0])
    md = [f"### {name}: {len(stats):,} items scored, {len(keep):,} kept (score below {ls_max}), {len(stats) - len(keep):,} dropped", "",
          f"Score: minimum {sc.min():.3f}, median {np.median(sc):.3f}, maximum {sc.max():.3f}.", "",
          "| score below | items kept | share of items | postings with at least one kept item |", "|---|---|---|---|"]
    for th in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
        kt = {t for t, v in stats.items() if v[1] < th}
        cov = sum(1 for x in docs if any(t in kt for t in x)) / max(1, len(docs))
        md.append(f"| {th} | {len(kt):,} | {len(kt) / max(1, len(stats)):.0%} | {cov:.1%} |")
    md += ["", "| item | postings | Laplacian Score | decision |", "|---|---|---|---|"]
    for t, (n, s) in sorted(stats.items(), key=lambda kv: -kv[1][0])[:40]:
        md.append(f"| {labels.get(t, t)[:50]} | {n:,} | {s:.3f} | {'kept' if t in keep else 'DROPPED'} |")
    return "\n".join(md) + "\n"


def tukey_cut(docs, min_count):
    """Upper Tukey fence (Q3 + 1.5 IQR) of the log10 share of postings carrying an item, over items with at least
    min_count postings (the items that can enter the tf-idf). Same rule as script 125."""
    cnt = Counter(t for x in docs for t in set(x))
    sh = np.array([c / max(1, len(docs)) for c in cnt.values() if c >= min_count])
    if len(sh) < 5:
        return None
    ls = np.log10(sh)
    q1, q3 = np.percentile(ls, [25, 75])
    return float(10 ** (q3 + 1.5 * (q3 - q1)))


def skill_blocks(ids, e, skills_file, lc_file, lc_terms_csv, w_skills, w_lc, min_lift, esco_label, docs_dir,
                 board, dim_sk=100, dim_lc=20, only_report=False, max_df=None, filt="ls", ls_max=1.0, ls_k=5, tag=""):
    """filt: 'ls' Laplacian Score (default), 'coherence' the own coherence filter of the first D v2 / D v3 runs, 'none'.
    max_df: None, a share (both blocks), or 'tukey' (ESCO skills only: the cut is computed from the board's own
    distribution of shares, see script 125)."""
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
    sk = {r["id"]: r["skills"] for r in load_jsonl(skills_file)}
    keep = set()
    with open(lc_terms_csv, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if str(r.get("selected", "")).strip() == "1":
                keep.add(r["term"])
    lc = {r["id"]: [t for t in r["terms"] if t in keep] for r in load_jsonl(lc_file)}
    if filt == "ls":
        graph = knn_graph(e, ls_k)
        print(f"  Laplacian Score graph: k={ls_k}, t={graph['t']:.4f}, {graph['S'].nnz // 2:,} edges")
        rep_md = [f"# Laplacian Score filter: {board}", "",
                  f"An item is kept when its Laplacian Score (He, Cai and Niyogi 2005) is below {ls_max}. Graph: {ls_k} nearest neighbours "
                  f"by title embedding (cosine), heat-kernel constant t = {graph['t']:.4f} (mean squared distance over the edges between different titles). A low score means that the postings carrying the item "
                  "are neighbours on the graph.", ""]
    else:
        graph = None
        rep_md = [f"# Skill coherence filter: {board}", "",
                  f"An item is kept when its lift is at least {min_lift}. Lift = how much more alike the titles of the postings "
                  "carrying the item are than the titles of a random set of the same size.", ""]
    blocks, info = [], {}
    for name, d, dim, mindf, w, min_n in (("esco", sk, dim_sk, 5, w_skills, 20), ("lightcast", lc, dim_lc, 3, w_lc, 10)):
        docs = [d.get(i, []) for i in ids]
        info[f"{name}_postings_with_any_raw"] = int(sum(1 for x in docs if x))
        lab = esco_label if name == "esco" else {}
        cut = None
        if max_df == "tukey":
            if name == "esco":
                cut = tukey_cut(docs, mindf)
        elif max_df is not None:
            cut = float(max_df)
        if cut is not None:
            # document-frequency cut (D v3): items present in more than `cut` of the board's postings are boilerplate or generic
            cnt = Counter(t for x in docs for t in set(x))
            common = {t for t, c in cnt.items() if c / max(1, len(docs)) > cut}
            docs = [[t for t in x if t not in common] for x in docs]
            info[f"{name}_max_df_cut"] = round(cut, 6)
            info[f"{name}_items_dropped_max_df"] = len(common)
            rep_md.append(f"### {name}: {len(common)} items dropped because they occur in more than {cut:.2%} of the postings\n")
            rep_md.append("\n".join(f"- {lab.get(t, t)[:60]} ({cnt[t] / max(1, len(docs)):.1%})" for t in sorted(common, key=lambda t: -cnt[t])[:25]) + "\n")
        if only_report:
            if filt == "ls":
                kp, stats = laplacian_filter(docs, graph, min_n, ls_max)
                rep_md.append(laplacian_report(name, stats, kp, lab, docs, ls_max))
            else:
                _, stats = coherence_filter(docs, e, min_n, 0.0)
                rep_md.append(f"### {name}: {len(stats):,} items with at least {min_n} postings\n")
                rep_md.append("| lift threshold | items kept | share of items | postings with at least one kept item |")
                rep_md.append("|---|---|---|---|")
                for th in (0.05, 0.1, 0.15, 0.2, 0.3, 0.4):
                    kt = {t for t, v in stats.items() if v[2] >= th}
                    cov = sum(1 for x in docs if any(t in kt for t in x)) / max(1, len(docs))
                    rep_md.append(f"| {th} | {len(kt):,} | {len(kt) / max(1, len(stats)):.0%} | {cov:.1%} |")
                rep_md.append("")
            continue
        if filt == "ls":
            kp, stats = laplacian_filter(docs, graph, min_n, ls_max)
            rep_md.append(laplacian_report(name, stats, kp, lab, docs, ls_max))
            docs = [[t for t in x if t in kp] for x in docs]
            info[f"{name}_items_kept"] = len(kp)
            info[f"{name}_items_dropped"] = len(stats) - len(kp)
        elif filt == "coherence":
            kp, stats = coherence_filter(docs, e, min_n, min_lift)
            rep_md.append(coherence_report(name, stats, kp, lab))
            docs = [[t for t in x if t in kp] for x in docs]
            info[f"{name}_items_kept"] = len(kp)
            info[f"{name}_items_dropped"] = len(stats) - len(kp)
        info[f"{name}_postings_with_any"] = int(sum(1 for x in docs if x))
        vec = TfidfVectorizer(analyzer=lambda x: x, min_df=mindf, sublinear_tf=True)
        try:
            x = vec.fit_transform(docs)
        except ValueError:
            x = None
        if x is None or x.shape[1] < 3:
            info[f"{name}_features"] = 0
            continue
        k = min(dim, x.shape[1] - 1)
        z = TruncatedSVD(k, random_state=0).fit_transform(x)
        nz = np.linalg.norm(z, axis=1, keepdims=True)
        z = np.where(nz > 1e-9, z / np.maximum(nz, 1e-9), 0.0) * w
        blocks.append(z.astype("float32"))
        info[f"{name}_features"] = int(x.shape[1])
    if only_report or filt != "none":
        Path(docs_dir).mkdir(parents=True, exist_ok=True)
        fname = f"skill_laplacian_{board}{'_' + tag if tag else ''}.md" if filt == "ls" else f"skill_coherence_{board}.md"
        Path(f"{docs_dir}/{fname}").write_text("\n".join(rep_md), encoding="utf-8")
    return (None, info) if only_report else (blocks, info)


# ---------------------------------------------------------------- clustering
def run_umap_hdbscan(x, seed, args):
    import hdbscan
    import umap
    u = umap.UMAP(n_neighbors=args.n_neighbors, n_components=args.dims, min_dist=0.0, metric="cosine",
                  random_state=seed).fit_transform(x)
    h = hdbscan.HDBSCAN(min_cluster_size=args.min_cluster_size, min_samples=args.min_samples, metric="euclidean",
                        cluster_selection_method="eom", gen_min_span_tree=True).fit(u)
    return u, h


def cluster_input(name, x, args, titles):
    from sklearn.cluster import KMeans
    from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score
    runs = []
    for s in args.seeds:
        print(f"  [{name}] UMAP + HDBSCAN, seed {s}")
        runs.append(run_umap_hdbscan(x, s, args))
    u, h = runs[0]
    lab = h.labels_
    k = int(lab.max()) + 1
    m = {"input": name, "n": int(len(lab)), "clusters": k, "noise_share": float((lab < 0).mean()),
         "relative_validity": float(h.relative_validity_), "min_cluster_size": args.min_cluster_size}
    st = []
    for (_, h2) in runs[1:]:
        both = (lab >= 0) & (h2.labels_ >= 0)
        st.append({"clusters": int(h2.labels_.max()) + 1, "ari_on_shared": float(adjusted_rand_score(lab[both], h2.labels_[both])) if both.sum() else None,
                   "shared_share": float(both.mean())})
    m["stability"] = st
    if k >= 2:
        km = KMeans(k, n_init=5, random_state=1).fit(u).labels_
        nn = lab >= 0
        m["kmeans_ami_on_non_noise"] = float(adjusted_mutual_info_score(lab[nn], km[nn]))
        m["kmeans_ari_on_non_noise"] = float(adjusted_rand_score(lab[nn], km[nn]))
    return lab, h.probabilities_, m


# ---------------------------------------------------------------- reporting
def report(board, name, recs, lab, prob, m, args, esco_label, lc_by_id, sk_by_id):
    n = len(lab)
    by = defaultdict(list)
    for i, c in enumerate(lab):
        if c >= 0:
            by[int(c)].append(i)
    md = [f"# Clusters: {board}, input {name}", "",
          f"{n:,} postings; {m['clusters']} clusters; noise {m['noise_share']:.1%}; relative validity {m['relative_validity']:.3f}; "
          f"min_cluster_size {args.min_cluster_size}.", ""]
    for j, s in enumerate(m["stability"], 2):
        md.append(f"- Stability seed 1 vs seed {j}: ARI {s['ari_on_shared']:.3f} on the {s['shared_share']:.1%} of postings clustered in both; "
                  f"{s['clusters']} clusters.")
    if "kmeans_ami_on_non_noise" in m:
        md.append(f"- k-means with k={m['clusters']} on the same UMAP space: AMI {m['kmeans_ami_on_non_noise']:.3f}, ARI {m['kmeans_ari_on_non_noise']:.3f} against HDBSCAN (non-noise postings).")
    md += ["", f"## Named emerging occupations (regex on the cleaned title; found or not, never forced)", ""]
    md.append("| occupation | titles matched | in a cluster | top clusters (matches / cluster size) |")
    md.append("|---|---|---|---|")
    hits_by_cluster = defaultdict(set)
    for occ, rx in NAMED_RX.items():
        idx = [i for i, r in enumerate(recs) if rx.search(r.get("title_clean") or "")]
        cl = Counter(int(lab[i]) for i in idx if lab[i] >= 0)
        for c in cl:
            hits_by_cluster[c].add(occ)
        top = ", ".join(f"C{c} ({v}/{len(by[c])})" for c, v in cl.most_common(4)) or "-"
        md.append(f"| {occ} | {len(idx)} | {sum(cl.values())} | {top} |")
    show = sorted(by, key=lambda c: -len(by[c]))[: args.show]
    show += [c for c in sorted(hits_by_cluster) if c not in show]
    md += ["", f"## Largest {args.show} clusters plus every cluster hit by a named occupation", ""]
    for c in show:
        idx = by[c]
        order = sorted(idx, key=lambda i: -prob[i])
        seen, tt = set(), []
        for i in order:
            t = text_a(recs[i])
            if t.lower() not in seen:
                seen.add(t.lower())
                tt.append(t[:80])
            if len(tt) == 6:
                break
        sc, lc = Counter(), Counter()
        for i in idx:
            sc.update(sk_by_id.get(recs[i]["id"], []))
            lc.update(lc_by_id.get(recs[i]["id"], []))
        sk = "; ".join(f"{esco_label.get(u, u.rsplit('/', 1)[-1])} ({v / len(idx):.0%})" for u, v in sc.most_common(6))
        lct = "; ".join(f"{t} ({v})" for t, v in lc.most_common(5))
        tag = f" [named: {', '.join(sorted(hits_by_cluster[c]))}]" if c in hits_by_cluster else ""
        md.append(f"### C{c}: {len(idx):,} postings ({len(idx) / n:.2%}){tag}")
        md.append("- Titles: " + " | ".join(tt))
        if sk:
            md.append("- ESCO skills: " + sk)
        if lct:
            md.append("- Lightcast terms: " + lct)
        md.append("")
    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True, help="jobbland | lesjeudis | jobsde (the label used by script 90)")
    ap.add_argument("--input", nargs="+", default=["A", "D"], choices=["A", "D"])
    ap.add_argument("--titles", help="default data/tagged/titles_<board>.jsonl")
    ap.add_argument("--skills", help="default data/tagged/skills_local_full_<corpus>_t0.60.jsonl")
    ap.add_argument("--lightcast", help="default data/tagged/lightcast_block_<board>.jsonl")
    ap.add_argument("--lc-terms", default="lexicon/lightcast_block_terms.csv")
    ap.add_argument("--esco-csv", default="lexicon/skills.csv", help="id,description : only to print skill names")
    ap.add_argument("--model", default="intfloat/multilingual-e5-large")
    ap.add_argument("--out", default="data/cluster")
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--min-cluster-size", type=int, default=40)
    ap.add_argument("--min-samples", type=int, default=10)
    ap.add_argument("--n-neighbors", type=int, default=30)
    ap.add_argument("--dims", type=int, default=10)
    ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--w-skills", type=float, default=0.5)
    ap.add_argument("--w-lc", type=float, default=0.3)
    ap.add_argument("--filter", choices=["ls", "coherence", "none"], default="ls",
                    help="which items of the skill blocks are kept: ls = Laplacian Score (default), coherence = the own filter of the first D v2/D v3 runs, none = every item (D v1)")
    ap.add_argument("--ls-k", type=int, default=5, help="Laplacian Score: nearest neighbours in the graph (the paper uses 5)")
    ap.add_argument("--ls-max", type=float, default=1.0, help="Laplacian Score: keep items with a score below this value (a feature unrelated to the graph scores about 1)")
    ap.add_argument("--ls-only", action="store_true", help="no clustering: write docs/skill_laplacian_<board>.md with kept-counts per threshold")
    ap.add_argument("--min-lift", type=float, default=0.15, help="coherence filter only (--filter coherence)")
    ap.add_argument("--no-coherence", action="store_true", help="same as --filter none (input D v1)")
    ap.add_argument("--coherence-only", action="store_true", help="no clustering: write docs/skill_coherence_<board>.md with kept-counts per threshold (--filter coherence)")
    ap.add_argument("--max-df", default=None, help="D v3: drop items present in more than this share of the board's postings, e.g. 0.05 (ESCO and Lightcast), "
                    "or the word tukey: the cut is the upper Tukey fence of the board's own distribution of shares, ESCO skills only (script 125)")
    ap.add_argument("--tag", default="", help="suffix for the output files, e.g. v2, so A and D v1 are not overwritten")
    ap.add_argument("--show", type=int, default=60)
    ap.add_argument("--limit", type=int, default=0, help="test on the first N postings")
    ap.add_argument("--mock", action="store_true", help="no GPU model: character n-gram embedding (pipeline test only)")
    args = ap.parse_args()
    if args.max_df is not None and args.max_df != "tukey":
        args.max_df = float(args.max_df)
    if args.no_coherence:
        args.filter = "none"

    corpus_name = {"jobbland": "jobbland", "lesjeudis": "lesjeudis", "jobsde": "jobsde"}[args.board]
    titles = args.titles or f"data/tagged/titles_{args.board}.jsonl"
    skills = args.skills or f"data/tagged/skills_local_full_{corpus_name}_t0.60.jsonl"
    lcf = args.lightcast or f"data/tagged/lightcast_block_{args.board}.jsonl"
    recs = load_jsonl(titles)
    if args.limit:
        recs = recs[: args.limit]
    ids = [r["id"] for r in recs]
    Path(args.out).mkdir(parents=True, exist_ok=True)
    Path(args.docs).mkdir(parents=True, exist_ok=True)
    print(f"{args.board}: {len(recs):,} postings; {sum(1 for r in recs if not r['has_title']):,} without a title")

    esco_label = {}
    if Path(args.esco_csv).exists():
        with open(args.esco_csv, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                esco_label[r["id"]] = r.get("description", "")[:40]
    sk_by_id = {r["id"]: r["skills"] for r in load_jsonl(skills)} if Path(skills).exists() else {}
    lc_by_id = {r["id"]: r["terms"] for r in load_jsonl(lcf)} if Path(lcf).exists() else {}

    cache = None if args.limit else f"{args.out}/emb_{args.board}.npy"
    e = embed_titles([text_a(r) for r in recs], args.model, cache, args.mock)

    if args.coherence_only or args.ls_only:
        skill_blocks(ids, e, skills, lcf, args.lc_terms, args.w_skills, args.w_lc, args.min_lift, esco_label, args.docs,
                     args.board, only_report=True, max_df=args.max_df, filt="coherence" if args.coherence_only else "ls",
                     ls_max=args.ls_max, ls_k=args.ls_k, tag=args.tag)
        print("report written to", args.docs)
        return
    for name in args.input:
        if name == "A":
            x, extra = e, {}
        else:
            if not Path(skills).exists():
                sys.exit(f"missing {skills}")
            blocks, extra = skill_blocks(ids, e, skills, lcf, args.lc_terms, args.w_skills, args.w_lc,
                                         args.min_lift, esco_label, args.docs, args.board,
                                         max_df=args.max_df, filt=args.filter, ls_max=args.ls_max, ls_k=args.ls_k, tag=args.tag)
            x = np.hstack([e] + blocks)
            x = x / np.linalg.norm(x, axis=1, keepdims=True)
        lab, prob, m = cluster_input(name, x, args, recs)
        name = name + args.tag if name == "D" else name
        m.update(extra)
        m["board"] = args.board
        with open(f"{args.out}/labels_{args.board}_{name}.jsonl", "w", encoding="utf-8") as f:
            for r, c, p in zip(recs, lab, prob):
                f.write(json.dumps({"id": r["id"], "day": r["day"], "cluster": int(c), "prob": round(float(p), 4)}) + "\n")
        Path(f"{args.out}/metrics_{args.board}_{name}.json").write_text(json.dumps(m, indent=1), encoding="utf-8")
        Path(f"{args.docs}/clusters_{args.board}_{name}.md").write_text(
            report(args.board, name, recs, lab, prob, m, args, esco_label, lc_by_id, sk_by_id), encoding="utf-8")
        print(f"[{name}] {m['clusters']} clusters, noise {m['noise_share']:.1%}, relative validity {m['relative_validity']:.3f}, "
              f"stability ARI {[round(s['ari_on_shared'], 3) for s in m['stability']]}, "
              f"k-means AMI {m.get('kmeans_ami_on_non_noise', float('nan')):.3f}")


if __name__ == "__main__":
    main()
