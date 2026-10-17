"""
Greece panel reliability: are Greek profiles disproportionately sparse?

The Month 2 brief says the completeness audit "must check this explicitly".
The report so far covers Greek POSTINGS (EL, 468 postings, all from
kariera.gr) but not Greek PROFILES. Profiles carry no country code, only the
free-text field `location` (100% filled), so Greek profiles have to be found
from that text. This script does that, shows what it matched so the rule can
be checked by eye, and compares field completeness for Greek profiles with
the rest of the working sample.

What it does
------------
1. Reads the working sample, data/raw/profiles_sample.jsonl (written by
   01_fetch_sample.py; one JSON profile per line).
2. Marks a profile as Greek when its `location` text, lower-cased and
   stripped of accents, contains a Greek country or city name (lists below).
   Two ambiguous names are handled: "Athens" followed by a US state
   (Athens, Georgia / GA / Ohio ...) is not counted, and short names are
   matched as whole words only.
3. Prints and writes: how many profiles are Greek, from which sources, the
   distinct matched location strings (to check for false positives), and for
   Greek, non-Greek and non-Greek-same-sources profiles the share with
   non-empty skills, occupation_uris, sectors, content, description and
   startdate, with 95% Wilson intervals.
4. Gives the tier split that does not need the lookup (Tier 1 = skills
   present; "Tier 2 reachable" = no skills but occupation_uris present;
   otherwise Tier 3/4 candidate). The exact tier labels come from
   assign_data_completeness_tier.py; this script does not replace it.

The comparison that matters is within source. Revelio has by far the lowest
`skills` completeness (12.4%), so a country with many Revelio profiles looks
sparse for that reason alone. The third group in the output (non-Greek
profiles from the sources that also hold Greek profiles) removes that
source effect.

Run (from the project root, venv active):
    python -m diagnostics.46_greek_profiles_check
    python -m diagnostics.46_greek_profiles_check --path data/raw/profiles_sample.jsonl

No network access and no credentials are needed.
Output: docs/greek_profiles_check.md
"""

import argparse
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

PROFILES_PATH = Path("data/raw/profiles_sample.jsonl")
OUT_PATH = Path("docs/greek_profiles_check.md")

# Names compared after lower-casing and removing accents. Greek-script forms
# are written without accents for the same reason.
GREEK_TERMS = [
    "greece", "hellas", "hellenic", "ellada", "ελλαδα", "ελληνικη",
    "athens", "athina", "αθηνα", "αθηνων",
    "thessaloniki", "salonica", "θεσσαλονικη",
    "patras", "patra", "πατρα",
    "heraklion", "irakleio", "iraklion", "ηρακλειο",
    "larissa", "λαρισα",
    "volos", "βολος",
    "ioannina", "ιωαννινα",
    "chania", "χανια",
    "rhodes", "ροδος",
    "kalamata", "καλαματα",
    "piraeus", "πειραιας",
    "attica", "αττικη",
    "crete", "κρητη",
    "peristeri", "περιστερι",
    "kavala", "καβαλα",
    "alexandroupoli", "αλεξανδρουπολη",
]
# "Athens, Georgia", "Athens, GA", "Athens, Ohio", and similar are not Greece.
ATHENS_US = re.compile(
    r"\bathens\b[\s,]*(georgia|ga|ohio|oh|alabama|al|tennessee|tn|texas|tx|"
    r"west virginia|wv|usa|united states|us)\b"
)

FIELDS = ["skills", "occupation_uris", "sectors", "content", "description",
          "startdate"]


