"""
Month 3: review sheet for postings that the lexicon flagged only after a lexicon change (script 77/new terms).

Joins a key file (posting_id, terms), the v12 tags and the corpus, and writes a csv with the title, the first
400 characters of the posting, the matched terms and the tagger's answer, so that each posting can be judged
by eye (employer, customer or technology list?).

Run (project root, venv active):
    python -m diagnostics.81_newflags_review --key annotation_key_newflags.jsonl \
        --tags tags_v12_newflags_lesjeudis.com_2024-08_2025-04.jsonl tags_v12_newflags_lesjeudis.com_2025-05_2025-09.jsonl \
        --corpus data/raw/corpus_lesjeudis.com_2024-08_2025-04.jsonl data/raw/corpus_lesjeudis.com_2025-05_2025-09.jsonl \
        --out docs/newflags_review.csv
"""
import argparse
import csv
import json
import re
import tempfile
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True)
    ap.add_argument("--tags", nargs="+", required=True)
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--out", default="docs/newflags_review.csv")
    ap.add_argument("--head", type=int, default=400)
    a = ap.parse_args()
    key = {}
    for l in open(a.key, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            key[str(r["posting_id"])] = r
    tags = {}
    for p in a.tags:
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                tags[str(r["posting_id"])] = r
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tmp:
        for p in a.corpus:
            for l in open(p, encoding="utf-8"):
                if l.strip():
                    tmp.write(l.rstrip("\n") + "\n")
        name = tmp.name
    rows, _ = load_corpus(name)
    Path(name).unlink()
    texts = {str(r["item"]["id"]): r["item"] for r in rows if str(r["item"]["id"]) in key}
    out = []
    for pid, k in key.items():
        it = texts.get(pid, {})
        t = tags.get(pid, {})
        desc = re.sub(r"\s+", " ", it.get("description") or "")
        out.append({"posting_id": pid, "day": k.get("day", ""), "terms": "|".join(k.get("terms", [])),
                    "title": it.get("title", ""), "head": desc[:a.head],
                    "v12_channel": t.get("channel") if t.get("ok") else "INVALID", "v12_intensity": t.get("intensity"),
                    "v12_evidence": (t.get("evidence") or "")[:200],
                    "human_channel": "", "human_intensity": "", "note": ""})
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"wrote {a.out}: {len(out)} postings, {sum(1 for o in out if o['title'])} found in the corpus")


if __name__ == "__main__":
    main()
