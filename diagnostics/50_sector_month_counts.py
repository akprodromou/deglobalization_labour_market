"""
Month 3, step 1: how many postings does each sector have in each month around
the three primary events? (Estimated from page samples, optimistic: only
postings that carry a sector tag, or have text, can be used.)

Primary events (author's choice, report Section 9.9; updated 27 October 2026):
  crma        EU Critical Raw Materials Act, 23 May 2024      jobbland.se
  steelapply  EU steel import regulation, applies 1 Jul 2026  jobbland.se   (primary, reshoring)
  steelvote   same regulation, Parliament vote 19 May 2026    jobbland.se   (secondary: anticipation)
  accelerate  AccelerateEU, 22 Apr 2026                       kariera.gr, jobbland.se

The EU Steel and Metals Action Plan (19 Mar 2025) was removed by the author on
27 October 2026 and is no longer an event here. Its earlier run is kept in
docs/sector_month_counts_steel.md for the record.

THE RULE (supervisor, 17 October 2026: "a minimum of postings per sector-month,
fixed before the results are seen"): a sector counts as usable for an event in
a source only if its estimated number of postings is at least MIN_N in EVERY
month of the pre-window and of the post-window (the event month itself is
left out of both). MIN_N is set below, once. To change it, change it, commit
the file, and only then run the script, so the number is on record before the
results exist. The output also shows a looser pooled reading (sum of the
pre-window months and of the post-window months) for information; the rule
is the strict one.

What is estimated, and how
--------------------------
For every source and month the script takes the month's posting count (closed
calendar window, the same probe as script 32) and fetches PAGES evenly spaced
pages of 100 postings (compact fields only, stored in
data/raw/stability_pages.json, the same file and key format as script 33, so
pages fetched by that script are reused). A sector's monthly count is
estimated as (month total) x (share of the sampled postings with that sector
as FIRST sector tag), with a Wilson 95% interval on the share. A cell is
marked "~" when the interval straddles MIN_N.

Limits, stated up front:
  * Only the first sector tag of a posting is used, and the labels are at mixed
    NACE levels (report 13.3); the real sector grouping will come from the
    validated classifier, so these counts are a first, optimistic screen.
  * Months after the tags stop (kariera.gr from December 2025, jobbland.se from
    October 2025) have no sector tags at all. For them the table gives only the
    number of postings with a description of at least MIN_TEXT characters, which
    is the most a text classifier can label. AccelerateEU sits entirely there.
  * Pages are evenly spaced in id order, which approximates a random sample
    but is not one (in the newest ids the order no longer follows the date).
  * Duplicates are not removed here (deduplication by content is a separate
    step), so the counts are upper bounds.

Usage, from the repo root (credentials in .env or env vars):
    python -m diagnostics.50_sector_month_counts                 # all events
    python -m diagnostics.50_sector_month_counts --events crma
    python -m diagnostics.50_sector_month_counts --offline       # report from files only

Resumable. Each page request takes 20-70 s; the full run is up to about 135
requests (one to two hours); run one event at a time if you prefer.
Output: docs/sector_month_counts_<event>.md (one file per event; a combined
sector_month_counts.md when several events are run together)
"""

import argparse
import calendar
import json
import math
import time
from collections import Counter
from datetime import date
from pathlib import Path

MIN_N = 100        # THE RULE: minimum estimated postings per sector-month
MIN_TEXT = 200     # characters of description needed to count as "has text"
PAGE_SIZE = 100
TOP_K = 12         # sector labels shown per source and event

PAGES_PATH = Path("data/raw/stability_pages.json")
COUNTS_PATH = Path("data/raw/event_window_counts.json")
REPORT_PATH = Path("docs/sector_month_counts.md")

# event key -> (name, event date, {source: (first month, last month)})
EVENTS = {
    "crma": ("EU Critical Raw Materials Act, 23 May 2024", date(2024, 5, 23),
             {"jobbland.se": ("2024-01", "2024-08")}),
    # EU steel import regulation (replaces the safeguard). Two possible test dates,
    # both fixed here before any 2026 sector result exists: the Parliament vote
    # (anticipation) and the application date. The regulation applies from 1 Jul 2026,
    # so July is wholly after it; the event date is set to 30 Jun so that June is the
    # event month that is left out and July and August count as post-window.
    "steelvote": ("EU steel import regulation, Parliament vote, 19 May 2026", date(2026, 5, 19),
                  {"jobbland.se": ("2026-01", "2026-08")}),
    "steelapply": ("EU steel import regulation, applies 1 Jul 2026 (June left out as event month)",
                   date(2026, 6, 30),
                   {"jobbland.se": ("2026-01", "2026-08")}),
    "accelerate": ("AccelerateEU, 22 Apr 2026", date(2026, 4, 22),
                   {"kariera.gr": ("2026-01", "2026-04"),
                    "jobbland.se": ("2026-01", "2026-07")}),
}

