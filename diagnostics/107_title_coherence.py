"""
Month 4: how title-coherent are the clusters of input A and of input D v2? (decision aid before the clustering setup is fixed)

Why: D v2 has fewer noise postings and stable seeds, but several of its clusters are held together by one skill or by company
text, with unrelated titles inside (jobbland C192, C54, C149; lesjeudis C69, C73, C70). This script puts a number on it.

For every cluster of every input (clusters only, noise left out):
  coherence  = length of the mean of the unit-length title embeddings of its postings, after centring the embeddings on the board mean
               (the same measure as the coherence filter in script 92; centring matters because e5 scores any two titles ~0.8-0.9).
               1 = identical titles, 0 = unrelated titles.
  lift       = coherence minus the coherence of random sets of the same size (5 draws). Removes the effect of cluster size.
  top-token  = share of the cluster's titles that contain its most frequent title word (3+ letters): a check that does not use the
               embedding at all (A is built from the title embedding, so A has an advantage on coherence by construction; the token share
               is the fairer second look).
Summary per input: clusters, noise, median and quartiles of the lift (clusters, and weighted by posting), share of clustered postings in
clusters whose lift is below the 10th percentile of A's clusters (the "weak" cutoff, fixed on A so both inputs use the same bar).
Also lists the weakest clusters of each input with sample titles and, if --skills is given, the most common ESCO skill and its share.

Needs on the Mac (copy from Colab/Drive, same files as script 106 uses):
  data/cluster/emb_<board>.npy                  (title embeddings, same order as the titles file)
  data/cluster/labels_<board>_A.jsonl           (script 92; Dv2: labels_<board>_Dv2.jsonl)
  data/tagged/titles_<board>.jsonl              (jobbland: titles_jobbland_inf.jsonl)
Output: docs/title_coherence_<board>.md and data/cluster/title_coherence_<board>.csv
Run:  python -m diagnostics.107_title_coherence --board lesjeudis
Test: python -m diagnostics.107_title_coherence --board lesjeudis --mock --limit 3000
"""

import argparse
import csv
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np


