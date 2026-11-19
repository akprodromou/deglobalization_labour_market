"""
Where do the postings of a small cluster of one clustering setting sit in the baseline run (40/10)? A cluster whose postings all come from one baseline
cluster is a split of it; postings from noise were not clustered at the baseline; postings spread over several baseline clusters are a new grouping.

Run (project root, venv active), lesjeudis 20/10:
    python -m diagnostics.117_grid_origin --board lesjeudis --grid-labels data/cluster/grid/lesjeudis_mcs20_ms10_labels_lesjeudis_A.jsonl --clusters 253 183 219 224 76
Output: docs/grid_origin_<board>.md
"""
import argparse
import json
from collections import Counter
from pathlib import Path


def lab(p):
    return {str(json.loads(l)["id"]): int(json.loads(l)["cluster"]) for l in open(p, encoding="utf-8") if l.strip()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--grid-labels", required=True)
    ap.add_argument("--baseline")
    ap.add_argument("--clusters", type=int, nargs="+", required=True)
    a = ap.parse_args()
    g = lab(a.grid_labels)
    b = lab(a.baseline or f"data/cluster/labels_{a.board}_A.jsonl")
    bsize = Counter(b.values())
    md = [f"# Origin of small clusters in the baseline run: {a.board}", "",
          f"Grid labels: `{a.grid_labels}`. For each cluster, the baseline clusters (40/10) that hold its postings (baseline id, postings, size of that baseline cluster); -1 is noise at the baseline.", "",
          "| grid cluster | postings | baseline clusters holding them (id: postings of this cluster / size of the baseline cluster) |", "|---|---|---|"]
    for c in a.clusters:
        ids = [i for i, x in g.items() if x == c]
        cnt = Counter(b.get(i, -1) for i in ids)
        md.append(f"| {c} | {len(ids)} | " + "; ".join(f"{k}: {v}" + (f" / {bsize[k]}" if k >= 0 else "") for k, v in cnt.most_common(5)) + " |")
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/grid_origin_{a.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
