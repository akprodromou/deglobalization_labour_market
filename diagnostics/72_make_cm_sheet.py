"""
Month 3: a fresh human sample for the critical-materials channel under the EU definition.

Why. The 20 critical-materials postings annotated in round 1 were labelled under the old
definition (LKAB and Boliden counted), so the channel has no valid score. This script draws a
new sheet from the postings that carry a critical-materials term of lexicon v2.

Population: every lexicon-flagged posting with at least one term whose channel is
"critical materials" (batteries, battery storage, mining and mineral, lithium, precious metals,
strategic resource, raw materials security, critical raw materials, battery recycling,
rare earths, battery materials, critical metals).
Strata:
    anchored   postings with an EU-anchored term (the same list as script 71): all of them are taken
    other      the rest (mostly "batteries" and "battery storage"): a random --other of them,
               weighted back to the stratum size
The sheet does not show any model's tag. The key (hidden) holds stratum, weight and terms in the
format of script 60, so the sheet is scored the same way.

Label (columns channel / intensity / note, as in the annotation guide):
    critical materials  only when the posting is about the supply, sourcing, extraction, processing or
                        recycling of materials on the lists of Regulation (EU) 2024/1252 (strategic and
                        critical raw materials; platinum-group metals count, gold and silver do not;
                        steel and general mining do not)
    another channel or none otherwise; unclear when the text does not decide it

Run (project root; the corpus files are read as one corpus):
    python -m diagnostics.72_make_cm_sheet --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl --flagged data/tagged/flagged_corpus_jobbland.se_2024-01_2026-09_lexv2.jsonl --lexicon lexicon/lexicon.csv

Score it afterwards (script 60, own copy of the results file):
    python -m diagnostics.60_score_tagging --sheet data/tagging_cm/annotation_sheet_cm.csv --key data/tagging_cm/annotation_key.jsonl --tags data/tagged/tags_qwen2.5_7b_tagging_v9r.jsonl --pass2 data/tagging_cm/none.csv
    cp docs/tagging_results.md docs/tagging_results_cm.md
(save the completed sheet under the same name; data/tagging_cm is not tracked by git)
"""

import argparse
import csv
import json
import random
import re
import tempfile
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

ANCHORED = {"critical raw materials", "rare earths", "strategic raw materials", "battery materials", "lithium",
            "raw materials security", "critical metals", "strategic resource", "battery recycling"}
TEXT_CHARS = 3000   # as many characters as the tagger reads (script 58, --max-chars)


def sheet_text(desc, matched):
    """First TEXT_CHARS of the description; where a matched term lies beyond that, a 500-character
    passage around it follows after [...] (at most 3), so that the evidence is never cut away."""
    d = re.sub(r"\s+", " ", desc or "").strip()
    body, extra = d[:TEXT_CHARS], []
    for m in matched:
        pos = d.lower().find(m.lower())
        if pos >= TEXT_CHARS - 100:
            extra.append(d[max(0, pos - 250):pos + len(m) + 250])
        if len(extra) == 3:
            break
    if len(d) > TEXT_CHARS:
        body += " [...text continues...]"
    return body + "".join(f" [...] {e}" for e in extra)


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
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--flagged", required=True)
    ap.add_argument("--lexicon", default="lexicon/lexicon.csv")
    ap.add_argument("--other", type=int, default=40, help="postings drawn from the non-anchored stratum")
    ap.add_argument("--seed", type=int, default=20261031)
    ap.add_argument("--out-dir", default="data/tagging_cm")
    args = ap.parse_args()

    channel = {r["term"]: r["channel"] for r in csv.DictReader(open(args.lexicon, encoding="utf-8-sig"))}
    cm_terms = {t for t, c in channel.items() if c == "critical materials"}
    rows, dropped = load_all(args.corpus)
    by_id = {str(r["item"]["id"]): r for r in rows}
    flagged = {}
    for line in open(args.flagged, encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            flagged[str(r["posting_id"])] = r
    pop = [p for p, f in flagged.items() if p in by_id and set(f["terms"]) & cm_terms]
    anchored = [p for p in pop if set(flagged[p]["terms"]) & ANCHORED]
    other = [p for p in pop if p not in set(anchored)]
    rng = random.Random(args.seed)
    take_other = rng.sample(other, min(args.other, len(other)))
    print(f"{len(pop)} flagged postings carry a critical-materials term; anchored: {len(anchored)} (all taken); "
          f"other: {len(other)} (taken {len(take_other)})")

    chosen, keys = [], []
    for stratum, ids, scale in (("anchored", anchored, 1.0),
                                ("other", take_other, len(other) / max(1, len(take_other)))):
        for p in ids:
            r = by_id[p]
            chosen.append(r)
            keys.append({"posting_id": p, "stratum": stratum, "day": r["day"], "weight": r["w"] * scale,
                         "flagged": True, "terms": flagged[p]["terms"]})
    order = list(range(len(chosen)))
    rng.shuffle(order)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "annotation_sheet_cm.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["item", "posting_id", "title", "terms_found", "text", "channel", "intensity", "note"])
        for k, i in enumerate(order, 1):
            it = chosen[i]["item"]
            text = sheet_text(it.get("description"), flagged[str(it["id"])].get("matched", []))
            w.writerow([k, str(it["id"]), (it.get("title") or "").strip(),
                        "; ".join(flagged[str(it["id"])]["terms"]), text, "", "", ""])
    with open(out / "annotation_key.jsonl", "w", encoding="utf-8") as f:
        for k in keys:
            f.write(json.dumps(k, ensure_ascii=False) + "\n")
    (out / "none.csv").write_text("item,posting_id,title,terms_found,text,channel,intensity,note\n", encoding="utf-8")
    print(f"Wrote {out / 'annotation_sheet_cm.csv'} ({len(chosen)} postings), the key and an empty none.csv.")


if __name__ == "__main__":
    main()
