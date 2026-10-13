"""
Composition stability check around the two testable events.

Question: when monthly volume is steady on both sides of an event, is the
COMPOSITION of the postings (occupation, sector, experience level, type, how
often the tags are filled) also steady? If a scraper started covering another
part of a board at the event date, shares computed within the source would move
for collection reasons and could be mistaken for an event effect.

Cases (source, months used, first month counted as "after"):
    ev-gr   kariera.gr     2024-09 .. 2024-12   after = 2024-11   (EU tariffs on Chinese EVs, 30 Oct 2024)
    ev-fr   lesjeudis.com  2024-08 .. 2025-01   after = 2024-11
    oil-gr  kariera.gr     2026-01 .. 2026-04   after = 2026-03   (Iran war / oil shock, 28 Feb 2026)
    oil-se  jobbland.se    2026-01 .. 2026-05   after = 2026-03

For every month the script samples evenly spaced result pages of the closed
calendar window (page_size 100, default 6 pages = up to 600 postings), so the
sample spreads over the whole month, not only its first days. It then compares:
  * the pre pool against the post pool, and
  * adjacent months inside the same side (the "normal drift" yardstick),
with the Jensen-Shannon divergence (base 2, 0 = identical, 1 = disjoint) for each
categorical variable, plus a permutation null (shuffle the pre/post labels).
Rule of thumb printed in the report: the event comparison is "within normal
drift" when its divergence does not exceed the largest adjacent-month divergence
on the same side and the permutation 95th percentile. This is a screening rule,
not a significance test; with large samples tiny shifts are "significant", so
the drift yardstick is the more useful number.

Usage, from the repo root (credentials in .env or env vars):
    python -m diagnostics.33_composition_stability_check --case oil-gr
    python -m diagnostics.33_composition_stability_check --case all --pages 6
    python -m diagnostics.33_composition_stability_check --analyse-only

Needs monthly counts from script 32 (data/raw/event_window_counts.json) to choose
the pages; missing counts are probed. Resumable: pages are kept in
data/raw/stability_pages.json (compact fields only; local, not for the repo).
Each request takes 20-70 s; one case is roughly 20-30 minutes. Re-run after
failures: only missing pages are fetched. Output: docs/stability_check.md
"""

import argparse
import calendar
import json
import math
import random
import time
from collections import Counter
from datetime import date
from pathlib import Path

PAGES_PATH = Path("data/raw/stability_pages.json")
COUNTS_PATH = Path("data/raw/event_window_counts.json")
REPORT_PATH = Path("docs/stability_check.md")
PAGE_SIZE = 100
TOP_K = 40          # categories kept per variable; the rest become "(other)"
MIN_N = 300         # months with fewer sampled postings are flagged

CASES = {
    "ev-gr": ("kariera.gr", ["2024-09", "2024-10", "2024-11", "2024-12"], "2024-11",
              "EU tariffs on Chinese EVs, 30 Oct 2024"),
    "ev-fr": ("lesjeudis.com", ["2024-08", "2024-09", "2024-10", "2024-11", "2024-12", "2025-01"], "2024-11",
              "EU tariffs on Chinese EVs, 30 Oct 2024"),
    "oil-gr": ("kariera.gr", ["2026-01", "2026-02", "2026-03", "2026-04"], "2026-03",
               "Iran war / oil shock, 28 Feb 2026"),
    "oil-se": ("jobbland.se", ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05"], "2026-03",
               "Iran war / oil shock, 28 Feb 2026"),
}

LABEL_KEYS = ("label", "name", "preferred_label", "preferredLabel", "title", "value", "id", "uri")


# ---------- helpers ----------
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


# ---------- fetching ----------
def fetch_page(client, source, ym, page, attempts=3):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    lo, hi = month_bounds(ym)
    last = None
    for i in range(1, attempts + 1):
        try:
            r = client.session.post(
                f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": page, "page_size": PAGE_SIZE},
                data={"sources": [source], "min_upload_date": lo, "max_upload_date": hi}, timeout=240)
            r.raise_for_status()
            j = r.json()
            return j.get("items", []), j.get("count")
        except Exception as exc:
            last = exc
            print(f"    attempt {i}/{attempts} failed: {exc}")
            time.sleep(5 * i)
    raise last


def month_count(client, source, ym, counts):
    c = counts.get(source, {}).get(ym)
    if c is not None:
        return c
    lo, hi = month_bounds(ym)
    return client.count_postings(source, lo, hi)


def collect(case, pages_per_month):
    from skillab_client import SkillabClient
    source, months, _after, _ev = CASES[case]
    client = SkillabClient()
    counts = load(COUNTS_PATH)
    store = load(PAGES_PATH)
    for ym in months:
        n = month_count(client, source, ym, counts)
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
    return store


# ---------- analysis ----------
def sample_for(store, source, ym):
    out = []
    for key, items in store.items():
        s, m, _pg = key.split("|")
        if s == source and m == ym:
            out.extend(items)
    return out


def flag(x):
    return "yes" if x else "no"


VARS = {
    "occupation (first tag)": lambda r: r["occ"] or "(none)",
    "sector (first tag)": lambda r: r["sec"] or "(none)",
    "experience_level": lambda r: r["exp"] or "(none)",
    "type": lambda r: r["typ"] or "(none)",
    "location_code": lambda r: r["loc"] or "(none)",
    "has occupation tag": lambda r: flag(r["occ"]),
    "has sector tag": lambda r: flag(r["sec"]),
    "has skills": lambda r: flag(r["nsk"] > 0),
    "description length (bin)": lambda r: ("0" if r["dl"] == 0 else "<500" if r["dl"] < 500 else
                                           "<1500" if r["dl"] < 1500 else "<4000" if r["dl"] < 4000 else "4000+"),
}


