"""
Month 4: read postings of chosen clusters (what is in a cluster, and is the flag right?)

Prints a random sample of postings from the clusters you name: day, Month 3 channel (or none), title (or "(no title)"), the
first --chars characters of the description. Use it to read the title-less clusters (171 and 168 on jobbland), the candidate
emerging clusters, and to check flag false positives.

Options
    --clusters 171 168          clusters to sample (labels of script 92; -1 is the noise group)
    --n 12                      postings per cluster
    --only-flagged              only postings carrying a Month 3 flag
    --from / --to               day range (YYYY-MM-DD)
    --chars 400                 description characters shown
    --seed 1

Run (project root, venv active), jobbland:
    python -m diagnostics.98_cluster_sample --board jobbland --input A --clusters 171 168 --n 12 --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl --tags data/tagged/tags_v12_jobbland.final.post.jsonl

Output: docs/cluster_sample_<board>_<clusters>.md
"""

import argparse
import json
import random
import re
import tempfile
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

CH = ["reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"]


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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--clusters", nargs="+", type=int, required=True)
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--labels")
    ap.add_argument("--tags", nargs="+")
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--chars", type=int, default=400)
    ap.add_argument("--only-flagged", action="store_true")
    ap.add_argument("--from", dest="d_from", default="0000-00-00")
    ap.add_argument("--to", dest="d_to", default="9999-99-99")
    ap.add_argument("--seed", type=int, default=1)
    a, _ignored = ap.parse_known_args()
    labels_p = a.labels or f"data/cluster/labels_{a.board}_{a.input}.jsonl"
    if not Path(labels_p).exists():
        raise SystemExit(f"labels file not found: {labels_p}")
    lab = {}
    for l in open(labels_p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            lab[str(r["id"])] = int(r["cluster"])
    flag = {}
    for p in a.tags or []:
        if not Path(p).exists():
            raise SystemExit(f"tags file not found: {p}")
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                if r.get("ok") and r.get("channel") in CH:
                    flag[str(r["posting_id"])] = r["channel"]
    rows, dup = load_all(a.corpus)
    rows = [r for r in rows if a.d_from <= r["day"] <= a.d_to]
    rnd = random.Random(a.seed)
    out = [f"# Sample of clusters {a.clusters}: {a.board} input {a.input}\n"]
    for c in a.clusters:
        mine = [r for r in rows if lab.get(str(r["item"]["id"]), -2) == c]
        if a.only_flagged:
            mine = [r for r in mine if str(r["item"]["id"]) in flag]
        nt = sum(not (r["item"].get("title") or "").strip() for r in mine)
        fl = sum(str(r["item"]["id"]) in flag for r in mine)
        out.append(f"## Cluster {c}: {len(mine):,} postings taken, {nt:,} without a title, {fl:,} flagged"
                   + (f", days {min(r['day'] for r in mine)} to {max(r['day'] for r in mine)}" if mine else "") + "\n")
        for r in rnd.sample(mine, min(a.n, len(mine))):
            it = r["item"]
            title = (it.get("title") or "").strip() or "(no title)"
            desc = re.sub(r"\s+", " ", it.get("description") or "").strip()[:a.chars]
            out.append(f"- **{r['day']}** | channel: {flag.get(str(it['id']), 'none')} | id {it['id']} | {title}\n  {desc}\n")
    Path("docs").mkdir(exist_ok=True)
    out_p = f"docs/cluster_sample_{a.board}_{'_'.join(map(str, a.clusters))}.md"
    Path(out_p).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(out_p + " written")


if __name__ == "__main__":
    main()
