"""
Month 3 deliverable: the tagged posting dataset (one CSV row per lexicon-flagged posting, with channel and intensity).

Joins three things by posting id: the flagged set (script 58: matched lexicon terms), the final tags (script 71 output,
tags_..._v9r...) and the corpus (title, date, source, employer, place, weight). Postings without a tag line (not tagged
because the flagged set and the tags are out of step) are listed in the printed warning and left out.

Columns: posting_id, source, upload_date, title, organization, location, location_code, experience_level, type,
         matched_terms, channel, intensity, evidence, weight, model, prompt, rule, model_channel, model_intensity, tag_ok
`weight` = posting's day total / postings taken that day (sum of weights = population of postings); rows where the model's answer could not be read have channel `invalid`. `rule` and the
`model_*` columns are filled where script 71 changed a critical-materials tag to none.
The description text is not exported (size); posting_id and source_id identify the posting in the Tracker data.

Run (project root):
    python -m diagnostics.76_export_tagged_dataset \
        --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl \
                 data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl \
        --flagged data/tagged/flagged_corpus_jobbland.se_2024-01_2026-09_lex154_phd.jsonl \
        --tags data/tagged/tags_qwen2.5_7b_tagging_v9r_lex154_phd.jsonl \
        --out deliverables/tagged_postings_v9.csv
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

FIELDS = ["posting_id", "source", "source_id", "upload_date", "title", "organization", "location", "location_code",
          "experience_level", "type", "matched_terms", "channel", "intensity", "evidence", "weight",
          "model", "prompt", "rule", "model_channel", "model_intensity", "tag_ok"]


def read_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--flagged", required=True)
    ap.add_argument("--tags", required=True)
    ap.add_argument("--out", default="tagged_postings.csv")
    a = ap.parse_args()

    flagged = {str(r["posting_id"]): r for r in read_jsonl(a.flagged)}
    tags = {str(t["posting_id"]): t for t in read_jsonl(a.tags)}
    # one corpus: the files are merged before duplicate removal, as in the tagging run
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tmp:
        for p in a.corpus:
            for line in open(p, encoding="utf-8"):
                if line.strip():
                    tmp.write(line.rstrip("\n") + "\n")
    rows, dropped = load_corpus(Path(tmp.name))
    Path(tmp.name).unlink()

    out, missing_tag = [], 0
    for r in rows:
        it = r["item"]
        pid = str(it["id"])
        fl = flagged.get(pid)
        if fl is None:
            continue
        t = tags.get(pid)
        if t is None:
            missing_tag += 1
            continue
        out.append({"posting_id": pid, "source": it.get("source"), "source_id": it.get("source_id"),
                    "upload_date": it.get("upload_date") or r["day"], "title": (it.get("title") or "").strip(),
                    "organization": it.get("organization"), "location": it.get("location"),
                    "location_code": it.get("location_code"), "experience_level": it.get("experience_level"),
                    "type": it.get("type"), "matched_terms": "; ".join(fl["terms"]),
                    "channel": t.get("channel") or "invalid", "intensity": t.get("intensity") or "", "evidence": t.get("evidence"),
                    "weight": round(r["w"], 4), "model": t.get("model"), "prompt": t.get("prompt"),
                    "rule": t.get("rule"), "model_channel": t.get("model_channel"),
                    "model_intensity": t.get("model_intensity"), "tag_ok": t.get("ok")})
    out.sort(key=lambda x: (x["upload_date"] or "", x["posting_id"]))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)
    c = Counter(x["channel"] for x in out)
    print(f"flagged {len(flagged):,}; written {len(out):,} rows to {a.out} ({missing_tag} flagged postings without a tag, left out)")
    print("by channel:", dict(c.most_common()))
    print("by channel and intensity (channels other than none):")
    ci = Counter((x["channel"], x["intensity"]) for x in out if x["channel"] != "none")
    for k, v in sorted(ci.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        print("  ", k, v)
    bad = sum(1 for x in out if x["channel"] == "invalid")
    if bad:
        print(f"WARNING: {bad} rows have an invalid model answer (tag_ok false); they are labelled `invalid` in the CSV and count as none in scripts 64 and 65.")


if __name__ == "__main__":
    main()
