"""
Month 4: how common are the ESCO skills and Lightcast terms? Data-based choice of the "too common" cut (D v3).

For ONE board and each block (ESCO skills, Lightcast terms) this script
  1. counts in how many of the board's postings every item appears (document frequency, as a share of all postings,
     the same denominator as --max-df in script 92),
  2. prints how many items exceed 0.5 / 1 / 2 / 5 / 10 % and which share of all item mentions they carry,
  3. proposes two cuts that come from the distribution itself, so no number of our own is needed:
       knee    point where the rank-frequency curve (rank and share on linear axes) bends away from the steep head
               towards the long tail: largest distance to the straight line between first and last point
               (the idea of the Kneedle algorithm, Satopaa et al. 2011; Kavargyris et al. 2025 read the inflection
               point of the skill frequency curve in the same way)
       tukey   upper fence of the boxplot rule on log10(share): Q3 + 1.5 * IQR (Tukey 1977)
     Both are computed on items that appear in at least --min-count postings (5 for ESCO, 3 for Lightcast: the
     items that can enter the tf-idf of script 92 at all); the shares use ALL postings.
  4. writes docs/df_distribution_<board>.md, data/cluster/df_items_<board>_<esco|lightcast>.csv and a figure
     docs/df_rank_frequency_<board>.png (if matplotlib is installed).

Needs no GPU and no embeddings. It reads the same files as script 92:
  data/tagged/titles_<board>.jsonl                          (ids of the board's postings)
  data/tagged/skills_local_full_<board>_t0.60.jsonl         {"id","skills"}
  data/tagged/lightcast_block_<board>.jsonl                 {"id","terms"}  + lexicon/lightcast_block_terms.csv (selected=1)

Run:  python -m diagnostics.125_df_distribution --board lesjeudis
"""

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

THRESHOLDS = (0.005, 0.01, 0.02, 0.05, 0.10)


def load_jsonl(p):
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def knee_index(shares_desc):
    """Index (0-based rank) of the knee of the rank-frequency curve (linear axes, as in Kneedle); items with rank <= index are the head."""
    n = len(shares_desc)
    if n < 5:
        return None
    x = np.arange(1, n + 1, dtype=float)
    y = np.asarray(shares_desc, dtype=float)
    xn = (x - x.min()) / (x.max() - x.min())
    yn = (y - y.min()) / (y.max() - y.min())
    # decreasing convex curve; straight line from (0, 1) to (1, 0); knee = largest gap below the line
    gap = (1 - xn) - yn
    return int(np.argmax(gap))


def tukey_fence(shares):
    ls = np.log10(shares)
    q1, q3 = np.percentile(ls, [25, 75])
    return float(10 ** (q3 + 1.5 * (q3 - q1)))


def analyse(name, docs, n_post, min_count, labels):
    cnt = Counter(t for x in docs for t in set(x))
    total_mentions = sum(cnt.values())
    items = sorted(cnt.items(), key=lambda kv: -kv[1])
    shares_all = np.array([c / n_post for _, c in items])
    res = {"name": name, "n_items": len(items), "mentions": total_mentions, "items": items, "shares": shares_all}
    res["postings_with_any"] = sum(1 for x in docs if x)
    rows = []
    for th in THRESHOLDS:
        above = [(t, c) for t, c in items if c / n_post > th]
        above_set = {t for t, _ in above}
        mention_share = sum(c for _, c in above) / max(1, total_mentions)
        post_hit = sum(1 for x in docs if any(t in above_set for t in x)) if above else 0
        rows.append((th, len(above), len(above) / max(1, len(items)), mention_share, post_hit / n_post))
    res["rows"] = rows
    # cuts on items that can enter the tf-idf
    ent = [(t, c) for t, c in items if c >= min_count]
    res["n_entering"] = len(ent)
    if len(ent) >= 5:
        sh = np.array([c / n_post for _, c in ent])
        k = knee_index(sh)
        res["knee_share"] = float(sh[k])
        res["knee_rank"] = k + 1
        res["tukey_share"] = tukey_fence(sh)
        res["median_share"] = float(np.median(sh))
    else:
        res["knee_share"] = res["tukey_share"] = res["median_share"] = None
    res["labels"] = labels
    return res


