"""
Month 4: give the title-less postings a cluster through their inferred title, without re-clustering the board.

Re-clustering (script 92 with the inferred titles) would change every cluster number and the candidate lists. This script keeps the
clusters of script 92 as they are and moves only the title-less postings: the inferred title (script 99) is embedded with the same model
(multilingual-e5-large, "query: " prefix) and the posting goes to the cluster that most of its nearest titled postings belong to
(cosine similarity, --k neighbours, titled postings only). If fewer than --min-agree of the neighbours share a cluster, the posting
goes to -1 (no clear cluster). Postings the model answered UNKNOWN for keep their old cluster.

Validation: the --validation postings of script 99 (titled, title hidden) are placed the same way, without themselves among their
neighbours, and the cluster found from the INFERRED title is compared with the cluster they actually have from their REAL title.

Output
  data/cluster/labels_<label>_<A>inf.jsonl     as labels_<label>_<A>.jsonl, with "cluster" changed for the moved postings and "moved": true
  docs/reassign_<label>.md                     where the title-less postings came from and went, and the validation
Use it as an input name for the later scripts:  python -m diagnostics.93_cluster_series ... --input Ainf

Run (project root, venv active; the embedding of ~1,400 short titles also runs on the Mac CPU, or use Colab with --device cuda):
    python -m diagnostics.99d_reassign_inferred --label jobbland
Needs: data/tagged/titles_<label>.jsonl (ORIGINAL), data/tagged/inferred_titles_<label>.jsonl, data/cluster/emb_<label>.npy and
data/cluster/labels_<label>_A.jsonl (written by script 92).
"""

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def embed(texts, model_name, device):
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer(model_name, device=device)
    e = m.encode(["query: " + t for t in texts], batch_size=64, normalize_embeddings=True, show_progress_bar=True)
    return e.astype("float32")


