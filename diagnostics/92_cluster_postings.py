"""
Month 4, step 3: cluster the postings of ONE board into occupation clusters (runs on Colab; the Mac has no torch).

Two inputs are clustered and compared:
  A  the cleaned job title (multilingual-e5; title-less postings use the first 150 characters of the description)
  D  the same title embedding + the ESCO skill vector of the FULL text (script 69b, local extractor, threshold 0.6)
     + the pruned Lightcast phrase block (script 91, only terms with selected=1 in lexicon/lightcast_block_terms.csv).
     Skills and Lightcast terms are tf-idf weighted and reduced with TruncatedSVD; every block is L2-normalised, so
     the title keeps weight 1, ESCO skills --w-skills (0.5) and Lightcast terms --w-lc (0.3).
     v2: before weighting, every skill/term passes a COHERENCE FILTER (see coherence_filter): v1 clustered on
     extractor false positives and generic skills ("sell bicycles" on postmen, "assume responsibility").
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
    "export control specialist": r"export[- ]?control|exportkontroll|exportkontrolle|ausfuhrkontroll|contr[oô]le des exportations|dual[- ]use",
    "supply chain resilience analyst": r"supply[- ]chain.{0,20}(risk|resilien)|resilien.{0,20}supply|leveranskedje.{0,20}(risk|resilien)",
    "semiconductor process engineer": r"(semiconductor|halvledar|halbleiter|semi-?conducteur|wafer|cleanroom).{0,40}(process|engineer|ingenj|ingenieur|ing[eé]nieur)|"
                                      r"(process|engineer|ingenj|ingenieur|ing[eé]nieur).{0,40}(semiconductor|halvledar|halbleiter|semi-?conducteur|wafer)",
    "battery cell technician": r"(batter|akku|accumulateur).{0,30}(cell|zell|technician|tekniker|techniker|technicien|operat|process)|"
                               r"(cell|zell|technician|tekniker|techniker|technicien|operator).{0,30}(batter|akku|accumulateur)",
    "critical materials specialist": r"critical (raw )?material|kritiska (råvaror|material)|kritische rohstoffe|rare earth|sällsynta jordartsmetaller|"
                                     r"mati[eè]res? (premi[eè]res? )?critiques|raw materials? (specialist|manager|analyst|engineer)",
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


def skill_blocks(ids, e, skills_file, lc_file, lc_terms_csv, w_skills, w_lc, min_lift, esco_label, docs_dir,
                 board, dim_sk=100, dim_lc=20):
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
    sk = {r["id"]: r["skills"] for r in load_jsonl(skills_file)}
    keep = set()
    with open(lc_terms_csv, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if str(r.get("selected", "")).strip() == "1":
                keep.add(r["term"])
    lc = {r["id"]: [t for t in r["terms"] if t in keep] for r in load_jsonl(lc_file)}
    blocks, info, rep_md = [], {}, [f"# Skill coherence filter: {board}", "",
                                    f"An item is kept when its lift is at least {min_lift}. Lift = how much more alike the titles of the postings "
                                    "carrying the item are than the titles of a random set of the same size.", ""]
    for name, d, dim, mindf, w, min_n in (("esco", sk, dim_sk, 5, w_skills, 20), ("lightcast", lc, dim_lc, 3, w_lc, 10)):
        docs = [d.get(i, []) for i in ids]
        info[f"{name}_postings_with_any_raw"] = int(sum(1 for x in docs if x))
        if min_lift is not None:
            keep, stats = coherence_filter(docs, e, min_n, min_lift)
            rep_md.append(coherence_report(name, stats, keep, esco_label if name == "esco" else {}))
            docs = [[t for t in x if t in keep] for x in docs]
            info[f"{name}_items_kept"] = len(keep)
            info[f"{name}_items_dropped"] = len(stats) - len(keep)
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
    if min_lift is not None:
        Path(docs_dir).mkdir(parents=True, exist_ok=True)
        Path(f"{docs_dir}/skill_coherence_{board}.md").write_text("\n".join(rep_md), encoding="utf-8")
    return blocks, info


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
    ap.add_argument("--min-lift", type=float, default=0.10, help="coherence filter for skills / Lightcast terms (see coherence_filter)")
    ap.add_argument("--no-coherence", action="store_true", help="old behaviour: every skill kept (input D v1)")
    ap.add_argument("--tag", default="", help="suffix for the output files, e.g. v2, so A and D v1 are not overwritten")
    ap.add_argument("--show", type=int, default=60)
    ap.add_argument("--limit", type=int, default=0, help="test on the first N postings")
    ap.add_argument("--mock", action="store_true", help="no GPU model: character n-gram embedding (pipeline test only)")
    args = ap.parse_args()

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

    for name in args.input:
        if name == "A":
            x, extra = e, {}
        else:
            if not Path(skills).exists():
                sys.exit(f"missing {skills}")
            blocks, extra = skill_blocks(ids, e, skills, lcf, args.lc_terms, args.w_skills, args.w_lc,
                                         None if args.no_coherence else args.min_lift, esco_label, args.docs, args.board)
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