# Target groups fixed on 17 Oct 2026 from the pooled label inventory (for the Action Plan, removed
# 27 Oct 2026; no event uses them now, since 2026 has no sector tags, and they are kept so that the
# pre-specification stays on record)
# (sector_labels_steel.md), before any monthly count of the groups was looked at.
# The narrow metals group is expected to fail the rule and is reported
# descriptively only; the exposed group is the primary Steel test.
METAL_WORDS = ("basic metals", "basic iron and steel", "fabricated metal",
               "machining of metals", "casting of metals", "metal structures",
               "metal forming machinery", "hollow profiles and related fittings, of steel")
GROUPS = {
    "steel": {
        "Exposed manufacturing (primary): all 'Manufacture ...', MANUFACTURING, "
        "machining/casting of metals, repair and maintenance of machinery":
            lambda lab: (lab.lower().startswith("manufactur")
                         or lab.lower() in ("machining of metals", "casting of metals",
                                            "repair and maintenance of machinery")),
        "Narrow metals (secondary, descriptive only)":
            lambda lab: any(w in lab.lower() for w in METAL_WORDS),
    },
}

LABEL_KEYS = ("label", "name", "preferred_label", "preferredLabel", "title",
              "value", "id", "uri")


# ---------- helpers (same conventions as script 33) ----------
def ym_range(a, b):
    y, m = (int(x) for x in a.split("-"))
    y2, m2 = (int(x) for x in b.split("-"))
    out = []
    while (y, m) <= (y2, m2):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def month_bounds(ym):
    y, m = (int(x) for x in ym.split("-"))
    return date(y, m, 1).isoformat(), date(y, m, calendar.monthrange(y, m)[1]).isoformat()


def grid_pages(n_pages, k):
    k = min(k, n_pages)
    return sorted({max(1, min(n_pages, round((j + 0.5) * n_pages / k))) for j in range(k)})


def label_of(v):
    if isinstance(v, str):
        return v.strip() or None
    if isinstance(v, dict):
        for k in LABEL_KEYS:
            if v.get(k):
                return str(v[k]).strip()
        return json.dumps(v, sort_keys=True, ensure_ascii=False)[:80]
    return None if v is None else str(v)


def first_label(val):
    items = val if isinstance(val, list) else ([val] if val else [])
    for it in items:
        lab = label_of(it)
        if lab:
            return lab
    return None


def compact(p):
    skills = p.get("skills") or []
    return {
        "id": p.get("id"),
        "d": str(p.get("upload_date") or "")[:10],
        "occ": first_label(p.get("occupations")),
        "sec": first_label(p.get("sectors")),
        "exp": label_of(p.get("experience_level")),
        "typ": label_of(p.get("type")),
        "loc": label_of(p.get("location_code")),
        "nsk": len(skills) if isinstance(skills, list) else 0,
        "dl": len(p.get("description") or ""),
        "t": str(p.get("title") or "")[:90],
    }


def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


# ---------- fetching ----------
def fetch_page(client, source, ym, page, attempts=3):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    lo, hi = month_bounds(ym)
    last = None
    for i in range(1, attempts + 1):
        try:
            r = client.session.post(
                f"{BASE_URL}{JOBS_ENDPOINT}",
                params={"page": page, "page_size": PAGE_SIZE},
                data={"sources": [source], "min_upload_date": lo,
                      "max_upload_date": hi}, timeout=240)
            r.raise_for_status()
            j = r.json()
            return j.get("items", []), j.get("count")
        except Exception as exc:
            last = exc
            print(f"    attempt {i}/{attempts} failed: {exc}")
            time.sleep(5 * i)
    raise last