def jsd(a, b, cats):
    na, nb = sum(a.values()), sum(b.values())
    if not na or not nb:
        return float("nan")
    tot = 0.0
    for c in cats:
        p, q = a.get(c, 0) / na, b.get(c, 0) / nb
        m = (p + q) / 2
        if p:
            tot += 0.5 * p * math.log2(p / m)
        if q:
            tot += 0.5 * q * math.log2(q / m)
    return tot


def collapse(values_by_group, top_k):
    pooled = Counter()
    for vals in values_by_group:
        pooled.update(vals)
    keep = {c for c, _ in pooled.most_common(top_k)}
    return keep


def jsd_values(vals_a, vals_b, keep):
    ca = Counter(v if v in keep else "(other)" for v in vals_a)
    cb = Counter(v if v in keep else "(other)" for v in vals_b)
    return jsd(ca, cb, set(ca) | set(cb))


def perm_null(vals_a, vals_b, keep, perms, rng):
    pool = [v if v in keep else "(other)" for v in vals_a + vals_b]
    na = len(vals_a)
    res = []
    for _ in range(perms):
        rng.shuffle(pool)
        ca, cb = Counter(pool[:na]), Counter(pool[na:])
        res.append(jsd(ca, cb, set(ca) | set(cb)))
    res.sort()
    return sum(res) / len(res), res[int(0.95 * (len(res) - 1))]


def analyse_case(case, store, perms, rng):
    source, months, after, ev = CASES[case]
    samples = {ym: sample_for(store, source, ym) for ym in months}
    have = [ym for ym in months if samples[ym]]
    pre_m = [m for m in have if m < after]
    post_m = [m for m in have if m >= after]
    lines = [f"## {case}: {source}, {ev}", "",
             f"Months before the event: {', '.join(pre_m) or 'none'}; after: {', '.join(post_m) or 'none'} "
             f"(the month of the event date is counted on the side where most of it falls).", "",
             "| month | sampled postings | side |", "|---|---:|---|"]
    for ym in have:
        n = len(samples[ym])
        lines.append(f"| {ym} | {n}{' (small)' if n < MIN_N else ''} | {'after' if ym >= after else 'before'} |")
    lines.append("")
    if not pre_m or not post_m:
        lines += ["Not enough sampled months on both sides yet; run the collection step.", ""]
        return lines

    pre = [r for m in pre_m for r in samples[m]]
    post = [r for m in post_m for r in samples[m]]
    lines += ["Jensen-Shannon divergence (0 = identical, 1 = disjoint). `drift` = largest divergence between two "
              "adjacent months on the same side; `null 95%` = 95th percentile when pre/post labels are shuffled.", "",
              "| variable | pre vs post | drift (adjacent months) | null 95% | reading |", "|---|---:|---:|---:|---|"]
    moves = {}
    for name, fn in VARS.items():
        vpre, vpost = [fn(r) for r in pre], [fn(r) for r in post]
        keep = collapse([vpre, vpost], TOP_K)
        d_event = jsd_values(vpre, vpost, keep)
        drifts = []
        for side in (pre_m, post_m):
            for a, b in zip(side, side[1:]):
                drifts.append(jsd_values([fn(r) for r in samples[a]], [fn(r) for r in samples[b]], keep))
        drift = max(drifts) if drifts else float("nan")
        _mean, null95 = perm_null(vpre, vpost, keep, perms, rng)
        ref = max([x for x in (drift, null95) if x == x] or [0])
        reading = "within normal drift" if d_event <= ref else "shift beyond drift"
        lines.append(f"| {name} | {d_event:.3f} | {'n/a' if drift != drift else f'{drift:.3f}'} | {null95:.3f} | {reading} |")
        moves[name] = (vpre, vpost)
    lines.append("")

    for name in ("occupation (first tag)", "sector (first tag)"):
        vpre, vpost = moves[name]
        cp, cq = Counter(vpre), Counter(vpost)
        npre, npost = len(vpre), len(vpost)
        cats = sorted(set(cp) | set(cq), key=lambda c: -abs(cq.get(c, 0) / npost - cp.get(c, 0) / npre))[:8]
        lines += [f"Largest share changes, {name} (pre n={npre}, post n={npost}):", "",
                  "| label | pre share | post share | change (pp) |", "|---|---:|---:|---:|"]
        for c in cats:
            a, b = 100 * cp.get(c, 0) / npre, 100 * cq.get(c, 0) / npost
            lines.append(f"| {c[:70]} | {a:.1f}% | {b:.1f}% | {b - a:+.1f} |")
        lines.append("")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=list(CASES) + ["all"], default="all")
    ap.add_argument("--pages", type=int, default=6, help="evenly spaced pages per month (default 6)")
    ap.add_argument("--perms", type=int, default=300)
    ap.add_argument("--analyse-only", action="store_true")
    args = ap.parse_args()

    chosen = list(CASES) if args.case == "all" else [args.case]
    if not args.analyse_only:
        for case in chosen:
            print(f"=== {case} ===")
            collect(case, args.pages)

    store = load(PAGES_PATH)
    rng = random.Random(20261013)
    out = ["# Composition stability check around candidate events", "",
           "Sampled postings (evenly spaced pages of each calendar month) compared before and after each event, "
           "within one source. A reading of \"within normal drift\" means the pre/post divergence is no larger than the "
           "month-to-month divergence on the same side and no larger than a random relabelling; it supports comparing "
           "shares across the event. \"Shift beyond drift\" means the mix of postings changed more than usual and the "
           "cause (collection or labour market) has to be examined before shares are interpreted.", ""]
    for case in chosen:
        out += analyse_case(case, store, args.perms, rng)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))
    print(f"\nWritten: {REPORT_PATH}")


if __name__ == "__main__":
    main()
