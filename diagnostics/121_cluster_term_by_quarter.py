"""
Does one employer or one wording explain a cluster's postings, and when does it appear? For one cluster, per quarter: postings of the cluster (collected, not weighted),
how many of them match a regular expression in the title or the first 1,500 characters of the description (for example the Swedish Customs Service),
how many postings of the whole board match it, and how many of those are in the cluster. Also lists a few matching titles per quarter.

Run (project root, venv active), jobbland cluster 283, Swedish Customs Service:
    python -m diagnostics.121_cluster_term_by_quarter --board jobbland --cluster 283 --regex "tullverket|swedish customs|customs administration|customs service|tullen" --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl
Output: docs/cluster_term_<board>_<cluster>.md
"""
import argparse
import json
import re
import tempfile
from collections import defaultdict
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus


def load_all(paths):
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


def quarter(day):
    return f"{day[:4]}-Q{(int(day[5:7]) - 1) // 3 + 1}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--cluster", type=int, required=True)
    ap.add_argument("--regex", required=True)
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--labels")
    ap.add_argument("--examples", type=int, default=3)
    a = ap.parse_args()
    rx = re.compile(a.regex, re.I)
    labels_p = a.labels or f"data/cluster/labels_{a.board}_{a.input}.jsonl"
    lab = {}
    for l in open(labels_p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l); lab[str(r["id"])] = int(r["cluster"])
    rows, _dup = load_all(a.corpus)
    Q = defaultdict(lambda: {"board": 0, "cl": 0, "hit_board": 0, "hit_cl": 0, "ex": []})
    for r in rows:
        it = r["item"]; q = quarter(r["day"]); d = Q[q]
        title = (it.get("title") or "").strip()
        hit = bool(rx.search(title) or rx.search((it.get("description") or "")[:1500]))
        incl = lab.get(str(it["id"]), -2) == a.cluster
        d["board"] += 1; d["hit_board"] += hit
        if incl:
            d["cl"] += 1; d["hit_cl"] += hit
            if hit and len(d["ex"]) < a.examples:
                d["ex"].append(title[:80])
    md = [f"# Cluster {a.cluster} of {a.board}: postings matching `{a.regex}` by quarter", "",
          "Collected postings, not weighted. Match = title or first 1,500 characters of the description. Cluster labels from "
          f"`{labels_p}`.", "",
          "| quarter | board postings | board matches | cluster postings | cluster matches | matches in cluster as share of cluster | share of board matches that are in the cluster | examples (cluster matches) |",
          "|---|---|---|---|---|---|---|---|"]
    for q in sorted(Q):
        d = Q[q]
        sh = f"{100 * d['hit_cl'] / d['cl']:.0f}%" if d["cl"] else ""
        sb = f"{100 * d['hit_cl'] / d['hit_board']:.0f}%" if d["hit_board"] else ""
        md.append(f"| {q} | {d['board']:,} | {d['hit_board']:,} | {d['cl']:,} | {d['hit_cl']:,} | {sh} | {sb} | " + "; ".join(d["ex"]) + " |")
    tot_cl = sum(d["cl"] for d in Q.values()); tot_hit = sum(d["hit_cl"] for d in Q.values())
    md += ["", f"Whole period: {tot_cl:,} postings in the cluster, {tot_hit:,} of them match ({100 * tot_hit / max(tot_cl, 1):.0f}%)."]
    Path("docs").mkdir(exist_ok=True)
    out = f"docs/cluster_term_{a.board}_{a.cluster}.md"
    Path(out).write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md)); print(out, "written")


if __name__ == "__main__":
    main()
