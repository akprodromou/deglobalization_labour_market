"""
Time-stratified OJA sample: did the composition of OJA change at January 2024?

Why: OJA postings jump from 5,391 (Dec 2023) to 276,271 (Jan 2024). The working
sample cannot test why, because every OJA posting in it is from 2019. This
script draws postings from several single-month windows and compares them:

  * 2019-06, 2023-06   a baseline-era month and a pre-break month
  * 2023-12, 2024-01   either side of the break
  * 2024-02, 2024-12, 2025-03   after the break (2024-12 is the low-volume tail,
                                2025-03 the last month with data)

For each window it fetches RANDOM result pages (page_size=100) rather than the
first pages, so the sample is not just whatever the API returns first. Each page
is 100 consecutive results, so the sample is clustered; with 5 pages per window
(500 postings) the comparison is indicative, not a precise estimate.

What it compares per window (docs/oja_stratified_check.md):
  - country mix (location_code)
  - ISCO major-group mix (derived from occupation entries, if they carry ISCO codes)
  - share with skills / occupations / organization / description, mean description length
  - duplicates inside the sample: same description prefix, same content key
  - concentration: share of postings from the 10 most frequent organizations
  - overlap in description prefixes BETWEEN windows (are Jan 2024 postings re-listings
    of older ones?)
  - a simple composition distance (total variation) between consecutive windows,
    for country and ISCO group

Usage, from the repo root (credentials in SKILLAB_USERNAME / SKILLAB_PASSWORD):
    python -m diagnostics.21_oja_time_stratified_sample
    python -m diagnostics.21_oja_time_stratified_sample --pages 8 --seed 7
    python -m diagnostics.21_oja_time_stratified_sample --windows 2023-12 2024-01
    python -m diagnostics.21_oja_time_stratified_sample --analyse-only

Resumable: each fetched page is appended to data/raw/oja_stratified_sample.jsonl and
recorded in data/raw/oja_stratified_pages.json; a re-run fetches only missing pages.
The page numbers are drawn from a seeded generator, so the same seed gives the same
pages. Failed pages are reported and retried on the next run.
"""

import argparse
import calendar
import hashlib
import json
import math
import random
import re
from collections import Counter
from datetime import date
from pathlib import Path

SAMPLE_PATH = Path("data/raw/oja_stratified_sample.jsonl")
PAGES_PATH = Path("data/raw/oja_stratified_pages.json")
REPORT_PATH = Path("docs/oja_stratified_check.md")
SOURCE = "OJA"
PAGE_SIZE = 100
DEFAULT_WINDOWS = ["2019-06", "2023-06", "2023-12", "2024-01", "2024-02", "2024-12", "2025-03"]
ISCO_PATTERN = re.compile(r"isco/C(\d)")
MIN_DESCRIPTION_CHARS = 80


# ---------- helpers ---------------------------------------------------------

def month_bounds(label):
    y, m = (int(x) for x in label.split("-"))
    last = min(date(y, m, calendar.monthrange(y, m)[1]), date.today())
    return date(y, m, 1).isoformat(), last.isoformat()


def norm(value):
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def description_key(p):
    text = norm(p.get("description"))
    if len(text) < MIN_DESCRIPTION_CHARS:
        return None
    return hashlib.md5(text[:300].encode("utf-8")).hexdigest()


def content_key(p):
    parts = [norm(p.get("title")), norm(p.get("organization")), norm(p.get("location")),
             norm(p.get("upload_date"))[:10]]
    return "|".join(parts) if parts[0] else None


def isco_major(p):
    """First ISCO major-group digit found anywhere in the occupation entries, else None."""
    for entry in p.get("occupations") or []:
        text = entry if isinstance(entry, str) else json.dumps(entry, ensure_ascii=False)
        match = ISCO_PATTERN.search(text)
        if match:
            return match.group(1)
    return None


def share(counter, total):
    return {k: v / total for k, v in counter.items()} if total else {}


def total_variation(a, b):
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a.get(k, 0) - b.get(k, 0)) for k in keys)


def pct(x):
    return f"{100 * x:.1f}%"


def load_json(path, default):
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------- fetching --------------------------------------------------------

def fetch_page(client, start, end, page):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [SOURCE], "min_upload_date": start, "max_upload_date": end}
    response = client._post_with_retries(
        f"{BASE_URL}{JOBS_ENDPOINT}", {"page": page, "page_size": PAGE_SIZE}, form)
    payload = response.json()
    return payload.get("items", []), payload.get("count")


