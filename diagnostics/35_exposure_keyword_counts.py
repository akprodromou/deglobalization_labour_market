"""
How big is the "exposed" group in each source? Pilot keyword counts on the pages
already sampled by script 33. No new API requests.

For the Iran-war / oil shock and the EU tariffs on Chinese EVs, an event study
needs a group of postings that the event plausibly touches, and a control group
that it does not. This script counts, per source and month, how many sampled
postings fall into each pilot group, using the posting TITLE (the only text
script 33 stored, cut to 90 characters) and, only with --with-sector, the first
SECTOR label. The first run matched sector labels too, and the matched titles showed
that this pollutes the groups (IT postings carrying an unrelated sector), so titles
only is now the default. Sector labels are empty in 2026 for kariera.gr and
jobbland.se (Section 9.7 item 11 of the report).

Groups (all pilot lists in English, German, French, Swedish and Greek):
    ev_industry        automotive, batteries, powertrain, e-mobility       (EV tariffs)
    vehicle_retail_service  cars, vehicles, Kfz, rental, dealers, workshops    (EV tariffs, indirect)
    energy_fuels       oil, gas, fuel, refining, energy                    (oil shock)
    transport_shipping drivers, logistics, shipping, aviation              (oil shock)
    tourism            hotels, restaurants, tourism                        (oil shock, indirect)
    manufacturing      chemicals, plastics, metals, production, industry   (oil shock, energy-intensive)
    control_health_edu nurses, doctors, teachers, care                     (candidate control group)

A posting can fall into more than one group. Matching ignores case and accents
(so Greek capitals without tonos match). The lists are a first guess: read the
"matched titles" section for false positives before trusting any number.

Output per source and month: matches / sample (share) and the implied number of
postings in the month (share x the month's total from script 32). A second table
pools the months before and after each event with a Wilson 95% interval for the
share. These are PILOT counts to size the groups, not results.

Usage, from the repo root:
    python -m diagnostics.35_exposure_keyword_counts
    python -m diagnostics.35_exposure_keyword_counts --pages-file data/raw/stability_pages_text.json --text-chars 400

With script 38's file the title and the first --text-chars characters of the description
are searched (the opening of an ad usually names the role; whole descriptions catch
"driver's licence required" and similar).

Needs data/raw/stability_pages.json (script 33) and, for the implied counts,
data/raw/event_window_counts.json (script 32). Output: docs/exposure_keywords.md
"""

import json
import math
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

PAGES_PATH = Path("data/raw/stability_pages.json")
COUNTS_PATH = Path("data/raw/event_window_counts.json")
REPORT_PATH = Path("docs/exposure_keywords.md")

