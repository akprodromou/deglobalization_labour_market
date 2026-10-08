"""
Systematic page grid for OJA months: what is in the window, in result order?

Why: script 22 showed that OJA results come back ordered by `id`, and that ids
are laid out in blocks by occupation (one page = one ISCO 4-digit code). Random
pages therefore give a few homogeneous clusters (script 21). A SYSTEMATIC grid
(pages at evenly spaced positions through the whole window) works with that
ordering: every block is hit roughly in proportion to its length, so the share
of grid pages in an occupation estimates that occupation's share of the window.

For each window it fetches `--pages` evenly spaced result pages and stores a
small summary per page (not the postings) in data/raw/oja_page_grid.json:
first/last id, upload dates, ISCO 4-digit mix, share with `location_code`,
country codes, mean number of skills, experience levels, and how many postings
have a non-empty title or description.

Report: docs/oja_page_grid.md, with one row per page (position in window, id
range, dominant occupation, dates, country) and window-level summaries
(occupation-group shares, id ranges, share of pages with no location code).

Usage, from the repo root (credentials in env vars):
    python -m diagnostics.24_oja_page_grid
    python -m diagnostics.24_oja_page_grid --windows 2023-12 2024-01 --pages 24
    python -m diagnostics.24_oja_page_grid --windows 2019-06 --pages 30

Resumable: finished pages are skipped on re-run; failed pages are listed and
retried next time. Each page is one request, and deep pages are slow, so allow time.
Resolution: a window of N pages with k grid pages is sampled at one page in N/k;
blocks shorter than that can be missed.
"""

import argparse
import calendar
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

OUT_PATH = Path("data/raw/oja_page_grid.json")
REPORT_PATH = Path("docs/oja_page_grid.md")
PAGE_SIZE = 100
ISCO = re.compile(r"isco/C(\d+)")


def bounds(label):
    y, m = (int(x) for x in label.split("-"))
    last = min(date(y, m, calendar.monthrange(y, m)[1]), date.today())
    return date(y, m, 1).isoformat(), last.isoformat()


def grid_pages(n_pages, k):
    k = min(k, n_pages)
    return sorted({max(1, min(n_pages, round((j + 0.5) * n_pages / k))) for j in range(k)})


def first_isco(p):
    for entry in p.get("occupations") or []:
        m = ISCO.search(entry if isinstance(entry, str) else json.dumps(entry))
        if m:
            return m.group(1)
    return None


def summarise(items):
    ids = [p.get("id") for p in items if isinstance(p.get("id"), int)]
    dates = Counter(str(p.get("upload_date"))[:10] for p in items)
    isco4 = Counter(first_isco(p) for p in items)
    codes = Counter(p.get("location_code") for p in items)
    return {
        "n": len(items),
        "first_id": min(ids) if ids else None,
        "last_id": max(ids) if ids else None,
        "dates": dict(dates.most_common(3)),
        "isco4": {str(k): v for k, v in isco4.most_common(6)},
        "codes": {str(k): v for k, v in codes.most_common(4)},
        "with_code": sum(1 for p in items if p.get("location_code")),
        "mean_skills": sum(len(p.get("skills") or []) for p in items) / len(items) if items else 0,
        "title_nonempty": sum(1 for p in items if str(p.get("title") or "").strip()),
        "desc_nonempty": sum(1 for p in items if str(p.get("description") or "").strip()),
        "experience": dict(Counter(str(p.get("experience_level")) for p in items).most_common(3)),
    }


def load():
    return json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}


def save(data):
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(data, indent=1), encoding="utf-8")


def fetch(client, start, end, page):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": ["OJA"], "min_upload_date": start, "max_upload_date": end}
    r = client._post_with_retries(f"{BASE_URL}{JOBS_ENDPOINT}", {"page": page, "page_size": PAGE_SIZE}, form)
    payload = r.json()
    return payload.get("items", []), payload.get("count")


