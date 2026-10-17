"""
Field completeness of postings by country and by sector.

The Month 2 brief (Step 2) asks for the completeness audit "disaggregated by
source, country, and sector". The report has completeness by source
(Section 3, 9.7) and the shares of postings by country (13.2) and by sector
(13.3), but not the completeness of each field WITHIN a country or a sector.
This script produces those two tables from the working sample,
data/raw/postings_sample.jsonl (one posting per line).

Tables
------
1. By country (`location_code`, upper-cased; postings without a code form
   the row "(no code)"): number of postings and the share with each field
   filled.
2. By sector: the sector labels of a posting (a posting can carry several;
   it is counted once in each) for the TOP_N most frequent labels, plus the
   row "(no sector)" for postings with an empty `sectors`. The `sectors`
   field itself is, by construction, 100% filled in the labelled rows, so it
   is not repeated there.
3. By source x country, a short table of which sources make up each country,
   because country is almost a function of source (Section 13.2) and a
   country row mostly repeats its source's completeness.

A field counts as filled when it is not null, not an empty string, not the
literal 'empty' and not an empty list or dictionary (the definition used by
18_postings_breakdowns.py).

Duplicates: four pairs of sources hold largely the same postings under two
names (jobbland / jobbland.se, lesjeudis / lesjeudis.com, jobmedic /
jobmedic.co.uk, jobbguru / jobbguru.se; Section 13.4). By default the alias
source of each pair is left out, so those postings are not counted twice.
This differs slightly from the merged sample of 18_postings_breakdowns.py
--merge-aliases, which keeps the non-duplicate alias postings. Use
--keep-aliases to leave all sources in.

The sample was drawn at about the same size per source, so counts describe
the sample and not the population; read the within-row shares. Cells are
marked with * when the row has fewer than MIN_N postings (shares are then
unreliable).

Run (from the project root, venv active):
    python -m diagnostics.47_completeness_by_country_sector
    python -m diagnostics.47_completeness_by_country_sector --keep-aliases --top 40

No network access and no credentials are needed.
Output: docs/completeness_by_country_sector.md
"""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

POSTINGS_PATH = Path("data/raw/postings_sample.jsonl")
OUT_PATH = Path("docs/completeness_by_country_sector.md")

TOP_N = 25
MIN_N = 30
# Alias source -> canonical source (Section 13.4).
ALIASES = {"jobbland.se": "jobbland", "lesjeudis.com": "lesjeudis",
           "jobmedic.co.uk": "jobmedic", "jobbguru.se": "jobbguru"}

# Fields reported. Others whose name contains one of EXTRA_HINTS are added
# automatically when present in the sample (experience level, contract type).
CORE_FIELDS = ["title", "description", "organization", "location",
               "location_code", "nuts1", "occupations", "skills", "sectors"]
EXTRA_HINTS = ("experience", "level", "type")


