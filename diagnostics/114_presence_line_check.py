"""
How many clusters can reach the presence line in some quarter? For each board: the collected-postings equivalent of the share line per quarter,
and the number of clusters whose peak share (or peak weighted volume) in a quarter with enough sampled days reaches each candidate line.
Reads data/cluster/series_<board>_A.csv (script 93). Cluster -1 (noise) is left out. Output: docs/presence_line_<board>.md

Run (project root, venv active):
    python -m diagnostics.114_presence_line_check --board lesjeudis
"""
import argparse
import csv
import statistics
from collections import defaultdict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--min-days", type=int, default=20)
    ap.add_argument("--series", default=None, help="series file; default data/cluster/series_<board>_<input>.csv")
    a = ap.parse_args()
    path = a.series or f"data/cluster/series_{a.board}_{a.input}.csv"
    allrows = [r for r in csv.DictReader(open(path, encoding="utf-8")) if int(r["days"]) >= a.min_days]
    tot_taken, tot_w = defaultdict(float), defaultdict(float)
    for r in allrows:   # all clusters incl. noise = the whole board in that quarter
        tot_taken[r["quarter"]] += float(r["taken"])
        if float(r["share"]) > 0:
            tot_w[r["quarter"]] = max(tot_w[r["quarter"]], float(r["weighted_adjusted"]) / float(r["share"]))
    rows = [r for r in allrows if r["cluster"] != "-1"]
    tk, mx_sh, mx_w = defaultdict(float), defaultdict(float), defaultdict(float)
    for r in rows:
        c = r["cluster"]
        tk[c] += float(r["taken"])
        mx_sh[c] = max(mx_sh[c], float(r["share"]))
        mx_w[c] = max(mx_w[c], float(r["weighted_adjusted"]))
    n = len(tk)
    md = [f"# Presence line check: {a.board}, input {a.input}", "",
          f"Quarters with at least {a.min_days} sampled days. {n} clusters (noise left out).", "",
          "## What the 0.1% line means in postings, per quarter", "",
          "| quarter | board postings taken | board weighted postings | 0.1% in postings taken | 0.1% in weighted postings |", "|---|---|---|---|---|"]
    for q in sorted(tot_taken):
        md.append(f"| {q} | {tot_taken[q]:.0f} | {tot_w[q]:.0f} | {0.001 * tot_taken[q]:.1f} | {0.001 * tot_w[q]:.0f} |")
    md += ["", "## Clusters that reach a line in at least one quarter", "", "| line | clusters reaching it | of |", "|---|---|---|"]
    for lab, f in [("share 0.05%", lambda c: mx_sh[c] >= 0.0005), ("share 0.1%", lambda c: mx_sh[c] >= 0.001),
                   ("share 0.2%", lambda c: mx_sh[c] >= 0.002), ("share 0.5%", lambda c: mx_sh[c] >= 0.005),
                   ("weighted 40", lambda c: mx_w[c] >= 40), ("weighted 100", lambda c: mx_w[c] >= 100)]:
        md.append(f"| {lab} | {sum(f(c) for c in tk)} | {n} |")
    q1, q2, q3 = statistics.quantiles(mx_sh.values(), n=4)
    md += ["", f"Peak share of a cluster in a quarter: minimum {100 * min(mx_sh.values()):.2f}%, quartiles {100 * q1:.2f}%, {100 * q2:.2f}%, {100 * q3:.2f}%, maximum {100 * max(mx_sh.values()):.2f}%.",
           f"Postings taken per cluster over the whole period: minimum {min(tk.values()):.0f}, median {statistics.median(tk.values()):.0f}, maximum {max(tk.values()):.0f}."]
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/presence_line_{a.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
