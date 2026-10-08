"""
Postings breakdowns by source, year, country and sector, written to
docs/postings_breakdowns.md (the brief's Week 2 "postings by year, country,
sector" deliverable).

IMPORTANT: data/raw/postings_sample.jsonl was drawn at roughly the same size
per source, so counts here describe the SAMPLE and are driven by that design,
not by the true size of each source or country. Read the "% of postings with
a known value" and the within-source shares, and use API count queries
(see 17_count_by_window.py) for true population sizes.

Duplicate sources: four pairs (jobbland/jobbland.se, lesjeudis/lesjeudis.com,
jobmedic/jobmedic.co.uk, jobbguru/jobbguru.se) contain largely the same
postings under different names (see 20_check_duplicate_postings.py). With
--merge-aliases, a posting from the alias source is dropped when the
canonical source already holds the same posting (same title/organisation/
location/date, or the same description start), and the rest are relabelled as
the canonical source. The output then goes to docs/postings_breakdowns_merged.md.

Usage, from the repo root:
    python -m diagnostics.18_postings_breakdowns
    python -m diagnostics.18_postings_breakdowns --merge-aliases
"""

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

POSTINGS_PATH = Path("data/raw/postings_sample.jsonl")
OUT_PATH = Path("docs/postings_breakdowns.md")
OUT_PATH_MERGED = Path("docs/postings_breakdowns_merged.md")
TOP_N = 25
ALIASES = {"jobbland.se": "jobbland", "lesjeudis.com": "lesjeudis",
           "jobmedic.co.uk": "jobmedic", "jobbguru.se": "jobbguru"}


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def missing(value):
    if value is None:
        return True
    if isinstance(value, str) and value.strip().lower() in ("", "empty"):
        return True
    if isinstance(value, (list, dict)) and not value:
        return True
    return False


def year_of(posting):
    value = posting.get("upload_date")
    if missing(value):
        return None
    text = str(value)
    return text[:4] if text[:4].isdigit() else None


def as_list(value):
    if missing(value):
        return []
    return value if isinstance(value, list) else [value]


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def pct(n, d):
    return f"{n / d:.1%}" if d else "n/a"


def sector_label(item):
    if isinstance(item, dict):
        return str(item.get("label") or item.get("name") or item.get("id") or item)
    return str(item)


def _norm(value):
    return "" if value is None else re.sub(r"\s+", " ", str(value)).strip().lower()


def posting_keys(p):
    """Keys identifying 'the same posting': content key and description key."""
    keys = set()
    title = _norm(p.get("title"))
    if title:
        keys.add("c|" + "|".join([title, _norm(p.get("organization")), _norm(p.get("location")),
                                  _norm(p.get("upload_date"))[:10]]))
    desc = _norm(p.get("description"))
    if len(desc) >= 80:
        keys.add("d|" + hashlib.md5(desc[:300].encode("utf-8")).hexdigest())
    return keys