def missing(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in ("", "empty"):
        return True
    if isinstance(value, (list, dict)) and not value:
        return True
    return False


def as_list(value):
    if missing(value):
        return []
    return value if isinstance(value, list) else [value]


def sector_label(item) -> str:
    if isinstance(item, dict):
        return str(item.get("label") or item.get("name") or item.get("id")
                   or item)
    return str(item)


def load(path: Path) -> list:
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return out


def cell(group, field) -> str:
    n = len(group)
    if n == 0:
        return "n/a"
    k = sum(1 for p in group if not missing(p.get(field)))
    text = f"{k / n:.0%}"
    return text + "*" if n < MIN_N else text


def fields_present(postings):
    keys = set()
    for p in postings:
        keys.update(p.keys())
    fields = [f for f in CORE_FIELDS if f in keys]
    for k in sorted(keys):
        if k not in fields and any(h in k.lower() for h in EXTRA_HINTS):
            fields.append(k)
    return fields


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--path", default=str(POSTINGS_PATH))
    ap.add_argument("--keep-aliases", action="store_true",
                    help="keep the four alias sources (duplicates counted twice)")
    ap.add_argument("--top", type=int, default=TOP_N,
                    help="number of sector labels in table 2")
    args = ap.parse_args()

    postings = load(Path(args.path))
    total_raw = len(postings)
    if not args.keep_aliases:
        postings = [p for p in postings if p.get("source") not in ALIASES]
    print(f"Postings loaded: {total_raw}; used: {len(postings)}")

    fields = fields_present(postings)
    print("Fields reported:", ", ".join(fields))

    # 1. By country
    by_country = defaultdict(list)
    for p in postings:
        code = p.get("location_code")
        key = "(no code)" if missing(code) else str(code).strip().upper()
        by_country[key].append(p)
    order = sorted(by_country, key=lambda c: (c == "(no code)",
                                              -len(by_country[c])))
    rows1 = [[c, len(by_country[c])] + [cell(by_country[c], f) for f in fields]
             for c in order]
    rows1.append(["**All**", len(postings)] +
                 [cell(postings, f) for f in fields])

    # 2. By sector
    by_sector = defaultdict(list)
    no_sector = []
    for p in postings:
        labels = {sector_label(x) for x in as_list(p.get("sectors"))}
        if not labels:
            no_sector.append(p)
        for lab in labels:
            by_sector[lab].append(p)
    top = sorted(by_sector, key=lambda s: -len(by_sector[s]))[: args.top]
    sector_fields = [f for f in fields if f != "sectors"]
    rows2 = [[s[:60], len(by_sector[s])] +
             [cell(by_sector[s], f) for f in sector_fields] for s in top]
    rows2.append(["(no sector)", len(no_sector)] +
                 [cell(no_sector, f) for f in sector_fields])

    # 3. Source x country
    pair = Counter()
    for p in postings:
        code = p.get("location_code")
        key = "(no code)" if missing(code) else str(code).strip().upper()
        pair[(key, p.get("source"))] += 1
    rows3 = []
    for c in order:
        parts = sorted(((s, n) for (cc, s), n in pair.items() if cc == c),
                       key=lambda x: -x[1])
        rows3.append([c, len(by_country[c]),
                      ", ".join(f"{s} {n}" for s, n in parts[:6]) +
                      (" ..." if len(parts) > 6 else "")])

    L = ["# Completeness by country and by sector (postings, working sample)\n"]
    L.append(f"Source file: `{args.path}`. Postings in the file: "
             f"{total_raw:,}; used: {len(postings):,}"
             + ("" if args.keep_aliases else
                f" (the four alias sources {', '.join(sorted(ALIASES))} are "
                "left out so duplicate postings are not counted twice)") +
             ". A field is filled when it is not null, not empty, not the "
             "literal 'empty' and not an empty list. `*` marks a row with "
             f"fewer than {MIN_N} postings. The sample has about the same "
             "size per source, so read the shares within a row, not the "
             "counts.\n")
    L.append("## 1. By country (`location_code`)\n")
    L += md_table(["Country", "Postings"] + [f"`{f}`" for f in fields], rows1)
    L.append("")
    L.append("## 2. By sector (a posting with several sectors counts in each)\n")
    L.append(f"The {args.top} most frequent sector labels; labels are at mixed "
             "NACE levels (Section 13.3), so rows can overlap.\n")
    L += md_table(["Sector", "Postings"] + [f"`{f}`" for f in sector_fields],
                  rows2)
    L.append("")
    L.append("## 3. Which sources make up each country\n")
    L += md_table(["Country", "Postings", "Sources (postings)"], rows3)
    L.append("")
    L.append("## 4. How to read it\n")
    L.append("- Country is almost a function of source, so a country row "
             "mostly repeats the completeness of its sources (table 3).")
    L.append("- The sector rows describe only postings that carry a sector; "
             "the row '(no sector)' shows what the others lack. Sector "
             "completeness is itself very uneven by source (Section 13.3).")
    L.append("- Rows marked `*` are too small to compare.")
    L.append("")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