def cut_summary(res, n_post, docs, cut):
    above = {t for t, c in res["items"] if c / n_post > cut}
    mentions = sum(c for t, c in res["items"] if t in above) / max(1, res["mentions"])
    lost = sum(1 for x in docs if x and all(t in above for t in x)) / n_post
    return len(above), mentions, lost, above


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", required=True, help="jobbland | lesjeudis | jobsde")
    ap.add_argument("--titles", help="default data/tagged/titles_<board>.jsonl")
    ap.add_argument("--skills", help="default data/tagged/skills_local_full_<board>_t0.60.jsonl")
    ap.add_argument("--lightcast", help="default data/tagged/lightcast_block_<board>.jsonl")
    ap.add_argument("--lc-terms", default="lexicon/lightcast_block_terms.csv")
    ap.add_argument("--esco-csv", default="lexicon/skills.csv", help="id,description : only to print skill names")
    ap.add_argument("--out", default="data/cluster")
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--show", type=int, default=15, help="items listed above each cut")
    args = ap.parse_args()

    titles = args.titles or f"data/tagged/titles_{args.board}.jsonl"
    skills = args.skills or f"data/tagged/skills_local_full_{args.board}_t0.60.jsonl"
    lcf = args.lightcast or f"data/tagged/lightcast_block_{args.board}.jsonl"
    ids = [r["id"] for r in load_jsonl(titles)]
    n_post = len(ids)
    print(f"{args.board}: {n_post:,} postings")

    esco_label = {}
    if Path(args.esco_csv).exists():
        with open(args.esco_csv, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                esco_label[r["id"]] = r.get("description", "")[:50]
    sk = {r["id"]: r["skills"] for r in load_jsonl(skills)}
    keep = set()
    with open(args.lc_terms, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if str(r.get("selected", "")).strip() == "1":
                keep.add(r["term"])
    lc = {r["id"]: [t for t in r["terms"] if t in keep] for r in load_jsonl(lcf)}

    blocks = (("esco", [sk.get(i, []) for i in ids], 5, esco_label),
              ("lightcast", [lc.get(i, []) for i in ids], 3, {}))
    Path(args.docs).mkdir(parents=True, exist_ok=True)
    Path(args.out).mkdir(parents=True, exist_ok=True)

    md = [f"# Document frequency of skills and terms: {args.board}", "",
          f"{n_post:,} postings. Share = postings with the item / all postings of the board (the denominator of `--max-df` in script 92).", ""]
    results = []
    for name, docs, min_count, lab in blocks:
        r = analyse(name, docs, n_post, min_count, lab)
        results.append((r, docs))
        with open(f"{args.out}/df_items_{args.board}_{name}.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["item", "label", "postings", "share"])
            for t, c in r["items"]:
                w.writerow([t, lab.get(t, ""), c, f"{c / n_post:.5f}"])
        md.append(f"## {name}: {r['n_items']:,} distinct items, {r['mentions']:,} mentions, "
                  f"{r['postings_with_any']:,} postings with at least one item ({r['postings_with_any'] / n_post:.1%})")
        md.append("")
        md.append(f"Median share of an item that appears in at least {min_count} postings ({r['n_entering']:,} items): "
                  + (f"{r['median_share']:.3%}" if r['median_share'] is not None else "n/a"))
        md.append("")
        md.append("| share of postings above | items | share of items | share of all mentions | postings with at least one such item |")
        md.append("|---|---|---|---|---|")
        for th, n, si, sm, sp in r["rows"]:
            md.append(f"| {th:.1%} | {n:,} | {si:.1%} | {sm:.1%} | {sp:.1%} |")
        md.append("")
        if r["knee_share"] is None:
            md.append("Too few items to find a knee or a fence.\n")
            continue
        md.append("| rule | cut (share of postings) | items above | share of all mentions | postings left with no item |")
        md.append("|---|---|---|---|---|")
        cuts = {}
        for label, cut in (("knee of the rank-frequency curve", r["knee_share"]),
                           ("Tukey upper fence (Q3 + 1.5 IQR of log share)", r["tukey_share"]),
                           ("current choice (5%)", 0.05)):
            n, m, lost, above = cut_summary(r, n_post, docs, cut)
            cuts[label] = above
            md.append(f"| {label} | {cut:.3%} | {n:,} | {m:.1%} | {lost:.1%} |")
        md.append("")
        md.append(f"The knee is at rank {r['knee_rank']:,} of {r['n_entering']:,} items.")
        md.append("")
        for label, above in cuts.items():
            top = [(t, c) for t, c in r["items"] if t in above][: args.show]
            if not top:
                continue
            md.append(f"Most common items removed by: {label}")
            md.append("")
            for t, c in top:
                md.append(f"- {lab.get(t, t)[:60]} ({c / n_post:.1%})")
            md.append("")
    Path(f"{args.docs}/df_distribution_{args.board}.md").write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {args.docs}/df_distribution_{args.board}.md")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
        for ax, (r, _) in zip(axes, results):
            sh = r["shares"]
            ax.loglog(np.arange(1, len(sh) + 1), sh, lw=1.4, color="#2f5d8a")
            ax.axhline(0.05, color="#999", ls=":", lw=1, label="5%")
            if r["knee_share"] is not None:
                ax.axhline(r["knee_share"], color="#c0392b", ls="--", lw=1, label=f"knee {r['knee_share']:.2%}")
                ax.axhline(r["tukey_share"], color="#27ae60", ls="-.", lw=1, label=f"Tukey {r['tukey_share']:.2%}")
            ax.set_title(f"{args.board}: {r['name']}")
            ax.set_xlabel("rank of the item")
            ax.set_ylabel("share of postings")
            ax.legend(frameon=False, fontsize=8)
        fig.tight_layout()
        fig.savefig(f"{args.docs}/df_rank_frequency_{args.board}.png")
        print(f"wrote {args.docs}/df_rank_frequency_{args.board}.png")
    except Exception as ex:  # figure is optional
        print("no figure:", ex)


if __name__ == "__main__":
    main()
