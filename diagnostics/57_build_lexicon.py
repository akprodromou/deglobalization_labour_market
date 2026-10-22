"""
Month 3, step 2c: build the final lexicon from the seed list and the reviewed sheets.

Reads
    lexicon/seed_lexicon.csv                  seed terms (kept as they are)
    data/lexicon/candidates_tfidf.csv         reviewed: keep = 1, channel = ...
    data/lexicon/candidates_embedding.csv     reviewed: keep = 1, channel_assigned = ...
and writes
    lexicon/lexicon.csv      term, channel, lang, variants, from_brief, source, note
    docs/lexicon_summary.md  terms per channel and per source, checks

Checks (printed and written to the summary): a kept candidate without a valid
channel is refused; duplicate terms (after lower-casing and replacing hyphens
by spaces) are merged; the total is compared with the 300 to 500 terms the
brief asks for and a warning is printed if it is outside that range. The
lexicon file holds terms only, no posting text, so it can be committed.

Run (project root):
    python -m diagnostics.57_build_lexicon
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

CHANNELS = {"reshoring", "defense", "critical materials", "energy security",
            "trade compliance", "diversification"}
SEEDS = Path("lexicon/seed_lexicon.csv")
# every reviewed sheet: candidates_tfidf.csv, candidates_tfidf_<tag>.csv, candidates_embedding*.csv ...
SHEETS = ([(p, "channel", "tfidf") for p in sorted(Path("data/lexicon").glob("candidates_tfidf*.csv"))] +
          [(p, "channel_assigned", "embedding") for p in sorted(Path("data/lexicon").glob("candidates_embedding*.csv"))])
OUT = Path("lexicon/lexicon.csv")
SUMMARY = Path("docs/lexicon_summary.md")
LOW, HIGH = 300, 500


def key(t):
    return re.sub(r"[-\s]+", " ", t.strip().lower())


def main():
    seeds = list(csv.DictReader(open(SEEDS, encoding="utf-8-sig", newline="")))
    out, seen, problems = [], {}, []
    for r in seeds:
        r = {"term": r["term"], "channel": r["channel"], "lang": r.get("lang") or "en",
             "variants": r.get("variants", ""), "from_brief": r.get("from_brief", "0"),
             "source": "seed", "note": r.get("note", "")}
        out.append(r)
        seen[key(r["term"])] = r
        for v in [x for x in r["variants"].split("|") if x.strip()]:
            seen.setdefault(key(v), r)

    for path, ch_col, source in SHEETS:
        if not path.exists():
            print(f"(skipped, not found: {path})")
            continue
        n_keep = 0
        for r in csv.DictReader(open(path, encoding="utf-8-sig", newline="")):
            if (r.get("keep") or "").strip().lower() not in {"1", "y", "yes", "x"}:
                continue
            n_keep += 1
            term, ch = r["term"].strip(), (r.get(ch_col) or "").strip().lower()
            if ch not in CHANNELS:
                problems.append(f"{path.name}: '{term}' has channel '{ch}' (must be one of {sorted(CHANNELS)})")
                continue
            k = key(term)
            if k in seen:
                if seen[k]["channel"] != ch:
                    problems.append(f"'{term}' already in the lexicon under channel "
                                    f"'{seen[k]['channel']}', sheet says '{ch}'")
                continue
            row = {"term": term, "channel": ch, "lang": "en", "variants": "", "from_brief": "0",
                   "source": source, "note": ""}
            out.append(row)
            seen[k] = row
        print(f"{path.name}: {n_keep} terms marked keep")

    if problems:
        print("\nPROBLEMS (fix in the sheets and run again):")
        for p in problems:
            print("  -", p)
        sys.exit(1)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["term", "channel", "lang", "variants", "from_brief", "source", "note"])
        w.writeheader()
        w.writerows(out)
    by_ch, by_src = Counter(r["channel"] for r in out), Counter(r["source"] for r in out)
    lines = ["# Deglobalization lexicon", "", f"Terms: **{len(out)}** (brief: {LOW} to {HIGH}).", "",
             "| Channel | Terms |", "|---|---:|"] + [f"| {c} | {n} |" for c, n in sorted(by_ch.items())]
    lines += ["", "| Source | Terms |", "|---|---:|"] + [f"| {c} | {n} |" for c, n in sorted(by_src.items())]
    if not LOW <= len(out) <= HIGH:
        lines += ["", f"**The lexicon has {len(out)} terms, outside the {LOW} to {HIGH} the brief asks for.**"]
        print(f"WARNING: {len(out)} terms, outside {LOW} to {HIGH}")
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(out)} terms) and {SUMMARY}")


if __name__ == "__main__":
    main()