def fold(text) -> str:
    """Lower-case and strip accents (Greek tonos included)."""
    if not isinstance(text, str):
        return ""
    t = unicodedata.normalize("NFD", text.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return t.replace("ς", "σ")


# Rebuild the Greek terms through the same folding, so they match folded text.
TERM_RES = [
    (term, re.compile(r"(?<![^\W_])" + re.escape(fold(term)) + r"(?![^\W_])"))
    for term in GREEK_TERMS
]


def greek_term(location) -> str:
    """The matched term, or '' when the location is not Greek."""
    t = fold(location)
    if not t:
        return ""
    for term, rx in TERM_RES:
        if rx.search(t):
            if term == "athens" and ATHENS_US.search(t):
                continue
            return term
    return ""


def filled(value) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() not in ("", "empty", "--")
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return True


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def share(group, field):
    n = len(group)
    k = sum(1 for p in group if filled(p.get(field)))
    lo, hi = wilson(k, n)
    return k, n, (k / n if n else 0.0), lo, hi


def fmt(group, field) -> str:
    k, n, p, lo, hi = share(group, field)
    if n == 0:
        return "n/a"
    return f"{p:.1%} ({k}/{n}; {lo:.0%}-{hi:.0%})"


def tier_split(group):
    t1 = sum(1 for p in group if filled(p.get("skills")))
    t2 = sum(1 for p in group
             if not filled(p.get("skills")) and filled(p.get("occupation_uris")))
    rest = len(group) - t1 - t2
    return t1, t2, rest


def load(path: Path) -> list:
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--path", default=str(PROFILES_PATH))
    args = ap.parse_args()

    profiles = load(Path(args.path))
    total = len(profiles)
    print(f"Profiles loaded: {total}")

    matched = [(p, greek_term(p.get("location"))) for p in profiles]
    greek = [p for p, t in matched if t]
    other = [p for p, t in matched if not t]
    term_counts = Counter(t for _, t in matched if t)
    greek_sources = Counter(p.get("source") for p in greek)
    loc_counts = Counter(str(p.get("location")).strip() for p in greek)
    same_src_other = [p for p in other if p.get("source") in greek_sources]

    print(f"Greek by location text: {len(greek)} ({len(greek)/total:.2%})")

    L = []
    L.append("# Greece panel reliability: Greek profiles in the working sample\n")
    L.append(f"Source file: `{args.path}`. Profiles: {total:,}. Profiles have no "
             "country code, so a profile is Greek when its free-text `location` "
             "contains a Greek country or city name (accents ignored; Athens in "
             "a US state excluded). The list of matched strings is below so the "
             "rule can be checked by eye.\n")
    L.append("## 1. How many\n")
    L.append(f"- Greek profiles: **{len(greek)}** of {total:,} "
             f"({len(greek)/total:.2%}).")
    L.append(f"- Matched by term: " +
             (", ".join(f"`{t}` {n}" for t, n in term_counts.most_common())
              or "none") + ".")
    L.append("")
    if greek:
        L.append("### Sources of the Greek profiles\n")
        L.append("| Source | Greek profiles | All profiles of the source | Share |")
        L.append("|---|---:|---:|---:|")
        all_src = Counter(p.get("source") for p in profiles)
        for s, n in greek_sources.most_common():
            L.append(f"| {s} | {n} | {all_src[s]} | {n/all_src[s]:.1%} |")
        L.append("")
        L.append("### Matched location strings (top 40)\n")
        L.append("| Location text | Profiles |")
        L.append("|---|---:|")
        for loc, n in loc_counts.most_common(40):
            L.append(f"| {loc} | {n} |")
        L.append("")
    else:
        L.append("No profile in the sample has a Greek location. This is a "
                 "finding: the sample cannot support a Greece panel built on "
                 "profiles. Check the top location strings below to be sure "
                 "that the rule did not miss a spelling.\n")

    # Locations written (partly) in Greek letters that the rule did NOT match:
    # a direct check for Greek places missing from GREEK_TERMS.
    greek_letters = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")
    unmatched_gr = Counter(str(p.get("location")).strip() for p in other
                           if greek_letters.search(str(p.get("location") or "")))
    L.append("### Locations with Greek letters that the rule did not match\n")
    if unmatched_gr:
        L.append("Add any Greek place from this list to `GREEK_TERMS`.\n")
        L.append("| Location text | Profiles |")
        L.append("|---|---:|")
        for loc, n in unmatched_gr.most_common(40):
            L.append(f"| {loc} | {n} |")
    else:
        L.append("None: every location written in Greek letters was matched.")
    L.append("")
    print(f"Locations with Greek letters not matched: {sum(unmatched_gr.values())}")

    L.append("### Most frequent location strings in the whole sample (top 25)\n")
    L.append("| Location text | Profiles |")
    L.append("|---|---:|")
    for loc, n in Counter(str(p.get("location")).strip()
                          for p in profiles).most_common(25):
        L.append(f"| {loc} | {n} |")
    L.append("")

    if greek:
        L.append("## 2. Field completeness: Greek against the rest\n")
        L.append("Each cell shows share (filled/total; 95% Wilson interval). "
                 "'Same sources' are non-Greek profiles from the sources that "
                 "hold Greek profiles, which removes the source effect "
                 "(Revelio's `skills` completeness is 12.4%).\n")
        L.append("| Field | Greek | All non-Greek | Non-Greek, same sources |")
        L.append("|---|---|---|---|")
        for f in FIELDS:
            L.append(f"| `{f}` | {fmt(greek, f)} | {fmt(other, f)} | "
                     f"{fmt(same_src_other, f)} |")
        L.append("")
        L.append("## 3. Tier split that needs no lookup\n")
        L.append("| Group | Tier 1 (skills) | Tier 2 reachable (no skills, has "
                 "occupation_uris) | Neither (Tier 3 or 4) |")
        L.append("|---|---:|---:|---:|")
        for name, g in [("Greek", greek), ("All non-Greek", other),
                        ("Non-Greek, same sources", same_src_other)]:
            t1, t2, rest = tier_split(g)
            n = len(g) or 1
            L.append(f"| {name} (n={len(g)}) | {t1} ({t1/n:.1%}) | "
                     f"{t2} ({t2/n:.1%}) | {rest} ({rest/n:.1%}) |")
        L.append("")
        L.append("## 4. How to read it\n")
        L.append("- With fewer than about 30 Greek profiles the intervals are "
                 "too wide to call Greek profiles sparse or not; say that the "
                 "sample cannot answer and, if the Greece panel needs "
                 "profiles, pull Greek profiles on purpose.")
        L.append("- Compare Greek with the 'same sources' column, not with "
                 "the whole sample.")
        L.append("- The sample is not representative of the population "
                 "(Section 13.1 of the report), so these shares describe the "
                 "sample.")
        L.append("")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
