"""
Month 3: download a day-stratified corpus of full postings for one source.

Why stratified by day. The page sample of script 50 takes a few pages of
100 postings that sit next to each other in the server's date order, so each
page is about one day. Postings from one day share employers and batches, and
the sample then describes a few days, not the month. Here every calendar day
of every month is a stratum: for each day the script asks for that day only,
learns the day's total from the response (`count`), and fetches a random page
of it. Each stored record keeps the day's total, so that every posting can be
weighted by (day total / postings taken that day) and a month's shares are
estimated without bias from the unequal size of days.

What is stored. The whole item as returned (title, description, dates,
location, type and every other field), one JSON line per request, in
data/raw/corpus_<source>_<first>_<last>.jsonl. data/raw is not tracked by git.
Postings contain text written by employers (names, contact details), so the
file is personal data: it stays on this machine.

Resumable. A day is skipped when its line is already in the file. Rerun the
same command after an interruption or a failure; days that failed are
listed at the end.

Before the full run, check how the date filter treats a single day:
    python -m diagnostics.52_download_corpus --dry-day 2026-03-10
It prints the total for the window [day, day] and for [day, day+1]. If the
second is about twice the first, `max_upload_date` includes the end date and
single-day windows are valid (the default). If the first total is 0, the end
date is exclusive and the script needs the next day as the end date.

Run (project root, venv active, .env present; takes hours, can run overnight):
    python -m diagnostics.52_download_corpus --first 2026-01 --last 2026-08
    python -m diagnostics.52_download_corpus --first 2026-01 --last 2026-08 --pages-per-day 2

Options: --per-day (postings taken per day, default 100), --pages-per-day
(that many separate random pages of per-day/pages-per-day postings each),
--timeout (seconds per request, default 120).
"""

import argparse
import calendar
import json
import math
import random
import time
from datetime import date, timedelta
from pathlib import Path

RAW_DIR = Path("data/raw")
COUNTS_PATH = RAW_DIR / "event_window_counts.json"   # month totals from script 50


def days_of(ym):
    y, m = int(ym[:4]), int(ym[5:])
    return [date(y, m, d) for d in range(1, calendar.monthrange(y, m)[1] + 1)]


def months_between(a, b):
    y, m = int(a[:4]), int(a[5:])
    out = []
    while f"{y:04d}-{m:02d}" <= b:
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def fetch(client, source, lo, hi, page, page_size, timeout, attempts=3):
    """One request; returns (items, count). Raises after the last attempt."""
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    last = None
    for i in range(1, attempts + 1):
        try:
            r = client.session.post(
                f"{BASE_URL}{JOBS_ENDPOINT}",
                params={"page": page, "page_size": page_size},
                data={"sources": [source], "min_upload_date": lo,
                      "max_upload_date": hi}, timeout=timeout)
            r.raise_for_status()
            j = r.json()
            return j.get("items", []), j.get("count")
        except Exception as exc:
            last = exc
            print(f"    attempt {i}/{attempts} failed: {exc}")
            time.sleep(5 * i)
    raise last


def page_for(u, total, page_size):
    n_pages = max(1, math.ceil(total / page_size))
    return min(n_pages, int(u * n_pages) + 1), n_pages


def load_done(path):
    done = {}
    if path.exists():
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    done.setdefault(r["day"], []).append(r)
    return done