# (title stems matched as word prefixes, exact title words, sector-label substrings)
GROUPS = {
    "ev_industry": (
        ["automotive", "automobilindustrie", "automobilhersteller", "powertrain", "drivetrain", "batter", "accumul",
         "elektrofahrzeug", "emobil", "e-mobil", "electromobil", "adas", "charging", "ladestation", "μπαταρ",
         "ηλεκτροκιν"],
        ["ev", "evs"],
        ["motor vehicles", "electrical equipment", "batteries"],
    ),
    "vehicle_retail_service": (
        ["vehicle", "vehicul", "fahrzeug", "kfz", "karosserie", "voiture", "fordon", "bilmek", "automobil", "αυτοκιν",
         "οχημ"],
        ["car", "cars", "auto", "bil", "pkw"],
        ["vehicle"],
    ),
    "energy_fuels": (
        ["petrol", "refiner", "refining", "fuel", "energ", "erdol", "kraftstoff", "tankstell", "brennstoff",
         "carburant", "raffinerie", "bransle", "drivmedel", "olja", "καυσιμ", "πετρελ", "διυλιστ", "ενεργ"],
        ["oil", "gas", "lng", "lpg", "gaz"],
        ["petroleum", "electricity", "gas ", "crude"],
    ),
    "transport_shipping": (
        ["driver", "truck", "logistic", "freight", "shipping", "vessel", "maritime", "seafar", "tanker",
         "aviation", "airline", "flight", "aircraft", "forwarder", "spedition", "fahrer", "lkw", "schiff",
         "seemann", "nautik", "flug", "chauffeur", "camion", "transport", "maritim", "navire", "aerien",
         "forare", "lastbil", "sjofart", "flyg", "οδηγ", "φορτηγ", "μεταφορ", "ναυτιλ", "πλοι", "ναυτικ",
         "αεροπορ", "πτησ"],
        ["pilot"],
        ["transport", "warehousing"],
    ),
    "tourism": (
        ["hotel", "restaurant", "touris", "hospitalit", "waiter", "waitress", "bartend", "housekeep", "kellner",
         "koch", "gastronom", "serveur", "cuisinier", "kock", "hotell", "ξενοδοχ", "εστιατορ", "τουρισ",
         "σερβιτορ", "μαγειρ", "ρεσεψιον"],
        ["cook"],
        ["accommodation", "food and beverage", "restaurant", "travel agency"],
    ),
    "manufacturing": (
        ["chemic", "chemi", "plastic", "fertili", "steel", "cement", "aluminium", "aluminum", "metal", "foundry",
         "smelt", "manufactur", "produktion", "fertigung", "kunststoff", "stahl", "industri", "usine", "plastique",
         "acier", "tillverk", "kemi", "plast", "χημικ", "πλαστικ", "βιομηχαν", "παραγωγ", "χαλυβ", "τσιμεντ",
         "αλουμιν"],
        ["production", "stal"],
        ["manufacture of", "basic metals", "chemicals", "plastics"],
    ),
    "control_health_edu": (
        ["nurs", "doctor", "physician", "teacher", "educator", "caregiver", "care assist", "care work", "childcare", "child care", "pflege", "arzt", "lehrer", "erzieh",
         "infirmi", "medecin", "enseignant", "soignant", "sjukskoters", "lakare", "larare", "undersk", "νοσηλευτ",
         "ιατρ", "γιατρ", "εκπαιδευτ", "καθηγητ", "δασκαλ", "νηπιαγωγ"],
        ["carer"],
        ["hospital", "human health", "education", "social work"],
    ),
}

# same cases as script 33: (source, months, first month counted as "after", label)
CASES = {
    "ev-gr": ("kariera.gr", ["2024-09", "2024-10", "2024-11", "2024-12"], "2024-11", "EU tariffs on Chinese EVs"),
    "ev-fr": ("lesjeudis.com", ["2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01"], "2024-11",
              "EU tariffs on Chinese EVs"),
    "ev-de": ("jobs.de", ["2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01"], "2024-11",
              "EU tariffs on Chinese EVs"),
    "oil-gr": ("kariera.gr", ["2026-01", "2026-02", "2026-03", "2026-04"], "2026-03", "Iran war / oil shock"),
    "oil-se": ("jobbland.se", ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"], "2026-03",
               "Iran war / oil shock"),
}


