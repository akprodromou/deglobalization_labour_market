"""
Second probe of the API keyword filter: does it search the title, is it
case-insensitive, how do 'and'/'or', plurals, stems and phrases behave?

Script 36 showed (kariera.gr, March 2026): `keywords_logic` accepts only the
lower-case values 'and' and 'or'; keyword counts come back in 1-4 seconds (the
month total took 25); 'driver' (525) and 'hotel' (1,748) match the DESCRIPTION
(96 and 99 of the first 100 hits contain the word there); 'energy' returns 0
while the stem 'energ' returns 12 with no hit in a title, although the titles
sampled by script 33 contain 'energ' words. That suggests the filter does not
search the title. This probe settles it and the other open points:

  A. Title test: take words that occur in a posting's TITLE but not in its
     DESCRIPTION, query the filter with each word and see whether that posting
     comes back. Back = the title (or another field containing it) is searched.
  B. Case: hotel / Hotel / HOTEL.
  C. Logic with non-zero counts: 'hotel' + 'driver' with 'or' and with 'and'
     (or >= max of the two, and <= min of the two).
  D. Plural and stem: hotel / hotels / hote.
  E. Phrase: 'hotel manager' as one keyword, and 'hotel' + 'manager' with 'and'.

Usage, from the repo root:
    python -m diagnostics.37_keyword_filter_probe2
    python -m diagnostics.37_keyword_filter_probe2 --source jobs.de --month 2024-10

Output: docs/keyword_filter_probe2.md. About 20 requests, mostly a few seconds.
"""

import argparse
import calendar
import re
import time
from datetime import date
from pathlib import Path

REPORT_PATH = Path("docs/keyword_filter_probe2.md")
WORD = re.compile(r"[^\W\d_]{5,}", re.UNICODE)


def post(client, source, lo, hi, kws=None, logic=None, page=1):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [source], "min_upload_date": lo, "max_upload_date": hi}
    if kws:
        form["keywords"] = kws
    if logic:
        form["keywords_logic"] = logic
    t0 = time.time()
    r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": page, "page_size": 100}, data=form,
                            timeout=240)
    dt = time.time() - t0
    if r.status_code != 200:
        return None, [], dt, f"HTTP {r.status_code}: {r.text[:100]}"
    j = r.json()
    return j.get("count"), j.get("items", []), dt, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="kariera.gr")
    ap.add_argument("--month", default="2026-03")
    args = ap.parse_args()

    from skillab_client import SkillabClient
    y, m = (int(x) for x in args.month.split("-"))
    lo, hi = date(y, m, 1).isoformat(), date(y, m, calendar.monthrange(y, m)[1]).isoformat()
    client = SkillabClient()
    src = args.source
    L = [f"# Keyword filter probe 2: {src}, {args.month}", ""]

    # A. title test
    L += ["## A. Is the title searched?", "",
          "Words taken from a posting's title that do not occur in its description (case-insensitive). "
          "'returned' = the posting is among the first 100 results for that word.", "",
          "| word | posting id | count | returned | note |", "|---|---:|---:|---|---|"]
    try:
        _, items, _, _ = post(client, src, lo, hi, page=1)
    except Exception as exc:
        items = []
        L.append(f"| - | - | - | - | could not fetch the base page: {exc} |")
    picked = []
    for p in items:
        title, desc = str(p.get("title") or ""), str(p.get("description") or "").lower()
        for w in WORD.findall(title.lower()):
            if w not in desc and all(w != q[0] for q in picked):
                picked.append((w, p["id"]))
                break
        if len(picked) >= 6:
            break
    for w, pid in picked:
        try:
            count, res, _, note = post(client, src, lo, hi, [w])
        except Exception as exc:
            L.append(f"| {w} | {pid} | - | - | FAILED: {exc} |")
            continue
        ids = {q.get("id") for q in res}
        if count is None:
            ret = "-"
        elif pid in ids:
            ret = "yes"
        elif count > 100:
            ret = "not in first 100 (inconclusive)"
        else:
            ret = "NO"
        L.append(f"| {w} | {pid} | {count} | {ret} | {note} |")
        print(L[-1])

    # B-E: counts
    probes = [
        ("B. case", [("hotel", ["hotel"], None), ("Hotel", ["Hotel"], None), ("HOTEL", ["HOTEL"], None)]),
        ("C. logic", [("hotel", ["hotel"], None), ("driver", ["driver"], None),
                      ("hotel or driver", ["hotel", "driver"], "or"), ("hotel and driver", ["hotel", "driver"], "and")]),
        ("D. plural and stem", [("hotel", ["hotel"], None), ("hotels", ["hotels"], None), ("hote", ["hote"], None)]),
        ("E. phrase", [("'hotel manager' as one keyword", ["hotel manager"], None),
                       ("hotel and manager", ["hotel", "manager"], "and"), ("manager", ["manager"], None)]),
    ]
    for title, rows in probes:
        L += ["", f"## {title}", "", "| probe | keywords | logic | count | seconds | note |", "|---|---|---|---:|---:|---|"]
        for label, kws, logic in rows:
            try:
                count, _, dt, note = post(client, src, lo, hi, kws, logic)
            except Exception as exc:
                count, dt, note = None, 0.0, f"FAILED: {exc}"
            L.append(f"| {label} | {kws} | {logic or '-'} | {'-' if count is None else f'{count:,}'} | {dt:.0f} | {note} |")
            print(L[-1])

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"\nWritten: {REPORT_PATH}")


if __name__ == "__main__":
    main()