def day_is_done(records, rng_seed, ppd, page_size):
    """A day is complete when it has one record for each of its ppd draws and
    each stored page is the page its draw gives for the stored total."""
    if not records:
        return False
    total = records[0]["total"]
    if total == 0:
        return True
    rng = random.Random(rng_seed)
    v = rng.random()
    need = {page_for((k + v) / ppd, total, page_size)[0] for k in range(ppd)}
    have = {r["page"] for r in records}
    return need <= have


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--source", default="jobbland.se")
    ap.add_argument("--first", default="2026-01")
    ap.add_argument("--last", default="2026-08")
    ap.add_argument("--per-day", type=int, default=100)
    ap.add_argument("--pages-per-day", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--dry-day", default=None, help="YYYY-MM-DD: print window totals and stop")
    args = ap.parse_args()

    from skillab_client import SkillabClient
    client = SkillabClient()

    if args.dry_day:
        d = date.fromisoformat(args.dry_day)
        for lo, hi in ((d, d), (d, d + timedelta(days=1))):
            _, c = fetch(client, args.source, lo.isoformat(), hi.isoformat(), 1, 1, args.timeout)
            print(f"window [{lo}, {hi}]: {c} postings")
        print("If the second total is about twice the first, the end date is inclusive "
              "and the default (window = the single day) is right.")
        return

    ppd = max(1, args.pages_per_day)
    page_size = max(1, args.per_day // ppd)
    out_path = RAW_DIR / f"corpus_{args.source}_{args.first}_{args.last}.jsonl"
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    done = load_done(out_path)
    failed = []
    streak = 0
    month_counts = json.loads(COUNTS_PATH.read_text(encoding="utf-8")) if COUNTS_PATH.exists() else {}

    for ym in months_between(args.first, args.last):
        taken = 0
        for d in days_of(ym):
            day = d.isoformat()
            seed = f"{args.source}|{day}"
            if day_is_done(done.get(day), seed, ppd, page_size):
                continue
            # the draw is fixed per day by the seed, so a rerun repeats it
            v = random.Random(seed).random()
            n_est = None
            mt = month_counts.get(args.source, {}).get(ym)
            if mt:
                n_est = max(1, mt // len(days_of(ym)))
            records = list(done.get(day, []))
            total = records[0]["total"] if records else None
            for k in range(ppd):
                u = (k + v) / ppd
                if total is None:
                    guess = max(1, math.ceil((n_est or page_size) / page_size))
                    page = min(guess, int(u * guess) + 1)
                else:
                    page, _ = page_for(u, total, page_size)
                if any(r["page"] == page for r in records):
                    continue
                try:
                    items, count = fetch(client, args.source, day, day, page, page_size, args.timeout)
                except Exception as exc:
                    print(f"  {day}: FAILED ({exc})")
                    failed.append(day)
                    break
                if count is None:
                    count = len(items)
                if total is None or total != count:
                    total = count
                    right, _ = page_for(u, total, page_size)
                    if right != page:   # the guess was off: fetch the right page
                        if total == 0:
                            items = []
                        else:
                            try:
                                items, _ = fetch(client, args.source, day, day, right, page_size, args.timeout)
                            except Exception as exc:
                                print(f"  {day}: FAILED ({exc})")
                                failed.append(day)
                                break
                        page = right
                rec = {"source": args.source, "day": day, "total": total, "page": page,
                       "page_size": page_size, "n": len(items), "items": items}
                records.append(rec)
                with open(out_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                taken += len(items)
                print(f"  {day}: total {total:,}, page {page}, took {len(items)}")
            done[day] = records
            streak = streak + 1 if day in failed[-1:] else 0
            if streak >= 5:
                print("  five days in a row failed: the server looks down. Stopping; "
                      "rerun the same command later.")
                break
        else:
            continue
        break

    # per-month check against the monthly totals saved by script 50
    done = load_done(out_path)
    print("\nMonth check (sum of day totals against the month total of script 50):")
    for ym in months_between(args.first, args.last):
        s = sum(r[0]["total"] for dday, r in done.items() if dday.startswith(ym) and r)
        n = sum(x["n"] for dday, r in done.items() if dday.startswith(ym) for x in r)
        days_done = sum(1 for dday in done if dday.startswith(ym))
        mt = month_counts.get(args.source, {}).get(ym)
        flag = "" if mt is None or abs(s - mt) <= 0.02 * mt else "  <-- differs by more than 2%"
        print(f"  {ym}: {days_done}/{len(days_of(ym))} days, day totals sum {s:,}, "
              f"month total {mt if mt is not None else 'n/a'}, postings taken {n:,}{flag}")
    if failed:
        print(f"\n{len(set(failed))} days failed; rerun the same command: "
              + ", ".join(sorted(set(failed))[:20]))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