def collect(windows, k):
    from skillab_client import SkillabClient
    client = SkillabClient()
    data = load()
    for label in windows:
        start, end = bounds(label)
        w = data.setdefault(label, {"pages": {}})
        if "count" not in w:
            try:
                _, w["count"] = fetch(client, start, end, 1)
            except Exception as exc:
                print(f"  {label}: could not get count ({exc}); skipped")
                continue
            save(data)
        n_pages = -(-w["count"] // PAGE_SIZE)
        wanted = grid_pages(n_pages, k)
        w["grid"] = wanted
        print(f"  {label}: {w['count']:,} postings, {n_pages:,} pages; grid {len(wanted)} pages")
        for page in wanted:
            if str(page) in w["pages"]:
                continue
            try:
                items, _ = fetch(client, start, end, page)
            except Exception as exc:
                print(f"    page {page}: FAILED ({exc})")
                continue
            w["pages"][str(page)] = summarise(items)
            save(data)
            s = w["pages"][str(page)]
            top = next(iter(s["isco4"]), "-")
            print(f"    page {page}: ids {s['first_id']}..{s['last_id']}, ISCO {top}, {list(s['dates'])[:1]}")
        save(data)
    return data


def report(data, windows):
    out = ["# OJA page grid: window contents in result order", "",
           "Evenly spaced result pages (100 postings each) through each month. Results are ordered by "
           "`id`; ids form blocks by occupation, so grid pages are a systematic sample of the blocks. "
           "Script: `diagnostics/24_oja_page_grid.py`. Shares are shares of grid pages' postings; "
           "blocks shorter than one grid step can be missed.", ""]
    for label in windows:
        w = data.get(label)
        if not w or not w.get("pages"):
            continue
        n_pages = -(-w["count"] // PAGE_SIZE)
        pages = sorted(((int(p), s) for p, s in w["pages"].items()))
        out += [f"## {label}: {w['count']:,} postings, {len(pages)}/{len(w.get('grid', []))} grid pages fetched", ""]
        out.append("| Position | Page | id range | Top ISCO 4-digit (share of page) | Main dates | with location code | Main country |")
        out.append("|---|---|---|---|---|---|---|")
        major, isco4_all, total = Counter(), Counter(), 0
        no_code_pages = 0
        for page, s in pages:
            n = s["n"] or 1
            top = next(iter(s["isco4"].items()), ("-", 0))
            dates = ", ".join(list(s["dates"])[:2])
            ctry = next(iter(s["codes"]), "-")
            out.append(f"| {100 * page / n_pages:.0f}% | {page} | {s['first_id']}..{s['last_id']} | "
                       f"{top[0]} ({100 * top[1] / n:.0f}%) | {dates} | {100 * s['with_code'] / n:.0f}% | {ctry} |")
            for code, c in s["isco4"].items():
                total += c
                isco4_all[code] += c
                if code not in ("None", None):
                    major[code[0]] += c
            if s["with_code"] == 0:
                no_code_pages += 1
        got = sum(major.values())
        out += ["", f"Occupation (ISCO major group) shares across grid pages: " +
                (", ".join(f"{g}: {100 * c / got:.0f}%" for g, c in sorted(major.items())) if got else "none"),
                f"Top 4-digit codes: " + ", ".join(f"{c} ({100 * v / total:.0f}%)" for c, v in isco4_all.most_common(6)),
                f"Pages with no location code at all: {no_code_pages}/{len(pages)}.",
                f"Postings with a non-empty title: {sum(s['title_nonempty'] for _, s in pages)}; "
                f"with a non-empty description: {sum(s['desc_nonempty'] for _, s in pages)} "
                f"(of {sum(s['n'] for _, s in pages)}).", ""]
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--windows", nargs="+", default=["2023-12", "2024-01"])
    parser.add_argument("--pages", type=int, default=24)
    parser.add_argument("--analyse-only", action="store_true")
    args = parser.parse_args()
    data = load() if args.analyse_only else collect(args.windows, args.pages)
    text = report(data, args.windows)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text, encoding="utf-8")
    print("\n" + text)
    print(f"Written to {REPORT_PATH}")
    missing = [w for w in args.windows if data.get(w) and
               len(data[w]["pages"]) < len(data[w].get("grid", []))]
    if missing:
        print("Incomplete windows (re-run to retry missing pages): " + ", ".join(missing))


if __name__ == "__main__":
    main()
