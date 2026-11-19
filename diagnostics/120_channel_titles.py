"""
Titles of the flagged postings of one channel with their best ESCO label (uses data/cluster/esco_titles_<board>.csv of script 118).
Lists the most frequent titles and then all postings from the lowest cosine upwards (--max rows).

Run (project root, venv active), lesjeudis:
    python -m diagnostics.120_channel_titles --board lesjeudis --channel "trade compliance" --tags data/tagged/tags_v12_lesjeudis.com_2024-08_2025-04.r71.post.jsonl data/tagged/tags_v12_lesjeudis.com_2025-05_2025-09.r71.post.jsonl
Output: docs/channel_titles_<board>_<channel>.md
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

CH = ["reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"]
INT_RANK = {"low": 0, "medium": 1, "high": 2}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--channel", required=True, choices=CH)
    ap.add_argument("--tags", nargs="+", required=True)
    ap.add_argument("--min-intensity", choices=["low", "medium", "high"], default="medium")
    ap.add_argument("--max", type=int, default=120)
    a = ap.parse_args()
    sel = {}
    for p in a.tags:
        if not Path(p).exists():
            raise SystemExit(f"tags file not found: {p}")
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                if r.get("ok") and r.get("channel") == a.channel and INT_RANK.get(r.get("intensity") or "", -1) >= INT_RANK[a.min_intensity]:
                    sel[str(r["posting_id"])] = r.get("intensity")
    rows = [r for r in csv.DictReader(open(f"data/cluster/esco_titles_{a.board}.csv", encoding="utf-8")) if r["id"] in sel]
    rows.sort(key=lambda r: float(r["best_cosine"]))
    cnt = Counter(r["title"].strip().lower() for r in rows)
    md = [f"# Flagged postings of the channel '{a.channel}': {a.board}", "",
          f"{len(rows)} postings with a title (tag intensity {a.min_intensity} or higher), {len(cnt)} distinct titles. Cluster = cluster of the baseline run (-1 noise).", "",
          "## Most frequent titles", ""] + [f"- {t} ({n})" for t, n in cnt.most_common(25)] + ["",
          f"## Postings from the lowest cosine upwards (first {a.max})", "", "| cosine | title | best ESCO label | cluster | intensity |", "|---|---|---|---|---|"]
    for r in rows[:a.max]:
        md.append(f"| {float(r['best_cosine']):.3f} | {r['title'].strip()[:90]} | {r['best_label'][:50]} | {r['cluster']} | {sel[r['id']]} |")
    Path("docs").mkdir(exist_ok=True)
    out = f"docs/channel_titles_{a.board}_{a.channel.replace(' ', '_')}.md"
    Path(out).write_text("\n".join(md) + "\n", encoding="utf-8")
    print(out, "written")


if __name__ == "__main__":
    main()