def vote(sims_row_idx, sims_row_val, lab_titled, k, min_agree):
    top = sims_row_idx[:k]
    c = Counter(lab_titled[top].tolist())
    cl, n = c.most_common(1)[0]
    return (cl if n / k >= min_agree else -1), n / k


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--label", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--titles")
    ap.add_argument("--inferred")
    ap.add_argument("--emb")
    ap.add_argument("--labels")
    ap.add_argument("--k", type=int, default=15)
    ap.add_argument("--min-agree", type=float, default=0.5)
    ap.add_argument("--model", default="intfloat/multilingual-e5-large")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--mock", action="store_true", help="pipeline test: character n-gram embedding of everything, cache ignored")
    a = ap.parse_args()
    tp = a.titles or f"data/tagged/titles_{a.label}.jsonl"
    ip = a.inferred or f"data/tagged/inferred_titles_{a.label}.jsonl"
    ep = a.emb or f"data/cluster/emb_{a.label}.npy"
    lp = a.labels or f"data/cluster/labels_{a.label}_{a.input}.jsonl"
    recs = jl(tp)
    ids = [str(r["id"]) for r in recs]
    inf = {str(r["id"]): r for r in jl(ip)}
    labrows = jl(lp)
    lab = {str(r["id"]): int(r["cluster"]) for r in labrows}
    has = np.array([bool(r.get("has_title", True)) for r in recs])
    row = {i: k for k, i in enumerate(ids)}
    texts_title = [(r.get("title_clean") or "").strip() for r in recs]

    movers = [i for i in ids if i in inf and inf[i]["kind"] == "inferred" and inf[i]["title_inferred"] != "UNKNOWN" and not has[row[i]]]
    vals = [i for i in ids if i in inf and inf[i]["kind"] == "validation" and inf[i]["title_inferred"] != "UNKNOWN" and has[row[i]]]
    q_ids = movers + vals
    q_text = [inf[i]["title_inferred"] for i in q_ids]
    if a.mock:
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer
        allt = [texts_title[k] if has[k] else "unknown" for k in range(len(recs))] + q_text
        x = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4), min_df=1).fit_transform(allt)
        z = TruncatedSVD(min(32, x.shape[1] - 1), random_state=0).fit_transform(x)
        z = z / np.maximum(np.linalg.norm(z, axis=1, keepdims=True), 1e-9)
        E, Q = z[:len(recs)].astype("float32"), z[len(recs):].astype("float32")
    else:
        E = np.load(ep)
        if len(E) != len(recs):
            raise SystemExit(f"{ep} has {len(E)} rows but {tp} has {len(recs)} postings: they must come from the same run of script 92")
        Q = embed(q_text, a.model, a.device)
    tidx = np.where(has)[0]
    lab_t = np.array([lab.get(ids[k], -1) for k in tidx])
    Et = E[tidx]
    pos_in_t = {ids[k]: j for j, k in enumerate(tidx)}
    new, agree = {}, {}
    for s in range(0, len(q_ids), 256):
        sims = Q[s:s + 256] @ Et.T
        for r_, i in enumerate(q_ids[s:s + 256]):
            if i in pos_in_t:
                sims[r_, pos_in_t[i]] = -9
            order = np.argpartition(-sims[r_], a.k)[:a.k]
            order = order[np.argsort(-sims[r_][order])]
            new[i], agree[i] = vote(order, sims[r_][order], lab_t, a.k, a.min_agree)

    L = [f"# Title-less postings placed through their inferred title: {a.label} input {a.input}\n",
         f"{len(movers):,} title-less postings with an inferred title; {len(vals):,} validation postings (titled, title hidden). Nearest {a.k} titled postings by cosine similarity; "
         f"a cluster is taken when at least {a.min_agree:.0%} of them agree, otherwise -1.\n",
         "## Validation: cluster from the inferred title against cluster from the real title\n"]
    same = [new[i] == lab.get(i, -1) for i in vals]
    in_cl = [i for i in vals if lab.get(i, -1) >= 0]
    L.append(f"All {len(vals)}: same cluster in {np.mean(same):.0%}. Postings whose real title lies in a cluster (not -1), {len(in_cl)}: same cluster in "
             f"{np.mean([new[i] == lab[i] for i in in_cl]):.0%}; placed in -1 instead in {np.mean([new[i] == -1 for i in in_cl]):.0%}; in another cluster in "
             f"{np.mean([new[i] not in (-1, lab[i]) for i in in_cl]):.0%}. Real title in -1 ({len(vals) - len(in_cl)}): inferred title also in -1 in "
             f"{np.mean([new[i] == -1 for i in vals if lab.get(i, -1) == -1]) if len(vals) > len(in_cl) else 0:.0%}.\n")
    L.append("## Where the title-less postings were and where they go\n")
    old = Counter(lab.get(i, -2) for i in movers)
    L.append("Old clusters (by first 150 description characters): " + ", ".join(f"{c} ({n})" for c, n in old.most_common(8)) + ".\n")
    dest = Counter(new[i] for i in movers)
    L.append(f"New clusters: {len(dest)} different; in -1: {dest.get(-1, 0):,} ({dest.get(-1, 0) / max(len(movers), 1):.0%}). Largest destinations: "
             + ", ".join(f"{c} ({n})" for c, n in dest.most_common(12)) + ".\n")
    L.append("Clusters 171 and 168 (the title-less clusters) after the move: " + ", ".join(
        f"{c}: {sum(1 for i in ids if lab.get(i) == c)} -> {sum(1 for i in ids if (new[i] if i in new and i in set(movers) else lab.get(i)) == c)}" for c in (171, 168)) + ".\n")
    mv = set(movers)
    out_p = f"data/cluster/labels_{a.label}_{a.input}inf.jsonl"
    with open(out_p, "w", encoding="utf-8") as f:
        for r in labrows:
            i = str(r["id"])
            if i in mv:
                r = dict(r)
                r["cluster"], r["moved"] = int(new[i]), True
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/reassign_{a.label}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{out_p} written, docs/reassign_{a.label}.md written")


if __name__ == "__main__":
    main()
