"""
Month 4: can postings be placed in NUTS-2 regions? Audits the location fields of a board before script 93 maps them.

Reports: postings, share with a non-empty location, share with nuts1/nuts2/nuts3 filled, locations that name only
a country (vague), the 25 most common location strings, the nuts2 codes found, and whether one location string
always maps to the same nuts2 code where nuts2 is filled (a lookup table could then be learnt from those rows).
Duplicates are not removed here; the counts are for the raw sampled items.

Run (project root, venv active):
    python -m diagnostics.95_location_audit --label jobbland --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl
Writes docs/location_audit_<label>.md.
"""
import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

COUNTRIES = {"sweden", "sverige", "france", "germany", "deutschland", "allemagne", "europe", "european union", "eu"}


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--label", required=True)
    a = ap.parse_args()
    n = 0
    fill = Counter()
    loc, n2, vague = Counter(), Counter(), Counter()
    by = defaultdict(Counter)
    for p in a.corpus:
        for l in open(p, encoding="utf-8"):
            if not l.strip():
                continue
            for it in json.loads(l)["items"]:
                n += 1
                s = norm(it.get("location"))
                for k in ("location", "nuts1", "nuts2", "nuts3"):
                    fill[k] += bool(it.get(k))
                if s:
                    loc[s] += 1
                    parts = [x.strip() for x in s.split(",")]
                    if all(x in COUNTRIES for x in parts):
                        vague[s] += 1
                if it.get("nuts2"):
                    n2[str(it["nuts2"])] += 1
                    if s:
                        by[s][str(it["nuts2"])] += 1
    multi = {k: v for k, v in by.items() if len(v) > 1}
    md = [f"# Location audit: {a.label}", "",
          f"{n:,} sampled items (duplicates not removed).", "",
          "| field | filled | share |", "|---|---|---|"]
    md += [f"| {k} | {fill[k]:,} | {fill[k] / max(n, 1):.1%} |" for k in ("location", "nuts1", "nuts2", "nuts3")]
    md += ["", f"Locations naming only a country: {sum(vague.values()):,} ({sum(vague.values()) / max(n, 1):.1%}): "
           + ", ".join(f"{k} {v:,}" for k, v in vague.most_common(5)),
           f"Distinct location strings: {len(loc):,}. Distinct nuts2 codes: {len(n2)}.",
           f"Location strings with nuts2 filled: {len(by):,}; of them mapped to more than one code: {len(multi):,}.", "",
           "## Most common locations", "", "| location | postings |", "|---|---|"]
    md += [f"| {k} | {v:,} |" for k, v in loc.most_common(25)]
    md += ["", "## nuts2 codes found", "", "| code | postings |", "|---|---|"]
    md += [f"| {k} | {v:,} |" for k, v in n2.most_common(40)]
    if multi:
        md += ["", "## Locations with more than one nuts2 code", ""]
        md += [f"- {k}: {dict(v)}" for k, v in list(multi.items())[:15]]
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/location_audit_{a.label}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
