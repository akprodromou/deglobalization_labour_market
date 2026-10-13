"""
Where are the postings with NO upload_date, and what do they look like?

Script 29 found that `eures` (158,689) and `eures-escox` (647,773) hold postings
with no upload_date: the all-time count is larger than the count inside a
1900-2100 window. Every date-windowed query we have run, and the trend endpoint,
leaves them out. This script samples them.

For each source it fetches evenly spaced result pages from the UNFILTERED result
set (page_size=100; results are ordered by id) and records per page: id range, how
many postings have no upload_date, the years of the dated ones, countries, and,
for undated postings, a short text snippet. It also counts four-digit years
(2010-2029) mentioned in the title/description, separately for dated and undated
postings. The dated postings are the calibration: a posting dated 2026 should
mention 2025/2026, so if undated postings mention mostly 2019/2020, that points
to old postings.

Usage, from the repo root (credentials in env vars):
    python -m diagnostics.30_undated_postings_grid
    python -m diagnostics.30_undated_postings_grid --sources eures --pages 40

Resumable: finished pages are kept in data/raw/undated_grid.json; re-run to fill
failed ones. Output: docs/undated_postings_grid.md. Snippets are saved locally in
data/raw/undated_grid.json (not committed by default; check .gitignore).
"""

import argparse
import json
import re
import time
from collections import Counter
from pathlib import Path

OUT_PATH = Path("data/raw/undated_grid.json")
REPORT_PATH = Path("docs/undated_postings_grid.md")
PAGE_SIZE = 100
YEAR = re.compile(r"\b(20[12]\d)\b")


def grid_pages(n_pages, k):
    k = min(k, n_pages)
    return sorted({max(1, min(n_pages, round((j + 0.5) * n_pages / k))) for j in range(k)})


def fetch(client, source, page, attempts=3):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    last = None
    for i in range(1, attempts + 1):
        try:
            r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": page, "page_size": PAGE_SIZE},
                                    data={"sources": [source]}, timeout=120)
            r.raise_for_status()
            p = r.json()
            return p.get("items", []), p.get("count")
        except Exception as exc:
            last = exc
            print(f"    attempt {i}/{attempts} failed: {exc}")
            time.sleep(5 * i)
    raise last


def text_of(p):
    return f"{p.get('title') or ''} {p.get('description') or ''}"


def summarise(items):
    undated = [p for p in items if not p.get("upload_date")]
    dated = [p for p in items if p.get("upload_date")]
    ids = [p["id"] for p in items if isinstance(p.get("id"), int)]
    yrs_dated = Counter(str(p["upload_date"])[:4] for p in dated)
    ctry = Counter(p.get("location_code") for p in items)
    mention_dated, mention_undated = Counter(), Counter()
    for p in dated:
        for y in set(YEAR.findall(text_of(p))):
            mention_dated[y] += 1
    for p in undated:
        for y in set(YEAR.findall(text_of(p))):
            mention_undated[y] += 1
    snippets = [{"id": p.get("id"), "title": str(p.get("title") or "")[:90],
                 "description": str(p.get("description") or "")[:220].replace("\n", " "),
                 "location": p.get("location"), "organization": p.get("organization"),
                 "type": p.get("type"), "experience_level": p.get("experience_level")}
                for p in undated[:2]]
    return {"n": len(items), "undated": len(undated), "first_id": min(ids) if ids else None,
            "last_id": max(ids) if ids else None, "years_dated": dict(yrs_dated.most_common(4)),
            "countries": {str(k): v for k, v in ctry.most_common(3)},
            "mentions_dated": dict(mention_dated), "mentions_undated": dict(mention_undated),
            "snippets": snippets}


def load():
    return json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}


def save(d):
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")


def collect(sources, k):
    from skillab_client import SkillabClient
    client = SkillabClient()
    data = load()
    for source in sources:
        w = data.setdefault(source, {"pages": {}})
        if "count" not in w:
            try:
                _, w["count"] = fetch(client, source, 1)
            except Exception as exc:
                print(f"  {source}: could not get count ({exc})")
                continue
            save(data)
        n_pages = -(-w["count"] // PAGE_SIZE)
        wanted = grid_pages(n_pages, k)
        w["grid"] = wanted
        print(f"  {source}: {w['count']:,} postings, {n_pages:,} pages; grid {len(wanted)} pages")
        for page in wanted:
            if str(page) in w["pages"]:
                continue
            try:
                items, _ = fetch(client, source, page)
            except Exception as exc:
                print(f"    page {page}: FAILED ({exc})")
                continue
            w["pages"][str(page)] = summarise(items)
            save(data)
            s = w["pages"][str(page)]
            print(f"    page {page}: ids {s['first_id']}..{s['last_id']}, undated {s['undated']}/{s['n']}")
    return data


def report(data, sources):
    out = ["# Postings with no upload_date: where they sit and what they say", "",
           "Evenly spaced pages from the unfiltered result set, ordered by id. "
           "Script: `diagnostics/30_undated_postings_grid.py`.", ""]
    for source in sources:
        w = data.get(source)
        if not w or not w.get("pages"):
            continue
        n_pages = -(-w["count"] // PAGE_SIZE)
        pages = sorted((int(p), s) for p, s in w["pages"].items())
        tot = sum(s["n"] for _, s in pages)
        und = sum(s["undated"] for _, s in pages)
        out += [f"## {source}: {w['count']:,} postings, {len(pages)}/{len(w.get('grid', []))} grid pages", "",
                f"Undated share of grid postings: {und}/{tot} ({100 * und / tot:.0f}%).", "",
                "| Position | Page | id range | Undated | Years of dated postings | Countries |",
                "|---|---|---|---|---|---|"]
        for page, s in pages:
            out.append(f"| {100 * page / n_pages:.0f}% | {page} | {s['first_id']}..{s['last_id']} | "
                       f"{s['undated']}/{s['n']} | {s['years_dated'] or '-'} | {s['countries']} |")
        md, mu = Counter(), Counter()
        for _, s in pages:
            md.update(s["mentions_dated"])
            mu.update(s["mentions_undated"])
        fmt = lambda c: ", ".join(f"{y}: {n}" for y, n in sorted(c.items())) or "none"
        out += ["", f"Years mentioned in text, dated postings (calibration): {fmt(md)}",
                f"Years mentioned in text, undated postings: {fmt(mu)}", "", "Sample undated postings:", ""]
        shown = 0
        for _, s in pages:
            for sn in s["snippets"]:
                if shown >= 8:
                    break
                out.append(f"- id {sn['id']}: {sn['title']!r} | {sn['location']} | {sn['organization']} | "
                           f"{sn['description']!r}")
                shown += 1
        out.append("")
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", nargs="+", default=["eures", "eures-escox"])
    parser.add_argument("--pages", type=int, default=40)
    parser.add_argument("--analyse-only", action="store_true")
    args = parser.parse_args()
    data = load() if args.analyse_only else collect(args.sources, args.pages)
    text = report(data, args.sources)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text, encoding="utf-8")
    print("\n" + text)
    print(f"Written to {REPORT_PATH}")


if __name__ == "__main__":
    main()