# Monthly totals already published in the report (Sections 9.3 and 9.9): jobbland.se,
# January to May 2024 and August 2026. Used only when the live probe fails.
KNOWN_COUNTS = {"jobbland.se": {"2024-01": 191, "2024-02": 246, "2024-03": 292,
                                "2024-04": 410, "2024-05": 2116, "2026-08": 40875}}


def probe_count(client, source, ym, attempts=3):
    """Closed-window count with page_size=1. Uses a long timeout (the server
    often needs more than the client's default 45 s) and returns None when all
    attempts fail, so one slow month does not stop the whole run."""
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    lo, hi = month_bounds(ym)
    for i in range(1, attempts + 1):
        try:
            r = client.session.post(
                f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": 1, "page_size": 1},
                data={"sources": [source], "min_upload_date": lo,
                      "max_upload_date": hi}, timeout=240)
            r.raise_for_status()
            return r.json().get("count")
        except Exception as exc:
            print(f"    count {source} {ym}: attempt {i}/{attempts} failed: {exc}")
            time.sleep(5 * i)
    return None


def month_total(client, source, ym, counts):
    c = counts.get(source, {}).get(ym)
    if c is not None:
        return c
    if client is None:
        return KNOWN_COUNTS.get(source, {}).get(ym)
    c = probe_count(client, source, ym)
    if c is None:
        c = KNOWN_COUNTS.get(source, {}).get(ym)
        if c is not None:
            print(f"    using the count published in the report for {source} {ym}: {c}")
    if c is not None:
        counts.setdefault(source, {})[ym] = c
        save(COUNTS_PATH, counts)
    return c


def collect(event_keys, pages_per_month):
    from skillab_client import SkillabClient
    client = SkillabClient()
    counts = load(COUNTS_PATH)
    store = load(PAGES_PATH)
    for ek in event_keys:
        _name, _d, srcs = EVENTS[ek]
        for source, (a, b) in srcs.items():
            for ym in ym_range(a, b):
                n = month_total(client, source, ym, counts)
                if n is None:
                    print(f"  {source} {ym}: count unavailable (server slow); re-run to retry")
                    continue
                if not n:
                    print(f"  {source} {ym}: no postings")
                    continue
                n_pages = math.ceil(n / PAGE_SIZE)
                for pg in grid_pages(n_pages, pages_per_month):
                    key = f"{source}|{ym}|{pg}"
                    if key in store:
                        continue
                    try:
                        items, _ = fetch_page(client, source, ym, pg)
                    except Exception as exc:
                        print(f"  {source} {ym} page {pg}/{n_pages}: FAILED ({exc})")
                        continue
                    store[key] = [compact(p) for p in items]
                    save(PAGES_PATH, store)
                    print(f"  {source} {ym} page {pg}/{n_pages}: {len(items)} postings")


# ---------- analysis ----------
def sample_for(store, source, ym):
    out = []
    for key, items in store.items():
        s, m, _pg = key.split("|")
        if s == source and m == ym:
            out.extend(items)
    return out


def cell(est, lo, hi):
    """Estimated count with a marker: ~ when the interval straddles MIN_N,
    ! when the estimate is below MIN_N."""
    mark = ""
    if est < MIN_N:
        mark = "!"
    elif lo < MIN_N:
        mark = "~"
    return f"{est:,.0f}{mark}"


