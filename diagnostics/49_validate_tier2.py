"""
Validation of Tier 2 of the fallback chain (occupation -> default skill set).

The brief says the student "builds and validates this occupation-to-skills
lookup in Month 2". Tier 2 has two links, and each is checked separately:

A. The skill sets. For profiles that have BOTH an ESCO occupation URI and
   self-reported skills (so Tier 1 data exist), compare the skill set that
   the ESCO table would infer from the occupation (essential + optional
   skills) with the profile's own skills. For each profile:
     recall    = share of the profile's own (matchable) skills that are in
                 the inferred set
     precision = share of the inferred set that the profile reports
   The same numbers are computed for a RANDOM OTHER occupation taken from
   another profile in the pool (fixed seed). If the real occupation does not
   beat a random one, the lookup carries no information. The difference is
   given with a bootstrap 95% interval.
   Own skills are matched to ESCO skills by URI when they are URIs and by
   lower-cased label otherwise (ESCO preferred labels only), so the report
   also shows what share of own skills could be matched at all.

B. The free-text link (optional). If --matcher-sheet points to the hand-
   labelled sheet written by 06b_validate_occupation_matcher.py (columns
   'method' and 'correct_y_n'), precision by method (exact / fuzzy) and the
   coverage of each method are computed with Wilson 95% intervals.

Reads: data/raw/profiles_sample.jsonl and occupationSkillRelations_en.csv
(ESCO download; columns occupationUri, relationType, skillUri, skillLabel).
No network, no credentials. The profile file contains personal data and stays
out of the repository; only aggregate numbers are written.

Run (from the project root, venv active):
    python -m diagnostics.49_validate_tier2
    python -m diagnostics.49_validate_tier2 --matcher-sheet <labelled .xlsx or .csv>
    python -m diagnostics.49_validate_tier2 --relations <path to the ESCO csv>

The ESCO file is looked for in data/raw/ and in the project root. The matcher
sheet is the file written by 06b_validate_occupation_matcher.py after the
'correct_y_n' column was filled in by hand (y / n); .xlsx and .csv both work.

Output: docs/tier2_validation.md
"""

import argparse
import csv
import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

PROFILES_PATH = Path("data/raw/profiles_sample.jsonl")
OUT_PATH = Path("docs/tier2_validation.md")
OCC_PREFIX = "http://data.europa.eu/esco/occupation/"
SEED = 42
N_BOOT = 2000


def norm(text) -> str:
    return re.sub(r"\s+", " ", str(text).strip().lower())


