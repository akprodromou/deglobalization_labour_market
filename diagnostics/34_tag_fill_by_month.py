"""
Why are occupation, sector and skill tags empty in 2026 kariera.gr postings?

Script 33 found occupations, sectors and skills empty in every sampled kariera.gr
posting of January-April 2026, while script 31 found them filled in 58%, 52% and
57% of the postings it sampled across the whole unfiltered result set. This
script separates three explanations:
  (a) tagging depends on the upload date (recent postings are not tagged yet,
      or tagging started/stopped at some date);
  (b) date-filtered queries return postings without the nested tag lists;
  (c) the earlier fill rates came from a different part of the source.

Part 1: for each calendar month with data, fetch one page from the middle of
        the date-filtered result and report the tag fill rates.
Part 2: fetch evenly spaced pages of the UNFILTERED result set and report, per
        page, the range of upload dates and the tag fill rates. If Part 2 shows
        old pages tagged and new pages untagged, explanation (a) holds; if the
        newest unfiltered pages are tagged but the same months are empty in
        Part 1, explanation (b) holds.

Usage, from the repo root:
    python -m diagnostics.34_tag_fill_by_month
    python -m diagnostics.34_tag_fill_by_month --source jobbland.se --pages 8

Resumable (data/raw/tag_fill.json). Output: docs/tag_fill_by_month.md
Each request takes 20-70 s; the default run is about 30 requests.
"""

import argparse
import calendar
import json
import math
import time
from datetime import date
from pathlib import Path

OUT = Path("data/raw/tag_fill.json")
COUNTS = Path("data/raw/event_window_counts.json")
REPORT = Path("docs/tag_fill_by_month.md")
PAGE_SIZE = 100


def load(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def save(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d), encoding="utf-8")


def fetch(client, source, page, lo=None, hi=None, attempts=3):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [source]}
    if lo:
        form["min_upload_date"], form["max_upload_date"] = lo, hi
    last = None
    for i in range(1, attempts + 1):
        try:
            r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": page, "page_size": PAGE_SIZE},
                                    data=form, timeout=240)
            r.raise_for_status()
            j = r.json()
            return j.get("items", []), j.get("count")
        except Exception as exc:
            last = exc
            print(f"    attempt {i}/{attempts} failed: {exc}")
            time.sleep(5 * i)
    raise last


def stats(items):
    n = len(items)
    if not n:
        return None
    dates = sorted(str(p.get("upload_date") or "")[:10] for p in items if p.get("upload_date"))
    ne = lambda v: bool(v)
    return {"n": n,
            "occ": round(100 * sum(ne(p.get("occupations")) for p in items) / n),
            "sec": round(100 * sum(ne(p.get("sectors")) for p in items) / n),
            "sk": round(100 * sum(ne(p.get("skills")) for p in items) / n),
            "dmin": dates[0] if dates else "", "dmax": dates[-1] if dates else "",
            "id_min": min((p["id"] for p in items if isinstance(p.get("id"), int)), default=None),
            "id_max": max((p["id"] for p in items if isinstance(p.get("id"), int)), default=None)}


def months_with_data(source):
    c = load(COUNTS).get(source, {})
    ms = sorted(m for m, v in c.items() if v)
    return ms or [f"{y}-{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="kariera.gr")
    ap.add_argument("--pages", type=int, default=8, help="unfiltered pages (Part 2)")
    args = ap.parse_args()

    from skillab_client import SkillabClient
    client = SkillabClient()
    store = load(OUT)
    src = args.source

    for ym in months_with_data(src):
        key = f"{src}|month|{ym}"
        if key in store:
            continue
        y, m = int(ym[:4]), int(ym[5:])
        lo, hi = date(y, m, 1).isoformat(), date(y, m, calendar.monthrange(y, m)[1]).isoformat()
        try:
            _, n = fetch(client, src, 1, lo, hi)
            if not n:
                continue
            page = max(1, math.ceil(n / PAGE_SIZE) // 2)
            items, _ = fetch(client, src, page, lo, hi)
        except Exception as exc:
            print(f"  {ym}: FAILED ({exc})")
            continue
        store[key] = dict(stats(items) or {}, page=page, count=n)
        save(OUT, store)
        print(f"  {ym}: {store[key]}")

    key0 = f"{src}|total"
    if key0 not in store:
        try:
            _, total = fetch(client, src, 1)
            store[key0] = total
            save(OUT, store)
        except Exception as exc:
            print(f"  total FAILED ({exc})")
    total = store.get(key0)
    if total:
        n_pages = math.ceil(total / PAGE_SIZE)
        k = min(args.pages, n_pages)
        for pg in sorted({max(1, min(n_pages, round((j + 0.5) * n_pages / k))) for j in range(k)}):
            key = f"{src}|page|{pg}"
            if key in store:
                continue
            try:
                items, _ = fetch(client, src, pg)
            except Exception as exc:
                print(f"  unfiltered page {pg}: FAILED ({exc})")
                continue
            store[key] = dict(stats(items) or {}, n_pages=n_pages)
            save(OUT, store)
            print(f"  unfiltered page {pg}/{n_pages}: {store[key]}")

    L = [f"# Tag fill rates by month, {src}", "",
         "Share of sampled postings with a non-empty `occupations`, `sectors` and `skills` list.", "",
         "## Part 1: date-filtered, one middle page per month", "",
         "| month | postings in month | sampled | occupations | sectors | skills |", "|---|---:|---:|---:|---:|---:|"]
    for k, v in sorted(store.items()):
        if k.startswith(f"{src}|month|") and v.get("n"):
            L.append(f"| {k.split('|')[2]} | {v['count']:,} | {v['n']} | {v['occ']}% | {v['sec']}% | {v['sk']}% |")
    L += ["", "## Part 2: unfiltered result set, evenly spaced pages (ordered by id)", "",
          "| page | ids | upload_date range | sampled | occupations | sectors | skills |", "|---:|---|---|---:|---:|---:|---:|"]
    pages = [(int(k.split("|")[2]), v) for k, v in store.items() if k.startswith(f"{src}|page|") and v.get("n")]
    for pg, v in sorted(pages):
        L.append(f"| {pg} | {v['id_min']}-{v['id_max']} | {v['dmin'] or '-'} to {v['dmax'] or '-'} | {v['n']} | "
                 f"{v['occ']}% | {v['sec']}% | {v['sk']}% |")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\nWritten: {REPORT}")


if __name__ == "__main__":
    main()
