"""
Month 4, supervisor request 3b: seeded (constrained) clustering with the named occupations as fixed centres. Complementary to
HDBSCAN: a named occupation cannot dissolve into a larger cluster, and the question becomes whether the seed grows.
Runs on the Mac (no GPU): it reads the title embeddings cached by script 92 (data/cluster/emb_<board>.npy), the cleaned titles
(data/tagged/titles_<board>.jsonl) and the corpus (for day weights). One board per run.

Method
  1. Seed postings: the postings whose cleaned title matches the occupation's regex (the NAMED patterns of script 92).
     An occupation with fewer than --min-seed matching titles is reported but not used as a centre.
  2. Centre = the mean of the (L2-normalised) title embeddings of the seed postings, normalised again.
  3. A posting belongs to the occupation when its cosine similarity to the centre is at least the threshold. The threshold is
     swept (--thresholds, default 0.80 0.85 0.88 0.90) and the number of postings is reported for each, so the choice is visible.
     The seed postings always belong, whatever their similarity. A posting nearest to several centres goes to the nearest.
  4. The members beyond the regex matches are listed with their titles (--show per occupation) so false positives can be read.
  5. Per month: weighted share of the board's postings in the occupation (day weights of script 52, duplicates removed), and the
     number of postings taken. A real new occupation grows; a stable or falling share is a finding too.
  6. Comparison with HDBSCAN (labels_<board>_<input>.jsonl, if present): which HDBSCAN clusters the members fall into.

Output: docs/seeded_<board>.md, data/cluster/seeded_<board>.csv (id, occupation, similarity, seed, threshold 0.85 by default)
Run (project root, venv active):
    python -m diagnostics.106_seeded_clusters --board lesjeudis --input A --corpus data/raw/corpus_lesjeudis.com_2024-08_2025-04.jsonl data/raw/corpus_lesjeudis.com_2025-05_2025-09.jsonl
Test without data: --mock
"""

import argparse
import csv
import importlib.util
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