def load92():
    p = Path(__file__).with_name("92_cluster_postings.py")
    spec = importlib.util.spec_from_file_location("cp92", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def coherence(v):
    return float(np.linalg.norm(v.mean(axis=0)))


def tokens(t):
    return set(re.findall(r"[^\W\d_]{3,}", t.lower()))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--inputs", nargs="+", default=["A", "Dv2"], help="label files labels_<board>_<name>.jsonl; the first one fixes the weak cutoff")
    ap.add_argument("--titles")
    ap.add_argument("--emb")
    ap.add_argument("--labels-dir", default="data/cluster")
    ap.add_argument("--skills", help="optional: data/tagged/skills_local_full_<corpus>_t0.60.jsonl, to print the top ESCO skill of weak clusters")
    ap.add_argument("--esco-csv", default="lexicon/skills.csv")
    ap.add_argument("--out", default="data/cluster")
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--weak-pct", type=float, default=10.0, help="percentile of the first input's cluster lifts used as the weak cutoff")
    ap.add_argument("--show", type=int, default=12)
    ap.add_argument("--draws", type=int, default=5)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--mock", action="store_true")
    args = ap.parse_args()

    cp = load92()
    titles = args.titles or f"data/tagged/titles_{args.board}.jsonl"
    recs = cp.load_jsonl(titles)
    if args.limit:
        recs = recs[: args.limit]
    ids = [r["id"] for r in recs]
    txt = [cp.text_a(r) for r in recs]
    if args.mock:
        e = cp.embed_titles(txt, "", None, True)
    else:
        ep = Path(args.emb or f"{args.out}/emb_{args.board}.npy")
        if not ep.exists():
            sys.exit(f"missing {ep}: copy emb_{args.board}.npy from Colab/Drive into data/cluster/ (this script never embeds)")
        e = np.load(ep)
        if len(e) < len(recs):
            sys.exit(f"{ep} has {len(e):,} rows but the titles file has {len(recs):,} postings: wrong titles file? (jobbland needs --titles data/tagged/titles_jobbland_inf.jsonl)")
        e = e[: len(recs)]
    c = e - e.mean(axis=0, keepdims=True)
    c = c / np.maximum(np.linalg.norm(c, axis=1, keepdims=True), 1e-9)
    rng = np.random.default_rng(args.seed)
    n_all = len(c)

    esco_label = {}
    if Path(args.esco_csv).exists():
        with open(args.esco_csv, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                esco_label[r["id"]] = r.get("description", "")[:40]
    sk = {}
    if args.skills and Path(args.skills).exists():
        sk = {r["id"]: r["skills"] for r in cp.load_jsonl(args.skills)}

    rand_cache = {}

    def random_coh(n):
        if n not in rand_cache:
            rand_cache[n] = float(np.mean([coherence(c[rng.choice(n_all, n, replace=False)]) for _ in range(args.draws)]))
        return rand_cache[n]

    per_input = {}
    rows = []
    for name in args.inputs:
        p = Path(args.labels_dir) / f"labels_{args.board}_{name}.jsonl"
        if not p.exists():
            sys.exit(f"missing {p}")
        by_id = {r["id"]: r["cluster"] for r in cp.load_jsonl(p)}
        lab = np.array([by_id.get(i, -1) for i in ids])
        clusters = []
        for k in sorted(set(lab.tolist()) - {-1}):
            idx = np.where(lab == k)[0]
            if len(idx) < 5:
                continue
            coh = coherence(c[idx])
            lift = coh - random_coh(len(idx))
            tk = [tokens(txt[i]) for i in idx]
            cnt = Counter(t for s in tk for t in s)
            top_tok, top_n = (cnt.most_common(1)[0] if cnt else ("", 0))
            top_skill, top_share = "", 0.0
            if sk:
                sc = Counter(s for i in idx for s in set(sk.get(ids[i], [])))
                if sc:
                    s0, n0 = sc.most_common(1)[0]
                    top_skill, top_share = esco_label.get(s0, s0), n0 / len(idx)
            d = {"input": name, "cluster": int(k), "size": len(idx), "coherence": coh, "lift": lift,
                 "top_token": top_tok, "top_token_share": top_n / len(idx), "top_skill": top_skill, "top_skill_share": top_share,
                 "sample": " | ".join(txt[i][:45] for i in rng.choice(idx, min(5, len(idx)), replace=False))}
            clusters.append(d)
            rows.append(d)
        per_input[name] = (lab, clusters)
        print(f"[{name}] {len(clusters)} clusters, median lift {np.median([d['lift'] for d in clusters]):.3f}")

    first = args.inputs[0]
    cutoff = float(np.percentile([d["lift"] for d in per_input[first][1]], args.weak_pct))

    def q(a, p):
        return float(np.percentile(a, p)) if len(a) else float("nan")

    md = [f"# Title coherence of the clusters: {args.board}", "",
          f"{n_all:,} postings. Coherence = length of the mean of the centred, unit title embeddings of a cluster (1 = identical titles, 0 = unrelated); "
          "lift = coherence minus that of random sets of the same size; top-token share = share of the cluster's titles holding its most frequent title word. "
          f"The weak cutoff is the {args.weak_pct:.0f}th percentile of the lift of the clusters of {first} ({cutoff:.3f}), the same bar for every input. "
          f"Input {first} is built from the title embedding alone, so it has an advantage on coherence by construction; read the top-token share next to it.", "",
          "| input | clusters | noise | lift Q1 / median / Q3 | lift, median per posting | top-token share, median | clusters below the weak cutoff | postings in them (of clustered) |",
          "|---|---|---|---|---|---|---|---|"]
    for name in args.inputs:
        lab, cl = per_input[name]
        lifts = np.array([d["lift"] for d in cl])
        sizes = np.array([d["size"] for d in cl])
        order = np.argsort(lifts)
        cum = np.cumsum(sizes[order]) / sizes.sum()
        wmed = float(lifts[order][np.searchsorted(cum, 0.5)])
        weak = lifts < cutoff
        md.append(f"| {name} | {len(cl)} | {(lab < 0).mean():.1%} | {q(lifts, 25):.3f} / {q(lifts, 50):.3f} / {q(lifts, 75):.3f} | {wmed:.3f} | "
                  f"{np.median([d['top_token_share'] for d in cl]):.0%} | {weak.sum()} ({weak.mean():.0%}) | {sizes[weak].sum():,} ({sizes[weak].sum() / sizes.sum():.0%}) |")
    # same postings in both inputs
    if len(args.inputs) > 1:
        both = np.all([per_input[n][0] >= 0 for n in args.inputs], axis=0)
        md += ["", f"Postings clustered in every input: {both.sum():,} ({both.mean():.1%} of all)."]
        from sklearn.metrics import adjusted_rand_score
        a0 = per_input[args.inputs[0]][0]
        for name in args.inputs[1:]:
            ok = (a0 >= 0) & (per_input[name][0] >= 0)
            if ok.sum() > 10:
                md.append(f"Agreement of {args.inputs[0]} and {name} on the {ok.sum():,} postings clustered in both: ARI {adjusted_rand_score(a0[ok], per_input[name][0][ok]):.3f} "
                          "(1 = same partition; a value near 0.3 to 0.5 means the inputs group the postings quite differently).")
    for name in args.inputs:
        cl = sorted(per_input[name][1], key=lambda d: d["lift"])[: args.show]
        md += ["", f"## Weakest {len(cl)} clusters of {name}", "",
               "| cluster | size | lift | top token (share) | top ESCO skill (share) | sample titles |", "|---|---|---|---|---|---|"]
        for d in cl:
            md.append(f"| {d['cluster']} | {d['size']} | {d['lift']:.3f} | {d['top_token']} ({d['top_token_share']:.0%}) | "
                      f"{d['top_skill']} ({d['top_skill_share']:.0%}) | {d['sample'].replace('|', '/')} |")
    md += ["", "Reading notes", "",
           "- A cluster far below the cutoff has titles that have little in common: it is held together by something else (a skill, company text, a template).",
           "- A high top-skill share next to a weak lift is the single-skill pattern seen in D v1; a high top-token share next to a good lift is an ordinary occupation cluster.",
           "- The lift compares clusters of different input spaces on the same scale (the title embedding); it does not say that one input finds more emerging occupations."]
    Path(args.docs).mkdir(parents=True, exist_ok=True)
    Path(args.out).mkdir(parents=True, exist_ok=True)
    Path(f"{args.docs}/title_coherence_{args.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    with open(f"{args.out}/title_coherence_{args.board}.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    print(f"wrote {args.docs}/title_coherence_{args.board}.md")


if __name__ == "__main__":
    main()