def load_relations(path: Path):
    """occupation uri -> (set essential, set optional); skill uri -> label;
    label -> skill uri."""
    ess, opt = defaultdict(set), defaultdict(set)
    label_of, uri_of = {}, {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            occ, sk = row["occupationUri"], row["skillUri"]
            (ess if row["relationType"].strip().lower() == "essential"
             else opt)[occ].add(sk)
            lab = norm(row.get("skillLabel", ""))
            if lab:
                label_of[sk] = lab
                uri_of.setdefault(lab, sk)
    return ess, opt, label_of, uri_of


RELATIONS_CANDIDATES = [Path("data/raw/occupationSkillRelations_en.csv"),
                        Path("occupationSkillRelations_en.csv")]


def find_relations(given):
    paths = [Path(given)] if given else RELATIONS_CANDIDATES
    for p in paths:
        if p.exists():
            return p
    raise SystemExit(
        "ESCO relations file not found. Tried: "
        + ", ".join(str(p) for p in paths)
        + ". Pass --relations <path to occupationSkillRelations_en.csv>.")


def esco_occupations(occupation_uris):
    if not isinstance(occupation_uris, list):
        return []
    return [u for u in occupation_uris
            if isinstance(u, str) and u.startswith(OCC_PREFIX)]


def own_skill_uris(skills, uri_of):
    """Map a profile's skills to ESCO skill URIs. Returns (set of uris,
    number of skill entries)."""
    out, n = set(), 0
    for item in skills or []:
        n += 1
        uri, label = None, None
        if isinstance(item, dict):
            uri = item.get("uri") or item.get("id")
            label = item.get("label") or item.get("name")
        elif isinstance(item, str):
            if item.startswith("http"):
                uri = item
            else:
                label = item
        if uri and uri.startswith("http"):
            out.add(uri)
        elif label and norm(label) in uri_of:
            out.add(uri_of[norm(label)])
    return out, n


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def median(xs):
    s = sorted(xs)
    if not s:
        return float("nan")
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def boot_ci(diffs, rng):
    if len(diffs) < 2:
        return (float("nan"), float("nan"))
    means = []
    for _ in range(N_BOOT):
        sample = [diffs[rng.randrange(len(diffs))] for _ in diffs]
        means.append(mean(sample))
    means.sort()
    return means[int(0.025 * N_BOOT)], means[int(0.975 * N_BOOT) - 1]


def metrics(own, inferred):
    hits = len(own & inferred)
    rec = hits / len(own) if own else float("nan")
    prec = hits / len(inferred) if inferred else float("nan")
    return rec, prec


def part_a(profiles, ess, opt, uri_of):
    L = ["## A. Do the inferred skill sets resemble the profiles' own skills?\n"]
    pool = []
    n_with_occ = n_in_table = 0
    own_entries = own_matched = 0
    for p in profiles:
        occs = esco_occupations(p.get("occupation_uris"))
        skills = p.get("skills")
        if not occs or not skills:
            continue
        n_with_occ += 1
        occ = next((o for o in occs if o in ess or o in opt), None)
        if occ is None:
            continue
        n_in_table += 1
        own, n_entries = own_skill_uris(skills, uri_of)
        own_entries += n_entries
        own_matched += len(own)
        if own:
            pool.append((occ, own))

    L.append(f"- Profiles with an ESCO occupation URI and self-reported skills: "
             f"**{n_with_occ}**; occupation found in the ESCO table: "
             f"**{n_in_table}**.")
    if own_entries:
        L.append(f"- Own skills matched to an ESCO skill (URI or preferred "
                 f"label): {own_matched} of {own_entries} entries "
                 f"({own_matched / own_entries:.0%}). Skills that are free "
                 "text and not an ESCO label cannot be scored.")
    L.append(f"- Profiles with at least one matchable own skill (used "
             f"below): **{len(pool)}**.\n")
    if len(pool) < 2:
        L.append("Too few profiles to compute anything. The check cannot "
                 "validate the skill sets on this sample; say so in the "
                 "report and pull more Revelio profiles that carry both "
                 "fields.\n")
        return L

    rng = random.Random(SEED)
    rows = []
    for i, (occ, own) in enumerate(pool):
        inferred = ess.get(occ, set()) | opt.get(occ, set())
        ess_only = ess.get(occ, set())
        rec, prec = metrics(own, inferred)
        rec_e, _ = metrics(own, ess_only)
        # random other occupation: from another profile with a different one
        others = [o for o, _ in pool if o != occ]
        if not others:
            continue
        occ_r = rng.choice(others)
        inf_r = ess.get(occ_r, set()) | opt.get(occ_r, set())
        rec_r, prec_r = metrics(own, inf_r)
        rec_er, _ = metrics(own, ess.get(occ_r, set()))
        rows.append((rec, prec, rec_e, rec_r, prec_r, rec_er, len(inferred)))

    n = len(rows)
    col = lambda i: [r[i] for r in rows]
    d_rec = [r[0] - r[3] for r in rows]
    d_prec = [r[1] - r[4] for r in rows]
    lo, hi = boot_ci(d_rec, rng)
    lo_p, hi_p = boot_ci(d_prec, rng)
    wins = sum(1 for d in d_rec if d > 0)
    L.append(f"Profiles scored: **{n}**. Mean size of the inferred set: "
             f"{mean(col(6)):.0f} skills.\n")
    L.append("| Measure | Own occupation | Random other occupation | Difference (95% bootstrap interval) |")
    L.append("|---|---:|---:|---|")
    L.append(f"| Recall, essential + optional (mean) | {mean(col(0)):.1%} | "
             f"{mean(col(3)):.1%} | {mean(d_rec):+.1%} ({lo:+.1%} to {hi:+.1%}) |")
    L.append(f"| Recall, essential only (mean) | {mean(col(2)):.1%} | "
             f"{mean(col(5)):.1%} | |")
    L.append(f"| Precision, essential + optional (mean) | {mean(col(1)):.1%} | "
             f"{mean(col(4)):.1%} | {mean(d_prec):+.1%} ({lo_p:+.1%} to {hi_p:+.1%}) |")
    L.append(f"| Recall (median) | {median(col(0)):.1%} | {median(col(3)):.1%} | |")
    L.append("")
    L.append(f"The own occupation has the higher recall in {wins} of {n} "
             f"profiles ({wins / n:.0%}).\n")
    L.append("How to read it: recall says how much of what a person reports is "
             "covered by the default set; precision says how much of the "
             "default set the person reports (low by construction, since an "
             "ESCO occupation lists many optional skills). The result is "
             "informative only if the own-occupation values clearly exceed the "
             "random-occupation values and the interval excludes zero. With "
             "few profiles the interval is wide, and a profile that reports "
             "skills is not a typical Tier 2 profile (Tier 2 is for profiles "
             "without skills).\n")
    return L


def read_sheet(path: Path):
    """Rows of (method, label) from an .xlsx or .csv sheet; None if the
    columns 'method' and 'correct_y_n' are not found."""
    if path.suffix.lower() == ".csv":
        with open(path, encoding="utf-8-sig", newline="") as f:
            table = list(csv.reader(f))
    else:
        try:
            import openpyxl
        except ImportError:
            return None
        ws = openpyxl.load_workbook(path, data_only=True).active
        table = [list(r) for r in ws.iter_rows(values_only=True)]
    if not table:
        return None
    header = [str(c).strip().lower() if c else "" for c in table[0]]
    try:
        im, ic = header.index("method"), header.index("correct_y_n")
    except ValueError:
        return None
    rows = []
    for r in table[1:]:
        if len(r) <= max(im, ic) or r[im] in (None, ""):
            continue
        rows.append((str(r[im]).strip().lower(),
                     str(r[ic]).strip().lower() if r[ic] not in (None, "") else ""))
    return rows


def part_b(path: Path):
    L = ["## B. Free-text occupation matcher: hand-labelled precision\n"]
    rows = read_sheet(path)
    if rows is None:
        L.append("The sheet could not be read (openpyxl missing, or columns "
                 "'method' and 'correct_y_n' not found).\n")
        return L
    total = len(rows)
    n_lab = sum(1 for m, lab in rows if lab in ("y", "n"))
    if n_lab == 0:
        L.append("No row in this sheet is labelled `y` or `n`, so no precision "
                 "can be computed. If you filled in the labels in a spreadsheet "
                 "copy (for example the .xlsx), pass that file instead of the "
                 ".csv written by script 06.\n")
    L.append(f"Rows in the sheet: {total}. One rater (the author). Rows "
             "counted only when labelled `y` or `n`.\n")
    L.append("| Method | Rows matched | Labelled | Correct | Precision (Wilson 95%) | Share of all rows |")
    L.append("|---|---:|---:|---:|---|---:|")
    for m in ("exact", "fuzzy"):
        sel = [lab for meth, lab in rows if meth == m]
        lab_rows = [x for x in sel if x in ("y", "n")]
        k = sum(1 for x in lab_rows if x == "y")
        n = len(lab_rows)
        lo, hi = wilson(k, n)
        pr = f"{k / n:.0%} ({lo:.0%}-{hi:.0%})" if n else "n/a"
        L.append(f"| {m} | {len(sel)} | {n} | {k} | {pr} | {len(sel) / total:.0%} |")
    nm = sum(1 for meth, _ in rows if meth == "no_match")
    L.append(f"| no match | {nm} | | | | {nm / total:.0%} |")
    L.append("")
    L.append("Reading: the exact-substring method is the one used in Tier 2. "
             "The fuzzy method is disabled. A high precision with a small "
             "number of labelled rows has a wide interval, which is why the "
             "interval is shown.\n")
    return L


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--profiles", default=str(PROFILES_PATH))
    ap.add_argument("--relations", default=None,
                    help="path to occupationSkillRelations_en.csv (default: "
                         "data/raw/ or the project root)")
    ap.add_argument("--matcher-sheet", default=None,
                    help="hand-labelled sheet (xlsx) from script 06")
    args = ap.parse_args()

    rel = find_relations(args.relations)
    print(f"ESCO table file: {rel}")
    ess, opt, label_of, uri_of = load_relations(rel)
    print(f"ESCO table: {len(set(ess) | set(opt))} occupations, "
          f"{len(label_of)} skills with labels")
    profiles = []
    with open(args.profiles, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                profiles.append(json.loads(line))
    print(f"Profiles: {len(profiles)}")

    L = ["# Tier 2 validation\n",
         "Tier 2 infers a skill set from an occupation (ESCO essential + "
         "optional skills). Part A checks the skill sets against profiles "
         "that report their own skills; part B checks the free-text link "
         "that extends Tier 2 beyond Revelio. Aggregate numbers only.\n"]
    L += part_a(profiles, ess, opt, uri_of)
    if args.matcher_sheet:
        L += part_b(Path(args.matcher_sheet))
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