def norm(text):
    text = unicodedata.normalize("NFD", (text or "").lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def compile_group(stems, words):
    parts = [r"\b" + re.escape(norm(s)) + r"\w*" for s in stems]
    parts += [r"\b" + re.escape(norm(w)) + r"\b" for w in words]
    return re.compile("|".join(parts), re.UNICODE) if parts else None


PATTERNS = {g: (compile_group(st, wd), [norm(x) for x in sec]) for g, (st, wd, sec) in GROUPS.items()}


USE_SECTOR = False   # set from --with-sector; sector labels proved noisy (see docstring)


TEXT_CHARS = 400   # how much of the description (key "x", from script 38) is searched with the title


def classify(rec):
    title = norm((rec.get("t") or "") + " " + (rec.get("x") or "")[:TEXT_CHARS])
    sector = norm(rec.get("sec")) if USE_SECTOR else ""
    hit = {}
    for g, (rx, secs) in PATTERNS.items():
        by_title = bool(rx and rx.search(title))
        by_sector = bool(sector) and any(x in sector for x in secs)
        hit[g] = by_title or by_sector
    return hit


def wilson(k, n, z=1.96):
    if not n:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main():
    global USE_SECTOR, TEXT_CHARS, PAGES_PATH
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages-file", default=str(PAGES_PATH),
                    help="sampled pages: script 33's file (titles only) or script 38's file (with descriptions)")
    ap.add_argument("--text-chars", type=int, default=400,
                    help="characters of the description searched together with the title (needs script 38's file)")
    ap.add_argument("--with-sector", action="store_true",
                    help="also match the first sector label (default: titles only)")
    a = ap.parse_args()
    USE_SECTOR, TEXT_CHARS, PAGES_PATH = a.with_sector, a.text_chars, Path(a.pages_file)
    store, counts = load(PAGES_PATH), load(COUNTS_PATH)
    if not store:
        raise SystemExit("data/raw/stability_pages.json is missing: run script 33 first.")

    by = defaultdict(list)                       # (source, month) -> records
    for key, items in store.items():
        src, ym, _pg = key.split("|")
        by[(src, ym)].extend(items)

    res = {}                                     # (source, month) -> {group: hits}
    examples = defaultdict(lambda: defaultdict(list))
    for (src, ym), recs in by.items():
        h = defaultdict(int)
        for r in recs:
            for g, ok in classify(r).items():
                if ok:
                    h[g] += 1
                    t = (r.get("t") or "").strip()
                    if t and len(examples[src][g]) < 8 and t not in examples[src][g]:
                        examples[src][g].append(t)
        res[(src, ym)] = (len(recs), dict(h))

    L = ["# Pilot exposure groups: keyword counts in the sampled postings", "",
         "Pilot lists, titles (cut to 90 characters) and first sector labels only. Cells: matches / sampled postings "
         "(share), then the implied number of postings in the whole month (share x month total). Not results: "
         "the purpose is to see whether each group is large enough to analyse. Check the matched titles at the "
         "end for false positives.", ""]
    for src in sorted({s for s, _ in res}):
        months = sorted(m for s, m in res if s == src)
        L += [f"## {src}", "", "| month | sampled | " + " | ".join(GROUPS) + " |",
              "|---|---:|" + "---:|" * len(GROUPS)]
        for ym in months:
            n, h = res[(src, ym)]
            total = counts.get(src, {}).get(ym)
            cells = []
            for g in GROUPS:
                k = h.get(g, 0)
                imp = f" ≈ {round(k / n * total):,}" if total and n else ""
                cells.append(f"{k}/{n} ({100 * k / n:.1f}%){imp}" if n else "-")
            L.append(f"| {ym} | {n} | " + " | ".join(cells) + " |")
        L.append("")

    L += ["## Before and after each event (pooled months, Wilson 95% interval for the share)", "",
          "| case | group | pre: matches/n (share, interval) | post: matches/n (share, interval) |", "|---|---|---|---|"]
    for case, (src, months, after, _lab) in CASES.items():
        pre = [m for m in months if m < after and (src, m) in res]
        post = [m for m in months if m >= after and (src, m) in res]
        if not pre or not post:
            continue
        for g in GROUPS:
            row = []
            for side in (pre, post):
                n = sum(res[(src, m)][0] for m in side)
                k = sum(res[(src, m)][1].get(g, 0) for m in side)
                lo, hi = wilson(k, n)
                row.append(f"{k}/{n} ({100 * k / n:.1f}%, {100 * lo:.1f}-{100 * hi:.1f}%)")
            L.append(f"| {case} ({src}) | {g} | {row[0]} | {row[1]} |")
    L.append("")

    L += ["## Matched titles (first few per group, to spot false positives)", ""]
    for src in sorted(examples):
        L.append(f"### {src}")
        L.append("")
        for g in GROUPS:
            if examples[src][g]:
                L.append(f"- **{g}**: " + "; ".join(examples[src][g]))
        L.append("")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\nWritten: {REPORT_PATH}")


if __name__ == "__main__":
    main()