def analyse(event_keys):
    counts = load(COUNTS_PATH)
    store = load(PAGES_PATH)
    L = ["# Sector-month counts around the primary events (Month 3, step 1)\n",
         f"Rule: a sector is usable for an event in a source only if its estimated "
         f"number of postings is at least **{MIN_N}** in every pre-window month and "
         f"every post-window month (event month left out). A description counts as "
         f"text from {MIN_TEXT} characters. Estimates come from page samples "
         "(see the script's header for limits); `!` = below the minimum, `~` = the "
         "95% interval straddles the minimum. Only the first sector tag of a "
         "posting is used, duplicates are not removed, so the counts are "
         "optimistic upper bounds. These are estimates for the whole source. The "
         "rule is applied to the postings that are actually downloaded and "
         "analysed, so the download size per month has to be chosen so that every "
         "sector reaches the minimum (for a sector with a share s of a month's "
         f"postings, about {MIN_N}/s postings must be downloaded).\n"]

    for ek in event_keys:
        name, edate, srcs = EVENTS[ek]
        ev_ym = f"{edate.year:04d}-{edate.month:02d}"
        L.append(f"## {name}\n")
        for source, (a, b) in srcs.items():
            months = ym_range(a, b)
            pre = [m for m in months if m < ev_ym]
            post = [m for m in months if m > ev_ym]
            L.append(f"### {source}  (pre: {', '.join(pre) or 'none'}; "
                     f"event month: {ev_ym}; post: {', '.join(post) or 'none'})\n")
            if not pre or not post:
                L.append("**This source has no "
                         + ("pre-window" if not pre else "post-window")
                         + " in whole months: not usable for this event as defined. "
                         "Option: split the event month at the event date and use "
                         "the days after it as the post-window (only if the source "
                         "is still collecting then).**\n")

            # per-month overview
            rows = ["| Month | Postings | Sampled | With sector tag | With text | Est. tagged | Est. with text |",
                    "|---|---:|---:|---:|---:|---:|---:|"]
            per = {}
            missing_data = []
            for ym in months:
                tot = counts.get(source, {}).get(ym)
                if tot is None:
                    tot = KNOWN_COUNTS.get(source, {}).get(ym)
                smp = sample_for(store, source, ym)
                if tot is None or not smp:
                    missing_data.append(ym)
                    rows.append(f"| {ym} | {tot if tot is not None else '-'} | {len(smp)} | | | | |")
                    continue
                n = len(smp)
                tag = sum(1 for r in smp if r["sec"])
                txt = sum(1 for r in smp if r["dl"] >= MIN_TEXT)
                per[ym] = (tot, smp)
                rows.append(f"| {ym} | {tot:,} | {n} | {tag / n:.0%} | {txt / n:.0%} | "
                            f"{tot * tag / n:,.0f} | {tot * txt / n:,.0f} |")
            L += rows
            L.append("")
            if missing_data:
                L.append(f"No sample or count yet for: {', '.join(missing_data)} "
                         "(run without --offline, or those months are empty).\n")

            # sector labels
            pool = Counter()
            for ym, (tot, smp) in per.items():
                for r in smp:
                    if r["sec"]:
                        pool[r["sec"]] += tot / len(smp)
            if not per:
                L.append("**No data yet for this window** (run the script without --offline).\n")
                continue
            if not pool:
                L.append("**No sector tags in any sampled month of this window.** Sector "
                         "must come from the text classifier; the usable ceiling is the "
                         "'Est. with text' column above.\n")
                continue
            labels = [lab for lab, _ in pool.most_common(TOP_K)]
            checked = [m for m in pre + post if m in per]
            hdr = ["Sector (first tag)"] + [m + ("*" if m == ev_ym else "") for m in months] + ["Rule met?"]
            rows = ["| " + " | ".join(hdr) + " |", "|" + "|".join("---" for _ in hdr) + "|"]
            for lab in labels:
                cells, ok_all, ok_pool = [], True, None
                pre_sum = post_sum = 0.0
                for ym in months:
                    if ym not in per:
                        cells.append("")
                        if ym in pre or ym in post:
                            ok_all = False
                        continue
                    tot, smp = per[ym]
                    k = sum(1 for r in smp if r["sec"] == lab)
                    lo, hi = wilson(k, len(smp))
                    est = tot * k / len(smp)
                    cells.append(cell(est, tot * lo, tot * hi))
                    if ym in pre:
                        pre_sum += est
                    if ym in post:
                        post_sum += est
                    if (ym in pre or ym in post) and est < MIN_N:
                        ok_all = False
                if not (pre and post and all(m in per for m in pre + post)):
                    verdict = "cannot say (months missing)"
                else:
                    verdict = "**yes**" if ok_all else "no"
                    verdict += f" (pooled pre {pre_sum:,.0f}, post {post_sum:,.0f})"
                rows.append("| " + " | ".join([lab[:55]] + cells + [verdict]) + " |")
            L += rows
            L.append("")
            n_yes = sum(1 for r in rows[2:] if "**yes**" in r)
            L.append(f"Sectors meeting the rule: **{n_yes}** of the {len(labels)} most frequent "
                     f"labels (`*` marks the event month).\n")

            if ek in GROUPS:
                L.append("**Pre-specified groups** (all labels of the group added up, "
                         "same rule):\n")
                hdr = ["Group"] + [m + ("*" if m == ev_ym else "") for m in months] + ["Rule met?"]
                grows = ["| " + " | ".join(hdr) + " |", "|" + "|".join("---" for _ in hdr) + "|"]
                for gname, pred in GROUPS[ek].items():
                    cells, ok_all, pre_sum, post_sum = [], True, 0.0, 0.0
                    for ym in months:
                        if ym not in per:
                            cells.append("")
                            if ym in pre or ym in post:
                                ok_all = False
                            continue
                        tot, smp = per[ym]
                        k = sum(1 for r in smp if r["sec"] and pred(r["sec"]))
                        lo, hi = wilson(k, len(smp))
                        est = tot * k / len(smp)
                        cells.append(cell(est, tot * lo, tot * hi))
                        if ym in pre:
                            pre_sum += est
                        if ym in post:
                            post_sum += est
                        if (ym in pre or ym in post) and est < MIN_N:
                            ok_all = False
                    if not (pre and post and all(m in per for m in pre + post)):
                        verdict = "cannot say (months missing)"
                    else:
                        verdict = ("**yes**" if ok_all else "no") + \
                                  f" (pooled pre {pre_sum:,.0f}, post {post_sum:,.0f})"
                    grows.append("| " + " | ".join([gname[:48] + ("..." if len(gname) > 48 else "")] + cells + [verdict]) + " |")
                L += grows
                L.append("")
    return L