def collect(windows, pages_per_window, seed):
    from skillab_client import SkillabClient
    client = SkillabClient()
    state = load_json(PAGES_PATH, {})   # window -> {"count": N, "pages": [chosen], "done": [fetched]}
    SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

    for label in windows:
        start, end = month_bounds(label)
        entry = state.setdefault(label, {})
        if "count" not in entry:
            try:
                _, count = fetch_page(client, start, end, 1)
            except Exception as exc:
                print(f"  {label}: could not get count ({exc}); skipped")
                continue
            entry["count"] = count
            save_json(PAGES_PATH, state)
        count = entry["count"]
        n_pages = math.ceil(count / PAGE_SIZE) if count else 0
        if n_pages == 0:
            print(f"  {label}: 0 postings")
            continue
        if "pages" not in entry or entry.get("seed") != seed or entry.get("n") != pages_per_window:
            rng = random.Random(f"{seed}-{label}")
            entry["pages"] = sorted(rng.sample(range(1, n_pages + 1), min(pages_per_window, n_pages)))
            entry["seed"], entry["n"] = seed, pages_per_window
            entry.setdefault("done", [])
            save_json(PAGES_PATH, state)
        print(f"  {label}: {count:,} postings, {n_pages:,} pages; sampling pages {entry['pages']}")
        for page in entry["pages"]:
            if page in entry["done"]:
                continue
            try:
                items, _ = fetch_page(client, start, end, page)
            except Exception as exc:
                print(f"    page {page}: FAILED ({exc})")
                continue
            with open(SAMPLE_PATH, "a", encoding="utf-8") as f:
                for item in items:
                    f.write(json.dumps({"_window": label, "_page": page, "posting": item},
                                       ensure_ascii=False) + "\n")
            entry["done"].append(page)
            save_json(PAGES_PATH, state)
            print(f"    page {page}: {len(items)} postings")
    return state


# ---------- analysis --------------------------------------------------------

