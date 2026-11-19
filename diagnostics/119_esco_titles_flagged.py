"""
Flagged postings against the other postings: how close are their titles to an ESCO occupation label?
Uses the per-posting file of script 118 (data/cluster/esco_titles_<board>.csv, no GPU needed) and the Month 3 tag files.
Flag = tag with intensity at or above --min-intensity. Shown for all flagged postings and for each channel.

Run (project root, venv active), lesjeudis:
    python -m diagnostics.119_esco_titles_flagged --board lesjeudis --tags data/tagged/tags_v12_lesjeudis.com_2024-08_2025-04.r71.post.jsonl data/tagged/tags_v12_lesjeudis.com_2025-05_2025-09.r71.post.jsonl
Output: docs/esco_titles_flagged_<board>.md
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np

CH = ["reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"]
INT_RANK = {"low": 0, "medium": 1, "high": 2}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--tags", nargs="+", required=True)
    ap.add_argument("--min-intensity", choices=["low", "medium", "high"], default="medium")
    ap.add_argument("--high", type=float, default=0.92)
    a = ap.parse_args()
    flag = {}
    for p in a.tags:
        if not Path(p).exists():
            raise SystemExit(f"tags file not found: {p}")
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                if r.get("ok") and r.get("channel") in CH and INT_RANK.get(r.get("intensity") or "", -1) >= INT_RANK[a.min_intensity]:
                    flag[str(r["posting_id"])] = r["channel"]
    rows = list(csv.DictReader(open(f"data/cluster/esco_titles_{a.board}.csv", encoding="utf-8")))
    g = lambda rs: (len(rs), np.median([float(r["best_cosine"]) for r in rs]) if rs else float("nan"),
                    100 * np.mean([float(r["best_cosine"]) >= a.high for r in rs]) if rs else float("nan"),
                    100 * np.mean([int(r["exact"]) for r in rs]) if rs else float("nan"))
    md = [f"# Flagged and other postings against ESCO labels: {a.board}", "",
          f"Flag = tag intensity {a.min_intensity} or higher. Postings with a title. Cut-off high = {a.high}.", "",
          "| group | postings | median cosine | share ≥ high | exact label match |", "|---|---|---|---|---|"]
    def add(name, rs):
        n, m, h, e = g(rs); md.append(f"| {name} | {n:,} | {m:.3f} | {h:.0f}% | {e:.0f}% |")
    add("all", rows)
    add("flagged", [r for r in rows if r["id"] in flag])
    add("other", [r for r in rows if r["id"] not in flag])
    for ch in CH:
        rs = [r for r in rows if flag.get(r["id"]) == ch]
        if rs:
            add(f"flagged: {ch}", rs)
    Path("docs").mkdir(exist_ok=True)
    out = f"docs/esco_titles_flagged_{a.board}.md"
    Path(out).write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md)); print(out, "written")


if __name__ == "__main__":
    main()