def load92():
    p = Path(__file__).with_name("92_cluster_postings.py")
    spec = importlib.util.spec_from_file_location("cp92", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_all(paths):
    try:
        from diagnostics.corpus_io import load_corpus
    except ImportError:
        from corpus_io import load_corpus
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tmp:
        for p in paths:
            for line in open(p, encoding="utf-8"):
                if line.strip():
                    tmp.write(line.rstrip("\n") + "\n")
        name = tmp.name
    try:
        return load_corpus(name)
    finally:
        Path(name).unlink()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A", help="HDBSCAN labels to compare with (labels_<board>_<input>.jsonl)")
    ap.add_argument("--titles")
    ap.add_argument("--emb")
    ap.add_argument("--corpus", nargs="+")
    ap.add_argument("--thresholds", type=float, nargs="+", default=[0.90, 0.92, 0.94, 0.96])
    ap.add_argument("--use", type=float, default=None, help="absolute threshold used for the series and the output file; default: the seed-relative threshold (the lowest leave-one-out similarity of the occupation's own seed postings)")
    ap.add_argument("--min-seed", type=int, default=5)
    ap.add_argument("--cluster-seeds", type=int, nargs="+", default=[], help="HDBSCAN cluster numbers (of --input) to use as seeds too: the centre is the mean embedding of the cluster's postings, and the members beyond the cluster show what HDBSCAN left in noise or in other clusters")
    ap.add_argument("--no-named", action="store_true", help="leave the seven named occupations out (use with --cluster-seeds); the report is then docs/seeded_clusters_<board>.md")
    ap.add_argument("--show", type=int, default=12)
    ap.add_argument("--mock", action="store_true")
    a = ap.parse_args()

    cp = load92()
    titles = a.titles or f"data/tagged/titles_{a.board}.jsonl"
    emb_p = a.emb or f"data/cluster/emb_{a.board}.npy"
    recs = cp.load_jsonl(titles)
    ids = [str(r["id"]) for r in recs]
    txt = [(r.get("title_clean") or "").strip() if r.get("has_title") else "" for r in recs]
    if a.mock:
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer
        e = TruncatedSVD(32, random_state=0).fit_transform(TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 4)).fit_transform([cp.text_a(r) for r in recs]))
        e = (e / np.maximum(np.linalg.norm(e, axis=1, keepdims=True), 1e-9)).astype("float32")
    else:
        e = np.load(emb_p)
        if len(e) != len(recs):
            raise SystemExit(f"{emb_p} has {len(e)} rows but {titles} has {len(recs)}: use the titles file the embeddings were made from (jobbland: titles_jobbland_inf.jsonl)")

    seeds = {}
    for name, rx in cp.NAMED_RX.items():
        hit = np.array([bool(t) and bool(rx.search(t)) for t in txt])
        seeds[name] = hit
    if a.no_named:
        seeds = {}
    if a.cluster_seeds:
        lp0 = Path(f"data/cluster/labels_{a.board}_{a.input}.jsonl")
        if not lp0.exists():
            raise SystemExit(f"{lp0} not found: --cluster-seeds needs the labels of script 92")
        lab0 = {str(r["id"]): r["cluster"] for r in cp.load_jsonl(str(lp0))}
        arr = np.array([lab0.get(i, -2) for i in ids])
        for c in a.cluster_seeds:
            seeds[f"C{c}"] = arr == c
    cluster_names = {f"C{c}" for c in a.cluster_seeds}
    OUT = f"seeded_clusters_{a.board}" if a.no_named else f"seeded_{a.board}"
    use = [n for n, h in seeds.items() if h.sum() >= a.min_seed]
    md = [f"# Seeded clustering with the named occupations: {a.board}", "",
          f"{len(recs):,} postings. Centre = mean title embedding of the postings whose cleaned title matches the occupation; a posting joins when its cosine similarity to the centre is at least the threshold; the matching postings always belong.", "",
          "## Seeds", "", "| occupation | titles matching | used as a centre |", "|---|---|---|"]
    for n, h in seeds.items():
        md.append(f"| {n} | {int(h.sum())} | {'yes' if n in use else 'no (fewer than ' + str(a.min_seed) + ')'} |")
    if not use:
        md += ["", "No occupation has enough matching titles to form a centre, so there is nothing to extend. The counts above are the result."]
        Path("docs").mkdir(exist_ok=True)
        Path(f"docs/{OUT}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        print("\n".join(md))
        return

    KEY = "rel" if a.use is None else a.use
    cent = {}
    for n in use:
        c = e[seeds[n]].mean(0)
        cent[n] = c / np.linalg.norm(c)
    C = np.stack([cent[n] for n in use])
    S = e @ C.T                                   # cosine similarity to every centre
    near = S.argmax(1)
    best = S.max(1)
    rel, loo_stats, bg, outliers = {}, {}, {}, {}
    for j, n in enumerate(use):
        idx = np.where(seeds[n])[0]
        tot = e[idx].sum(0)
        loo = []
        for i in idx:
            c = tot - e[i]
            loo.append(float(e[i] @ (c / np.linalg.norm(c))))
        loo = np.array(loo)
        loo_stats[n] = (float(loo.min()), float(np.median(loo)), float(loo.max()))
        bg[n] = tuple(float(np.quantile(S[:, j], q)) for q in (0.5, 0.95, 0.99))
        # an outlier seed (a title like "TULL24STO, Export Control, 10Yhp, v18-19") must not pull the threshold down into the background
        # a cluster seed has hundreds of postings and a few odd ones: its floor is the 10th percentile of the leave-one-out similarities, not the minimum
        floor = float(np.quantile(loo, 0.10)) if n in cluster_names else float(loo.min())
        rel[n] = max(floor, bg[n][2])
        low = [(txt[i], float(l)) for i, l in zip(idx, loo) if l < bg[n][2]]
        outliers[n] = low

    md += ["", "## The seed titles", ""]
    for n in use:
        c = Counter(txt[i] for i in np.where(seeds[n])[0])
        md.append(f"- {n}: " + "; ".join(f"{t} ({k})" for t, k in c.most_common(15)))
    md += ["", "## Calibration: how similar is similar?",
           "multilingual-e5 gives high cosine similarity to almost any pair of short texts, so an absolute threshold such as 0.85 means little. "
           "Background = the similarity of ALL postings of the board to the centre. Seed leave-one-out = each seed posting against the centre made from the others.", "",
           "| occupation | background median | background 95th pct | background 99th pct | seed leave-one-out lowest | median | highest |", "|---|---|---|---|---|---|---|"]
    for n in use:
        md.append(f"| {n} | {bg[n][0]:.3f} | {bg[n][1]:.3f} | {bg[n][2]:.3f} | {loo_stats[n][0]:.3f} | {loo_stats[n][1]:.3f} | {loo_stats[n][2]:.3f} |")
    for n in use:
        if outliers[n]:
            md.append("")
            lst = sorted(outliers[n], key=lambda x: x[1])[:8]
            more = len(outliers[n]) - len(lst)
            md.append(f"Seed titles of {n} that are no more similar to the others than the background 99th percentile (outliers; the threshold ignores them): " + "; ".join(f"{t} ({l:.3f})" for t, l in lst) + (f"; and {more} more" if more > 0 else ""))
    md += ["", "## Members by threshold", "The last column uses the occupation's own seed-relative threshold = the larger of (the lowest leave-one-out seed similarity, the background 99th percentile); it is the one used for the series.", "",
           "| occupation | seed (regex) | " + " | ".join(f"sim >= {t:.2f}" for t in a.thresholds) + " | seed-relative threshold | members at it |",
           "|---|---|" + "---|" * (len(a.thresholds) + 2)]
    member = {}
    for t in a.thresholds:
        for j, n in enumerate(use):
            member[(n, t)] = seeds[n] | ((near == j) & (best >= t))
    if a.use is not None and a.use not in a.thresholds:
        for j, n in enumerate(use):
            member[(n, a.use)] = seeds[n] | ((near == j) & (best >= a.use))
    for j, n in enumerate(use):
        member[(n, "rel")] = seeds[n] | ((near == j) & (S[:, j] >= rel[n]))
    for n in use:
        md.append(f"| {n} | {int(seeds[n].sum())} | " + " | ".join(str(int(member[(n, t)].sum())) for t in a.thresholds) + f" | {rel[n]:.3f} | {int(member[(n, 'rel')].sum())} |")

    md += ["", "## Members beyond the regex matches, to read for false positives", f"({"seed-relative threshold" if a.use is None else f"threshold {a.use:.2f}"}; the most similar first)", ""]
    for j, n in enumerate(use):
        extra = np.where(member[(n, KEY)] & ~seeds[n])[0]
        extra = extra[np.argsort(-S[extra, j])]
        md += [f"### {n}: {len(extra)} postings beyond the {int(seeds[n].sum())} matching titles", ""]
        cnt = Counter(txt[i] or recs[i].get("desc_start", "")[:60] for i in extra)
        for tt, c in cnt.most_common(a.show):
            md.append(f"- {tt} ({c})")
        md.append("")

    # series
    w_by, day_by = {}, {}
    if a.corpus:
        rows, _ = load_all(a.corpus)
        for r in rows:
            w_by[str(r["item"]["id"])] = r["w"]
            day_by[str(r["item"]["id"])] = r["day"]
    if w_by:
        months = sorted({d[:7] for d in day_by.values()})
        tot = defaultdict(float)
        for i in w_by:
            tot[day_by[i][:7]] += w_by[i]
        md += ["## Monthly weighted share of the board (%s)" % ("seed-relative threshold" if a.use is None else f"threshold {a.use:.2f}"), "",
               "| month | " + " | ".join(use) + " |", "|---|" + "---|" * len(use)]
        num = {n: defaultdict(float) for n in use}
        takn = {n: defaultdict(int) for n in use}
        for n in use:
            for i in np.where(member[(n, KEY)])[0]:
                pid = ids[i]
                if pid in w_by:
                    num[n][day_by[pid][:7]] += w_by[pid]
                    takn[n][day_by[pid][:7]] += 1
        for m in months:
            md.append(f"| {m} | " + " | ".join(f"{100 * num[n][m] / tot[m]:.2f}% ({takn[n][m]})" if tot[m] else "" for n in use) + " |")
        md += ["", "Shares in percent of all weighted postings of the month; the number in brackets is the postings taken. Months with few sampled days (see the coverage table of script 93) are unreliable.", ""]

    # HDBSCAN comparison
    lp = Path(f"data/cluster/labels_{a.board}_{a.input}.jsonl")
    if lp.exists():
        lab = {str(r["id"]): r["cluster"] for r in cp.load_jsonl(str(lp))}
        md += [f"## Where the members fall in the HDBSCAN clustering (input {a.input})", "", "| occupation | members | in noise | largest HDBSCAN clusters (members) |", "|---|---|---|---|"]
        for n in use:
            idx = np.where(member[(n, KEY)])[0]
            c = Counter(lab.get(ids[i], -2) for i in idx)
            noise = c.pop(-1, 0)
            top = ", ".join(f"C{k} ({v})" for k, v in c.most_common(4))
            md.append(f"| {n} | {len(idx)} | {noise} | {top} |")
        md.append("")

    Path("docs").mkdir(exist_ok=True)
    Path("data/cluster").mkdir(parents=True, exist_ok=True)
    Path(f"docs/{OUT}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    with open(f"data/cluster/{OUT}.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["id", "occupation", "similarity", "seed"])
        for j, n in enumerate(use):
            for i in np.where(member[(n, KEY)])[0]:
                wr.writerow([ids[i], n, round(float(S[i, j]), 4), int(seeds[n][i])])
    print("\n".join(md[:30]))
    print(f"docs/{OUT}.md written")


if __name__ == "__main__":
    main()
