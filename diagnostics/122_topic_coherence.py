"""
Month 4: topic coherence (NPMI) and topic diversity of the clusters of each input, the two measures used to evaluate embedding + UMAP + HDBSCAN
pipelines on text (BERTopic, Grootendorst 2022).

For every cluster (noise left out) of every input:
  top words   the topn words of the cluster by class-based tf-idf (c-TF-IDF, Grootendorst 2022): tf(t,c) * log(1 + A / f_t), where tf is the count of
              the word in the titles of the cluster, A the average number of words per cluster and f_t the count of the word over all clusters.
              Words are lower-case tokens of at least 3 letters, minus a short English, French, German and Swedish stop list.
  C_NPMI      coherence of the top words (Roeder, Both and Hinneburg 2015): mean over all word pairs of the normalised pointwise mutual information,
              NPMI(wi,wj) = log(P(wi,wj) / (P(wi) P(wj))) / -log P(wi,wj), -1 when the two words never occur together, +1 when they always do.
              Probabilities: share of the board's titles (the reference corpus, all postings with a title) that contain the word (pair).
              A title is one document (boolean document co-occurrence); this is a simplification of the sliding-window version used in gensim.
Per input:
  median and posting-weighted mean C_NPMI over clusters; topic diversity (Dieng, Ruiz and Blei 2020) = share of distinct words among the
  top --div-topn words of all clusters (1 = no word shared between clusters).
No cut-off is applied: inputs are compared by these values, as in the topic-modelling literature.

Needs (same files as script 107): data/tagged/titles_<board>.jsonl, data/cluster/labels_<board>_<input>.jsonl for each input
(A, Dv2, Dv3; the label files of script 92).
Run (project root, venv active):
    python -m diagnostics.122_topic_coherence --board lesjeudis --inputs A Dv2 Dv3
Output: docs/topic_coherence_<board>.md, data/cluster/topic_coherence_<board>.csv
"""
import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

STOP = set("""the and for with from you your our are will this that der die das und mit für von zum zur den dem des ein eine einer eines les des une dans pour avec sur par aux
och att för med som till hos inom the all new senior junior sr jr h/f m/w/d m/f/d f/h""".split())


def tokens(t):
    return [w for w in re.findall(r"[^\W\d_]{3,}", (t or "").lower()) if w not in STOP]


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--inputs", nargs="+", default=["A", "Dv2", "Dv3"])
    ap.add_argument("--titles")
    ap.add_argument("--labels-dir", default="data/cluster")
    ap.add_argument("--topn", type=int, default=10)
    ap.add_argument("--div-topn", type=int, default=25)
    ap.add_argument("--min-postings", type=int, default=20)
    ap.add_argument("--show", type=int, default=10)
    a = ap.parse_args()
    tp = a.titles or f"data/tagged/titles_{a.board}.jsonl"
    recs = [r for r in jl(tp) if r.get("has_title") and (r.get("title_clean") or "").strip()]
    toks = {str(r["id"]): set(tokens(r["title_clean"])) for r in recs}
    toks_list = {str(r["id"]): tokens(r["title_clean"]) for r in recs}
    N = len(toks)
    df = Counter(w for s in toks.values() for w in s)
    pair_cache = {}

    def p_pair(w1, w2):
        k = (w1, w2) if w1 < w2 else (w2, w1)
        if k not in pair_cache:
            pair_cache[k] = sum(1 for s in toks.values() if w1 in s and w2 in s)
        return pair_cache[k]

    def npmi(w1, w2):
        c12 = p_pair(w1, w2)
        if c12 == 0:
            return -1.0
        p12 = c12 / N
        p1, p2 = df[w1] / N, df[w2] / N
        if p12 >= 1:
            return 1.0
        return math.log(p12 / (p1 * p2)) / -math.log(p12)

    rows, md = [], [f"# Topic coherence (C_NPMI) and topic diversity of the clusters: {a.board}", "",
                    f"Reference corpus: {N:,} titles with a title (boolean document co-occurrence, one title = one document). Top {a.topn} words per cluster by class-based tf-idf; "
                    f"clusters with at least {a.min_postings} titles; diversity over the top {a.div_topn} words. NPMI is -1 when two words never occur together and +1 when they always do.", "",
                    "| input | clusters | noise (postings with a title) | median C_NPMI | mean C_NPMI weighted by postings | topic diversity |", "|---|---|---|---|---|---|"]
    detail = []
    for name in a.inputs:
        lab = {str(r["id"]): int(r["cluster"]) for r in jl(f"{a.labels_dir}/labels_{a.board}_{name}.jsonl")}
        by = defaultdict(Counter); size = Counter()
        n_noise = 0
        for i, ws in toks_list.items():
            c = lab.get(i, -1)
            if c < 0:
                n_noise += 1
                continue
            by[c].update(ws); size[c] += 1
        use = [c for c in by if size[c] >= a.min_postings]
        tot_words = {c: sum(by[c].values()) for c in by}
        A = np.mean(list(tot_words.values())) if tot_words else 1
        f_t = Counter()
        for c in by:
            f_t.update(by[c])
        tops, res = {}, {}
        for c in by:
            sc = {t: n * math.log(1 + A / f_t[t]) for t, n in by[c].items()}
            tops[c] = [t for t, _ in sorted(sc.items(), key=lambda x: -x[1])[:max(a.topn, a.div_topn)]]
        for c in use:
            tw = [t for t in tops[c][:a.topn] if t in df]
            pairs = [npmi(x, y) for x, y in combinations(tw, 2)]
            res[c] = float(np.mean(pairs)) if pairs else float("nan")
            rows.append({"input": name, "cluster": c, "postings": size[c], "c_npmi": round(res[c], 4), "top_words": " ".join(tops[c][:a.topn])})
        vals = np.array([res[c] for c in use if not math.isnan(res[c])])
        w = np.array([size[c] for c in use if not math.isnan(res[c])], dtype=float)
        alltop = [t for c in by for t in tops[c][:a.div_topn]]
        div = len(set(alltop)) / max(1, len(alltop))
        md.append(f"| {name} | {len(by)} | {100 * n_noise / N:.1f}% | {np.median(vals):.3f} | {np.average(vals, weights=w):.3f} | {div:.3f} |")
        low = sorted(use, key=lambda c: res[c])[:a.show]
        detail += ["", f"### {name}: the {a.show} clusters with the lowest C_NPMI", "", "| cluster | titles | C_NPMI | top words |", "|---|---|---|---|"]
        detail += [f"| {c} | {size[c]} | {res[c]:.3f} | {' '.join(tops[c][:a.topn])} |" for c in low]
    md += detail
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/topic_coherence_{a.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    with open(f"data/cluster/topic_coherence_{a.board}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["input", "cluster", "postings", "c_npmi", "top_words"]); w.writeheader(); w.writerows(rows)
    print("\n".join(md[:12])); print(f"docs/topic_coherence_{a.board}.md written")


if __name__ == "__main__":
    main()
