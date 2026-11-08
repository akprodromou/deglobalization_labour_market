"""
Month 3: list the critical-materials tags that script 71 changed to none, for reading (and labelling).

Script 71 removes a `critical materials` tag unless a matched term is tied to the EU lists. A removed tag becomes none, not
reshoring, so battery-production postings among them (terms `northvolt`, `battery manufacturing`) may belong to
reshoring under the fixed-sector rule. This script writes one row per removed tag, with the title, the matched terms, the
model's evidence and the first 900 characters of the posting text, and two empty columns (channel, intensity) to fill in.

Run (project root):
    python -m diagnostics.86_review_removed_cm --tags data/tagged/tags_v12_jobbland.r71.post.jsonl \\
        --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl \\
                 data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl
Writes data/tagging/cm_removed_review.csv (all removed tags; --only northvolt "battery manufacturing" keeps the rows with those terms).
Fill `channel` (reshoring, critical materials, energy security, defense, trade compliance, diversification, none) and `intensity`.
"""
import argparse
import csv
import json
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus, posting_text
except ImportError:
    from corpus_io import load_corpus, posting_text


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--tags", required=True)
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--only", nargs="*", default=[], help="keep rows whose terms include one of these")
    ap.add_argument("--out", default="data/tagging/cm_removed_review.csv")
    a = ap.parse_args()
    removed = {}
    for line in open(a.tags, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("rule") == "no_eu_anchored_term":
            if a.only and not (set(r.get("terms") or []) & set(a.only)):
                continue
            removed[str(r["posting_id"])] = r
    text = {}
    for p in a.corpus:
        rows, _ = load_corpus(Path(p))
        for x in rows:
            pid = str(x["item"]["id"])
            if pid in removed:
                text[pid] = (x["item"].get("title") or "", posting_text(x["item"], 900))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["posting_id", "title", "terms", "model_intensity", "evidence", "text_excerpt", "channel", "intensity"])
        for pid, r in removed.items():
            t, tx = text.get(pid, ("", ""))
            w.writerow([pid, t, "; ".join(r.get("terms") or []), r.get("model_intensity"), r.get("evidence"), tx.replace("\n", " "), "", ""])
    print(f"{len(removed)} removed tags written to {a.out} ({len(text)} with text)")


if __name__ == "__main__":
    main()