def merge_aliases(postings):
    """Drop alias-source postings already present in the canonical source and
    relabel the rest. Returns (merged_postings, {alias: (dropped, kept)})."""
    canonical_keys = defaultdict(set)
    for p in postings:
        if p.get("source") in ALIASES.values():
            canonical_keys[p["source"]] |= posting_keys(p)
    merged, stats = [], defaultdict(lambda: [0, 0])
    for p in postings:
        source = p.get("source")
        if source in ALIASES:
            canon = ALIASES[source]
            if posting_keys(p) & canonical_keys[canon]:
                stats[source][0] += 1
                continue
            stats[source][1] += 1
            p = {**p, "source": canon}
        merged.append(p)
    return merged, {k: tuple(v) for k, v in stats.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--merge-aliases", action="store_true",
                        help="collapse the four duplicate source pairs into their canonical source")
    args = parser.parse_args()

    postings = load(POSTINGS_PATH)
    out_path = OUT_PATH
    note = ""
    if args.merge_aliases:
        postings, stats = merge_aliases(postings)
        out_path = OUT_PATH_MERGED
        lines = [f"- {alias}: {d} dropped as already in `{ALIASES[alias]}`, {k} kept and relabelled"
                 for alias, (d, k) in sorted(stats.items())]
        note = "Duplicate source pairs were merged (--merge-aliases):\n" + "\n".join(lines) + "\n"
    n = len(postings)
    parts = [f"# Postings breakdowns (sample of {n:,} postings{', alias sources merged' if args.merge_aliases else ''})\n",
             "Counts describe the sample, which was drawn at roughly equal size per source; they are not "
             "the true distribution. See `diagnostics/18_postings_breakdowns.py`.\n"]
    if note:
        parts.append(note)

    # 1. by source and year of upload_date
    by_source = Counter(p.get("source", "UNKNOWN") for p in postings)
    years = sorted({y for p in postings if (y := year_of(p))})
    cell = defaultdict(Counter)
    for p in postings:
        cell[p.get("source", "UNKNOWN")][year_of(p) or "none"] += 1
    header = ["Source", "n"] + years + ["no date"]
    rows = []
    for source, total in by_source.most_common():
        rows.append([source, total] + [cell[source].get(y, 0) for y in years] + [cell[source].get("none", 0)])
    parts.append("## 1. Sample by source and `upload_date` year\n")
    parts.append(md_table(header, rows) + "\n")

    # 2. by country (location_code)
    known = [p for p in postings if not missing(p.get("location_code"))]
    parts.append("## 2. Country (`location_code`)\n")
    parts.append(f"`location_code` is populated for {len(known):,} of {n:,} postings ({pct(len(known), n)}). "
                 "Codes follow the Eurostat convention (EL for Greece, UK for the United Kingdom).\n")
    country = Counter(str(p["location_code"]).strip().upper() for p in known)
    total_known = sum(country.values())
    rows = [[code, c, pct(c, total_known)] for code, c in country.most_common(TOP_N)]
    parts.append(md_table(["Country code", "Postings in sample", "% of postings with a code"], rows) + "\n")
    if len(country) > TOP_N:
        parts.append(f"({len(country) - TOP_N} further codes not shown.)\n")

    src_known = defaultdict(lambda: [0, 0])
    for p in postings:
        s = p.get("source", "UNKNOWN")
        src_known[s][1] += 1
        if not missing(p.get("location_code")):
            src_known[s][0] += 1
    rows = [[s, f"{k}/{t}", pct(k, t), len({str(p['location_code']).strip().upper() for p in postings if p.get('source', 'UNKNOWN') == s and not missing(p.get('location_code'))})]
            for s, (k, t) in sorted(src_known.items(), key=lambda x: -x[1][1])]
    parts.append("### Country completeness and spread by source\n")
    parts.append(md_table(["Source", "With code", "%", "Distinct codes"], rows) + "\n")

    # 3. by sector
    with_sector = [p for p in postings if as_list(p.get("sectors"))]
    parts.append("## 3. Sector (`sectors`)\n")
    parts.append(f"`sectors` is populated for {len(with_sector):,} of {n:,} postings ({pct(len(with_sector), n)}). "
                 "A posting can list several sectors; each is counted once per posting.\n")
    sector = Counter()
    for p in with_sector:
        for label in {sector_label(x) for x in as_list(p.get("sectors"))}:
            sector[label] += 1
    rows = [[label, c, pct(c, len(with_sector))] for label, c in sector.most_common(TOP_N)]
    parts.append(md_table(["Sector", "Postings in sample", "% of postings with sectors"], rows) + "\n")
    if len(sector) > TOP_N:
        parts.append(f"({len(sector) - TOP_N} further sectors not shown; {len(sector)} distinct in total.)\n")

    src_sec = defaultdict(lambda: [0, 0])
    for p in postings:
        s = p.get("source", "UNKNOWN")
        src_sec[s][1] += 1
        if as_list(p.get("sectors")):
            src_sec[s][0] += 1
    rows = [[s, f"{k}/{t}", pct(k, t)] for s, (k, t) in sorted(src_sec.items(), key=lambda x: -x[1][1])]
    parts.append("### Sector completeness by source\n")
    parts.append(md_table(["Source", "With sectors", "%"], rows) + "\n")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(parts), encoding="utf-8")
    print("\n".join(parts))
    print(f"\nWritten to {out_path}")


if __name__ == "__main__":
    main()
