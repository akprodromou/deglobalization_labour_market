"""
OJA postings per ISCO code per window, from filtered COUNT queries.

Why: the page grid (script 24) showed that each OJA month is made of a few
occupation blocks, and that the blocks change between months (December 2023:
chemical/laboratory/environment codes; January 2024: roughly two thirds ISCO
251x software/systems, the rest marketing, finance, education). If so, the
monthly OJA totals reflect which occupation batches exist, not the labour
market. This script measures it for the whole population: for each ISCO code
seen so far, how many OJA postings does each window hold?

Step 1, check that the occupation filter works and which value format it takes:
    python -m diagnostics.25_oja_counts_by_occupation --probe
This asks for ISCO 2512 in January 2024 in three formats and prints the counts.
A format is working if its count is above 0 and below the window total
(276,271); the same number as the total means the filter was ignored. Then pass
the working one as --format.

Step 2, the counts (default: December 2023 and January 2024, 18 codes):
    python -m diagnostics.25_oja_counts_by_occupation --format uri
    python -m diagnostics.25_oja_counts_by_occupation --format uri --windows 2019 2020 2021 2022 2023 2024
Windows are 'YYYY' (a year) or 'YYYY-MM' (a month). Resumable: successful counts
are saved to data/raw/oja_occupation_counts.json; failures show as '?'.
Output: docs/oja_occupation_counts.md.
"""

import argparse
import calendar
import json
from datetime import date
from pathlib import Path

OUT_PATH = Path("data/raw/oja_occupation_counts.json")
REPORT_PATH = Path("docs/oja_occupation_counts.md")
URI = "http://data.europa.eu/esco/isco/C{}"

# ISCO-08 codes seen in script 21/22/24 pages, with ISCO-08 titles
CODES = {
    "3141": "Life science technicians",
    "3116": "Chemical engineering technicians",
    "2113": "Chemists",
    "2145": "Chemical engineers",
    "2133": "Environmental protection professionals",
    "8131": "Chemical products plant and machine operators",
    "8114": "Cement, stone and other mineral products machine operators",
    "7124": "Insulation workers",
    "2511": "Systems analysts",
    "2512": "Software developers",
    "2513": "Web and multimedia developers",
    "2514": "Applications programmers",
    "2519": "Software and applications developers n.e.c.",
    "2431": "Advertising and marketing professionals",
    "2330": "Secondary education teachers",
    "3312": "Credit and loans officers",
    "1211": "Finance managers",
    "2413": "Financial investment advisers",
}


def bounds(token):
    if len(token) == 4:
        y = int(token)
        start, end = date(y, 1, 1), date(y, 12, 31)
    else:
        y, m = (int(x) for x in token.split("-"))
        start, end = date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1])
    return start.isoformat(), min(end, date.today()).isoformat()


def occupation_value(code, fmt):
    return {"uri": URI.format(code), "code": f"C{code}", "number": code}[fmt]


def count(client, start, end, value=None):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": ["OJA"], "min_upload_date": start, "max_upload_date": end}
    if value is not None:
        form["occupation_ids"] = value
    r = client._post_with_retries(f"{BASE_URL}{JOBS_ENDPOINT}", {"page": 1, "page_size": 100}, form)
    return r.json().get("count", 0)


def load():
    return json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}


def save(d):
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(d, indent=2), encoding="utf-8")


def probe(client):
    start, end = bounds("2024-01")
    print("Window 2024-01, ISCO 2512 (expected: a large share of the total, not equal to it)")
    try:
        print(f"  unfiltered total: {count(client, start, end):,}")
    except Exception as exc:
        print(f"  unfiltered total: FAILED ({exc})")
    for fmt in ("uri", "code", "number"):
        value = occupation_value("2512", fmt)
        try:
            print(f"  --format {fmt:<6} ({value}): {count(client, start, end, value):,}")
        except Exception as exc:
            print(f"  --format {fmt:<6} ({value}): FAILED ({exc})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--format", choices=["uri", "code", "number"], default="uri")
    parser.add_argument("--windows", nargs="+", default=["2023-12", "2024-01"])
    parser.add_argument("--codes", nargs="+", default=list(CODES))
    args = parser.parse_args()

    from skillab_client import SkillabClient
    client = SkillabClient()
    if args.probe:
        probe(client)
        return

    data = load()
    for token in args.windows:
        start, end = bounds(token)
        w = data.setdefault(args.format, {}).setdefault(token, {})
        for key in ["TOTAL"] + args.codes:
            if key in w:
                continue
            value = None if key == "TOTAL" else occupation_value(key, args.format)
            try:
                w[key] = count(client, start, end, value)
            except Exception as exc:
                print(f"  {token} {key}: FAILED ({exc})")
                continue
            save(data)
            print(f"  {token} {key}: {w[key]:,}")

    res = data.get(args.format, {})
    lines = ["# OJA postings per ISCO code and window (population counts)", "",
             f"Filtered count queries on source `OJA`, occupation filter format `{args.format}`. "
             "'Listed' = sum over the listed codes; 'other' = total minus listed.", ""]
    head = "| ISCO | Occupation | " + " | ".join(args.windows) + " |"
    lines += [head, "|---|---|" + "---|" * len(args.windows)]
    for code in args.codes:
        cells = []
        for t in args.windows:
            v = res.get(t, {}).get(code)
            cells.append("?" if v is None else f"{v:,}")
        lines.append(f"| {code} | {CODES.get(code, '')} | " + " | ".join(cells) + " |")
    listed, totals, warn = {}, {}, []
    for t in args.windows:
        w = res.get(t, {})
        totals[t] = w.get("TOTAL")
        vals = [w.get(c) for c in args.codes]
        listed[t] = sum(v for v in vals if v is not None) if all(v is not None for v in vals) else None
        if totals[t] and any(w.get(c) == totals[t] for c in args.codes):
            warn.append(t)
    lines.append("| | **Listed codes** | " + " | ".join("?" if listed[t] is None else f"{listed[t]:,}" for t in args.windows) + " |")
    lines.append("| | **Window total** | " + " | ".join("?" if totals[t] is None else f"{totals[t]:,}" for t in args.windows) + " |")
    lines.append("| | **Other (total - listed)** | " + " | ".join(
        "?" if listed[t] is None or totals[t] is None else f"{totals[t] - listed[t]:,}" for t in args.windows) + " |")
    lines.append("")
    if warn:
        lines.append("> WARNING: for " + ", ".join(warn) + " a code's count equals the window total, "
                     "so the occupation filter may be ignored with `--format " + args.format + "`. "
                     "Run `--probe` and try another format.\n")
    text = "\n".join(lines) + "\n"
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text, encoding="utf-8")
    print("\n" + text)
    print(f"Written to {REPORT_PATH}. Re-run to retry any '?'.")


if __name__ == "__main__":
    main()