def load_sample():
    by_window = {}
    if not SAMPLE_PATH.exists():
        return by_window
    with open(SAMPLE_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                row = json.loads(line)
                by_window.setdefault(row["_window"], []).append(row["posting"])
    return by_window


def summarise(postings):
    n = len(postings)
    country = Counter(p.get("location_code") for p in postings if p.get("location_code"))
    isco = Counter(isco_major(p) for p in postings if isco_major(p))
    desc_keys = [k for k in (description_key(p) for p in postings) if k]
    content_keys = [k for k in (content_key(p) for p in postings) if k]
    orgs = Counter(norm(p.get("organization")) for p in postings if norm(p.get("organization")))
    top10 = sum(c for _, c in orgs.most_common(10))
    lengths = [len(str(p.get("description") or "")) for p in postings]
    return {
        "n": n,
        "country": country, "n_country": sum(country.values()),
        "isco": isco, "n_isco": sum(isco.values()),
        "with_skills": sum(1 for p in postings if p.get("skills")),
        "with_occupations": sum(1 for p in postings if p.get("occupations")),
        "with_org": sum(1 for p in postings if norm(p.get("organization"))),
        "with_desc": len(desc_keys),
        "dup_desc": len(desc_keys) - len(set(desc_keys)),
        "dup_content": len(content_keys) - len(set(content_keys)),
        "n_content": len(content_keys),
        "top10_org_share": top10 / sum(orgs.values()) if orgs else None,
        "mean_desc_len": sum(lengths) / n if n else 0,
        "desc_keys": set(desc_keys),
    }


def report(windows, state, by_window):
    order = [w for w in windows if by_window.get(w)]
    S = {w: summarise(by_window[w]) for w in order}
    out = ["# OJA time-stratified sample: composition across windows", ""]
    out.append("Random result pages (100 postings each) from single-month windows of source `OJA`. "
               "Pages are clusters of consecutive results, so differences of a few percentage points "
               "are within sampling noise; large shifts are not. Script: "
               "`diagnostics/21_oja_time_stratified_sample.py`.")
    out.append("")
    out.append("## 1. Sample")
    out.append("")
    out.append("| Window | Postings in window | Pages sampled | Postings in sample |")
    out.append("|---|---|---|---|")
    for w in windows:
        e = state.get(w, {})
        out.append(f"| {w} | {e.get('count', '?'):,} | {len(e.get('done', []))}/{len(e.get('pages', []))} | "
                   f"{S[w]['n'] if w in S else 0} |" if isinstance(e.get('count'), int) else
                   f"| {w} | ? | 0/0 | 0 |")
    out.append("")

    out.append("## 2. Field completeness and duplicates")
    out.append("")
    out.append("| Window | skills | occupations | organization | description | mean desc. chars | "
               "repeated description prefix | repeated title/org/place/date | top-10 org share |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for w in order:
        s = S[w]
        n = s["n"]
        t10 = pct(s["top10_org_share"]) if s["top10_org_share"] is not None else "n/a"
        out.append(f"| {w} | {pct(s['with_skills']/n)} | {pct(s['with_occupations']/n)} | "
                   f"{pct(s['with_org']/n)} | {pct(s['with_desc']/n)} | {s['mean_desc_len']:.0f} | "
                   f"{s['dup_desc']}/{s['with_desc']} | {s['dup_content']}/{s['n_content']} | {t10} |")
    out.append("")

    out.append("## 3. Country mix (`location_code`)")
    out.append("")
    all_c = Counter()
    for w in order:
        all_c.update(S[w]["country"])
    top = [c for c, _ in all_c.most_common(10)]
    out.append("| Window | with code | " + " | ".join(top) + " | other |")
    out.append("|---|---|" + "---|" * (len(top) + 1))
    for w in order:
        s = S[w]
        tot = s["n_country"]
        cells = [pct(s["country"].get(c, 0) / tot) if tot else "-" for c in top]
        other = pct(sum(v for k, v in s["country"].items() if k not in top) / tot) if tot else "-"
        out.append(f"| {w} | {pct(tot / s['n'])} | " + " | ".join(cells) + f" | {other} |")
    out.append("")

    out.append("## 4. ISCO major-group mix")
    out.append("")
    if not any(S[w]["n_isco"] for w in order):
        out.append("No ISCO code could be read from the `occupations` entries in this sample. "
                   "Look at one sample posting's `occupations` field to see its format "
                   "(`data/raw/oja_stratified_sample.jsonl`) and adjust `isco_major`.")
    else:
        groups = sorted({g for w in order for g in S[w]["isco"]})
        out.append("| Window | with ISCO | " + " | ".join(f"ISCO {g}" for g in groups) + " |")
        out.append("|---|---|" + "---|" * len(groups))
        for w in order:
            s = S[w]
            tot = s["n_isco"]
            cells = [pct(s["isco"].get(g, 0) / tot) if tot else "-" for g in groups]
            out.append(f"| {w} | {pct(tot / s['n'])} | " + " | ".join(cells) + " |")
    out.append("")

    out.append("## 5. Distance between consecutive windows")
    out.append("")
    out.append("Total variation distance (0 = identical mix, 1 = disjoint) between the window and the "
               "previous one in the table.")
    out.append("")
    out.append("| From → to | country | ISCO group |")
    out.append("|---|---|---|")
    for a, b in zip(order, order[1:]):
        dc = total_variation(share(S[a]["country"], S[a]["n_country"]), share(S[b]["country"], S[b]["n_country"]))
        di = (total_variation(share(S[a]["isco"], S[a]["n_isco"]), share(S[b]["isco"], S[b]["n_isco"]))
              if S[a]["n_isco"] and S[b]["n_isco"] else None)
        out.append(f"| {a} → {b} | {dc:.2f} | {'n/a' if di is None else f'{di:.2f}'} |")
    out.append("")
    out.append("Read the Dec 2023 → Jan 2024 row against the others. A distance much larger there than "
               "between, say, 2023-06 and 2023-12 or 2024-01 and 2024-02 points to a change of "
               "composition (new feed or source mix) at the break; similar distances point to the same "
               "mix at a different volume.")
    out.append("")

    out.append("## 6. Shared description prefixes between windows")
    out.append("")
    out.append("Share of the row window's postings whose description prefix also appears in the column "
               "window's sample. High values across months mean the same adverts are listed repeatedly.")
    out.append("")
    out.append("| Window ↓ in → | " + " | ".join(order) + " |")
    out.append("|---|" + "---|" * len(order))
    for a in order:
        keys_a = S[a]["desc_keys"]
        cells = []
        for b in order:
            cells.append("-" if a == b or not keys_a else pct(len(keys_a & S[b]["desc_keys"]) / len(keys_a)))
        out.append(f"| {a} | " + " | ".join(cells) + " |")
    out.append("")
    out.append("Sample sizes are a few hundred per window, so an overlap can only be seen if a large "
               "share of the population repeats; zero overlap does not rule out smaller-scale duplication.")
    out.append("")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--windows", nargs="+", default=DEFAULT_WINDOWS, help="months as YYYY-MM")
    parser.add_argument("--pages", type=int, default=5, help="random pages (100 postings) per window")
    parser.add_argument("--seed", type=int, default=2024)
    parser.add_argument("--analyse-only", action="store_true")
    args = parser.parse_args()

    if args.analyse_only:
        state = load_json(PAGES_PATH, {})
    else:
        state = collect(args.windows, args.pages, args.seed)
    by_window = load_sample()
    if not by_window:
        print("No sampled postings yet; nothing to analyse.")
        return
    text = report(args.windows, state, by_window)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text, encoding="utf-8")
    print(text)
    print(f"\nWritten to {REPORT_PATH}")
    missing = [w for w in args.windows if state.get(w, {}).get("pages")
               and len(state[w]["done"]) < len(state[w]["pages"])]
    if missing:
        print("Incomplete windows (re-run to retry the missing pages): " + ", ".join(missing))


if __name__ == "__main__":
    main()
