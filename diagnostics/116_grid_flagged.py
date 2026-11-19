"""
Compare clustering settings by what they do with the flagged postings (Month 3 tags) instead of the seven named occupations. The flagged postings are
hundreds per board, so the comparison is not decided by a few postings. For each labels file:
  - flagged postings in a cluster (not in noise), as a share of all flagged postings;
  - clusters with at least --min-flagged flagged postings and a flagged share of at least --min-share ("flagged clusters"), their number and the share of
    all flagged postings they hold;
  - the five clusters with the largest flagged share (at least --min-flagged flagged postings): size, flagged share.
Counts are postings taken (not weighted). Flag = tag ok, a channel of script 93 and intensity at or above --min-intensity.

Run (project root, venv active), lesjeudis; the grid labels are the files copied from Drive to data/cluster/grid/:
    python -m diagnostics.116_grid_flagged --board lesjeudis --tags data/tagged/tags_v12_lesjeudis.com_2024-08_2025-04.r71.post.jsonl data/tagged/tags_v12_lesjeudis.com_2025-05_2025-09.r71.post.jsonl --min-intensity medium
"""
import argparse
import glob
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


CH = ["reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"]   # as in script 93
INT_RANK = {"low": 0, "medium": 1, "high": 2}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--tags", nargs="+", required=True)
    ap.add_argument("--min-intensity", choices=["low", "medium", "high"], default="medium")
    ap.add_argument("--baseline", help="default data/cluster/labels_<board>_A.jsonl")
    ap.add_argument("--grid-dir", default="data/cluster/grid")
    ap.add_argument("--min-flagged", type=int, default=10)
    ap.add_argument("--min-share", type=float, default=0.30)
    a = ap.parse_args()
    RANK = INT_RANK
    flag = {}
    for p in a.tags:
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                if r.get("ok") and r.get("channel") in CH and RANK.get(r.get("intensity") or "low", 0) >= RANK[a.min_intensity]:
                    flag[str(r["posting_id"])] = r["channel"]
    files = [("40/10 (baseline)", a.baseline or f"data/cluster/labels_{a.board}_A.jsonl")]
    for p in sorted(glob.glob(f"{a.grid_dir}/{a.board}_mcs*_ms*_labels_{a.board}_A.jsonl")):
        mm = re.search(r"mcs(\d+)_ms(\d+)", p)
        files.append((f"{mm.group(1)}/{mm.group(2)}", p))
    md = [f"# Clustering settings and the flagged postings: {a.board}", "",
          f"Flag = Month 3 tag with intensity {a.min_intensity} or higher; {len(flag):,} flagged postings with a tag. Flagged cluster = at least {a.min_flagged} flagged postings and a flagged share of at least {a.min_share:.0%}. Postings taken, not weighted.", "",
          "| min_cluster_size / min_samples | clusters | flagged postings in a cluster | flagged clusters | flagged postings in flagged clusters | top five clusters by flagged share (size, share) |", "|---|---|---|---|---|---|"]
    for name, path in files:
        if not Path(path).exists():
            continue
        lab = {}
        for l in open(path, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                lab[str(r["id"])] = int(r["cluster"])
        size, fl = Counter(), Counter()
        for i, c in lab.items():
            if c >= 0:
                size[c] += 1
                fl[c] += i in flag
        n_fl = sum(1 for i in lab if i in flag)
        in_cl = sum(fl.values())
        cand = [(c, size[c], fl[c] / size[c]) for c in size if fl[c] >= a.min_flagged]
        fc = [x for x in cand if x[2] >= a.min_share]
        top = sorted(cand, key=lambda x: -x[2])[:5]
        md.append(f"| {name} | {len(size)} | {in_cl} of {n_fl} ({in_cl / n_fl:.0%}) | {len(fc)} | {sum(fl[x[0]] for x in fc)} ({sum(fl[x[0]] for x in fc) / n_fl:.0%}) | " +
                  "; ".join(f"{x[0]} ({x[1]}, {x[2]:.0%})" for x in top) + " |")
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/grid_flagged_{a.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
