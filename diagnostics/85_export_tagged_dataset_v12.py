"""
Month 3 deliverable: the final tagged posting dataset (one CSV row per lexicon-flagged posting, three boards).

Replaces script 76 for the v12 run. It reads, for each board, the tags after the post-tagging rules (script 82,
`*.post.jsonl`) and the corpus files of the board, and joins them by posting id. The matched lexicon terms are read from
the tag line (script 58 stores them there), so no flagged file is needed.

Columns
  board, posting_id, source_id, upload_date, title, organization, location, location_code, experience_level, type,
  matched_terms, channel, subtype, intensity, evidence, weight, prompt, post_rule,
  channel_model, intensity_model, subtype_model, tag_ok
`channel`, `subtype` and `intensity` are the FINAL values (the model's answer after rules R0 to R3). The model's own answer
is kept in the `*_model` columns, and `post_rule` names the rule(s) that changed the tag (R0 to R3 of script 82, `no_eu_anchored_term` of script 71; empty if none). `weight` is the posting's
day total divided by the postings taken that day (all corpus files of a board are read as one corpus, after removal of
exact duplicates, as in script 84); the weights of a board add up to its population of postings. `channel` is `invalid`
when the model's answer could not be read. The description text is not exported (size).
Postings without a lexicon term are not in the file; they count as none in scripts 64 and 84.

Run (project root; quote the patterns so that Python, not the shell, expands them), for example:
    python -m diagnostics.85_export_tagged_dataset_v12 \\
      --board jobbland.se "data/tagged/tags_v12_jobbland.post.jsonl" "data/raw/corpus_jobbland.se_*.jsonl" \\
      --board lesjeudis.com "data/tagged/tags_v12_lesjeudis.com_*.post.jsonl" "data/raw/corpus_lesjeudis.com_*.jsonl" \\
      --board jobs.de "data/tagged/tags_v12_jobs.de_*.post.jsonl" "data/raw/corpus_jobs.de_*.jsonl" \\
      --out deliverables/tagged_postings_v12.csv
"""
import argparse
import csv
import glob
import json
import tempfile
from collections import Counter
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

FIELDS = ["board", "posting_id", "source_id", "upload_date", "title", "organization", "location", "location_code",
          "experience_level", "type", "matched_terms", "channel", "subtype", "intensity", "evidence", "weight",
          "prompt", "post_rule", "channel_model", "intensity_model", "subtype_model", "tag_ok"]


def read_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", nargs=3, action="append", metavar=("NAME", "TAGS_GLOB", "CORPUS_GLOB"), required=True)
    ap.add_argument("--out", default="deliverables/tagged_postings_v12.csv")
    a = ap.parse_args()

    out = []
    for name, tg, cg in a.board:
        tag_files, corpus_files = sorted(glob.glob(tg)), sorted(glob.glob(cg))
        if not tag_files or not corpus_files:
            raise SystemExit(f"{name}: no file for tags '{tg}' ({len(tag_files)}) or corpus '{cg}' ({len(corpus_files)})")
        for p in tag_files:
            if not p.endswith(".post.jsonl"):
                raise SystemExit(f"{name}: {p} is not a .post.jsonl file; run script 82 first")
        tags = {}
        for p in tag_files:
            for t in read_jsonl(p):
                tags[str(t["posting_id"])] = t
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tmp:
            for p in corpus_files:
                for line in open(p, encoding="utf-8"):
                    if line.strip():
                        tmp.write(line.rstrip("\n") + "\n")
        rows, dropped = load_corpus(Path(tmp.name))
        Path(tmp.name).unlink()
        seen, n = set(), 0
        for r in rows:
            it = r["item"]
            pid = str(it["id"])
            t = tags.get(pid)
            if t is None:
                continue
            seen.add(pid)
            n += 1
            ch = t.get("channel") or "invalid"
            out.append({"board": name, "posting_id": pid, "source_id": it.get("source_id"),
                        "upload_date": it.get("upload_date") or r["day"], "title": (it.get("title") or "").strip(),
                        "organization": it.get("organization"), "location": it.get("location"),
                        "location_code": it.get("location_code"), "experience_level": it.get("experience_level"),
                        "type": it.get("type"), "matched_terms": "; ".join(t.get("terms") or []),
                        "channel": ch, "subtype": t.get("subtype") or "", "intensity": t.get("intensity") or "",
                        "evidence": t.get("evidence"), "weight": round(r["w"], 4), "prompt": t.get("prompt"),
                        "post_rule": "; ".join(x for x in (t.get("post_rule"), t.get("rule")) if x),
                        "channel_model": t.get("channel_model", t.get("model_channel", ch)),
                        "intensity_model": t.get("intensity_model", t.get("model_intensity", t.get("intensity") or "")),
                        "subtype_model": t.get("subtype_model", t.get("subtype") or ""), "tag_ok": t.get("ok")})
        print(f"{name}: {len(tags):,} tags, {n:,} joined to the corpus ({len(tags) - len(seen):,} tags without a corpus posting, "
              f"{dropped:,} duplicate postings dropped in the corpus)")
    out.sort(key=lambda x: (x["board"], x["upload_date"] or "", x["posting_id"]))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out)
    print(f"written {len(out):,} rows to {a.out}")
    for b in sorted({x["board"] for x in out}):
        c = Counter(x["channel"] for x in out if x["board"] == b)
        print(f"  {b}: {dict(c.most_common())}")
    changed = sum(1 for x in out if x["post_rule"])
    print(f"tags changed by a post-tagging rule: {changed:,}")
    bad = sum(1 for x in out if x["channel"] == "invalid")
    if bad:
        print(f"WARNING: {bad} rows have an invalid model answer; they count as none in scripts 64 and 84.")


if __name__ == "__main__":
    main()