def list_labels(event_keys, match):
    """Inventory of first-tag sector labels in the cached samples, pooled over
    all months of each source in the event windows. No monthly breakdown on
    purpose: target sectors are chosen from this list, before any monthly
    count is looked at. Labels with a rare share may be missing from a sample
    of a few hundred postings per month; --match shows only labels containing
    one of the given words (case-insensitive)."""
    store = load(PAGES_PATH)
    words = [w.lower() for w in (match or [])]
    for ek in event_keys:
        name, _d, srcs = EVENTS[ek]
        L = [f"# Sector label inventory: {name}\n",
             "Pooled over every sampled month of the event windows, first sector "
             "tag only. Counts are postings in the cached sample, not estimates "
             "for the whole source. Choose the target sectors from the event "
             "text, write them down, and only then look at monthly counts.\n"]
        for source, (a, b) in srcs.items():
            labs, tagged, n = {}, 0, 0
            for ym in ym_range(a, b):
                for p in sample_for(store, source, ym):
                    n += 1
                    if p.get("sec"):
                        tagged += 1
                        labs[p["sec"]] = labs.get(p["sec"], 0) + 1
            L.append(f"## {source}  ({n} sampled postings, {tagged} with a sector tag)\n")
            if not tagged:
                L.append("No sector tags in the sample.\n")
                continue
            L += ["| Sector label | Sampled postings | Share of tagged |", "|---|---:|---:|"]
            for lab, c in sorted(labs.items(), key=lambda x: -x[1]):
                if words and not any(w in lab.lower() for w in words):
                    continue
                L.append(f"| {lab} | {c} | {c / tagged:.1%} |")
            L.append("")
        path = REPORT_PATH.with_name(f"sector_labels_{ek}.md")
        path.write_text("\n".join(L) + "\n", encoding="utf-8")
        print(f"Wrote {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--events", nargs="+", choices=list(EVENTS), default=list(EVENTS))
    ap.add_argument("--pages", type=int, default=3,
                    help="pages of 100 postings fetched per source and month (default 3)")
    ap.add_argument("--offline", action="store_true",
                    help="do not call the API; build the report from the saved files")
    ap.add_argument("--list-labels", action="store_true",
                    help="write the inventory of sector labels from the saved "
                         "samples (offline) and stop")
    ap.add_argument("--match", nargs="+", default=None,
                    help="with --list-labels: only labels containing these words")
    args = ap.parse_args()

    if args.list_labels:
        list_labels(args.events, args.match)
        return

    print(f"Rule in force: MIN_N = {MIN_N} postings per sector-month; MIN_TEXT = {MIN_TEXT}")
    if not args.offline:
        collect(args.events, args.pages)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # One file per event, so running the events one after the other does not
    # overwrite earlier results; a combined file is written as well.
    for ek in args.events:
        path = REPORT_PATH.with_name(f"sector_month_counts_{ek}.md")
        path.write_text("\n".join(analyse([ek])) + "\n", encoding="utf-8")
        print(f"Wrote {path}")
    if len(args.events) > 1:
        REPORT_PATH.write_text("\n".join(analyse(args.events)) + "\n", encoding="utf-8")
        print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
