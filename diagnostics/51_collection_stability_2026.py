"""
Has the composition of the collected postings changed from month to month?

Section 9.8 warns that a constant monthly count can hide a changing mix of
postings (a different scraped category or country mix), and that the stability
check "has not been run". This script runs a first version of it on the pages
that script 50 saved, for one source and a run of months, before any 2026 event
is analysed. A change in the collection would show up as a jump in the mix of
locations, posting types or description lengths, or in the share of repeated
titles, that is larger than the month-to-month change that sampling alone
produces.

How the noise floor is built: each month's sample is split at random into two
halves, many times, and the same distance is computed between the halves. Two
halves of one month differ only by chance, so the 95th percentile of that
distance is what "no change" looks like at this sample size. A real transition
between two months is flagged only when its distance is above that floor.
Halves are half the size of a month, so the floor is on the high side and
the flags are conservative.

Distances: Jensen-Shannon divergence (base 2, 0 to 1) for the mix of title
words, of `location_code` and of posting `type`; Kolmogorov-Smirnov distance (0 to 1)
for description length. The first two use every category seen.

Offline: reads data/raw/stability_pages.json (written by script 50), no
network, no credentials.

Run (project root, venv active):
    python -m diagnostics.51_collection_stability_2026
    python -m diagnostics.51_collection_stability_2026 --source jobbland.se --first 2026-01 --last 2026-08

Output: docs/collection_stability_<source>.md
"""

import argparse
import json
import math
import random
from collections import Counter
from pathlib import Path

PAGES_PATH = Path("data/raw/stability_pages.json")
SPLITS = 300
SEED = 20261017


def months_between(a, b):
    y, m = int(a[:4]), int(a[5:])
    out = []
    while f"{y:04d}-{m:02d}" <= b:
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def load_sample(source, ym):
    store = json.loads(PAGES_PATH.read_text(encoding="utf-8"))
    rows = []
    for key, items in store.items():
        s, m, _pg = key.split("|")
        if s == source and m == ym:
            rows.extend(items)
    return rows


def js_div(a, b):
    """Jensen-Shannon divergence in bits between two Counters."""
    ta, tb = sum(a.values()), sum(b.values())
    if not ta or not tb:
        return float("nan")
    d = 0.0
    for k in set(a) | set(b):
        p, q = a.get(k, 0) / ta, b.get(k, 0) / tb
        m = (p + q) / 2
        if p:
            d += 0.5 * p * math.log2(p / m)
        if q:
            d += 0.5 * q * math.log2(q / m)
    return d


def ks(x, y):
    if not x or not y:
        return float("nan")
    x, y = sorted(x), sorted(y)
    i = j = 0
    d = 0.0
    nx, ny = len(x), len(y)
    while i < nx and j < ny:
        v = min(x[i], y[j])
        while i < nx and x[i] <= v:
            i += 1
        while j < ny and y[j] <= v:
            j += 1
        d = max(d, abs(i / nx - j / ny))
    return d


def title_words(rows):
    c = Counter()
    for r in rows:
        for w in "".join(ch if ch.isalpha() else " " for ch in (r.get("t") or "").lower()).split():
            if len(w) >= 3:
                c[w] += 1
    return c


def metrics_pair(a, b):
    return {
        "words": js_div(title_words(a), title_words(b)),
        "loc": js_div(Counter(r.get("loc") or "(none)" for r in a),
                      Counter(r.get("loc") or "(none)" for r in b)),
        "type": js_div(Counter(r.get("typ") or "(none)" for r in a),
                       Counter(r.get("typ") or "(none)" for r in b)),
        "len": ks([r.get("dl", 0) for r in a], [r.get("dl", 0) for r in b]),
    }


def pct(v, q):
    v = sorted(x for x in v if x == x)
    if not v:
        return float("nan")
    k = (len(v) - 1) * q
    lo, hi = int(math.floor(k)), int(math.ceil(k))
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def noise_floor(rows, rng):
    res = {"words": [], "loc": [], "type": [], "len": []}
    if len(rows) < 40:
        return {k: float("nan") for k in res}
    for _ in range(SPLITS):
        r = rows[:]
        rng.shuffle(r)
        h = len(r) // 2
        m = metrics_pair(r[:h], r[h:2 * h])
        for k in res:
            res[k].append(m[k])
    return {k: pct(v, 0.95) for k, v in res.items()}


def median(v):
    v = sorted(v)
    n = len(v)
    return float("nan") if not n else (v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--source", default="jobbland.se")
    ap.add_argument("--first", default="2026-01")
    ap.add_argument("--last", default="2026-08")
    args = ap.parse_args()

    months = months_between(args.first, args.last)
    data = {m: load_sample(args.source, m) for m in months}
    have = [m for m in months if data[m]]
    rng = random.Random(SEED)

    out = [f"# Collection stability: {args.source}, {args.first} to {args.last}\n",
           "Compares the mix of the saved page samples month by month (see the script's "
           "header). A flagged transition means the mix changed by more than sampling "
           "alone produces; it does not say why. Samples are about 300 postings a month, "
           "taken from pages spread over the month's results.\n"]

    out += ["## Each month", "",
            "| Month | Sampled | With text (200+) | Median description length | Repeated titles | Distinct upload days | Distinct location codes | Distinct types |",
            "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for m in months:
        r = data[m]
        if not r:
            out.append(f"| {m} | 0 | | | | | | |")
            continue
        n = len(r)
        titles = [(x.get("t") or "").strip().lower() for x in r]
        rep = 1 - len(set(titles)) / n
        days = [x.get("d", "")[8:10] for x in r if x.get("d")]
        out.append(f"| {m} | {n} | {sum(1 for x in r if x.get('dl', 0) >= 200) / n:.0%} | "
                   f"{median([x.get('dl', 0) for x in r]):,.0f} | {rep:.1%} | "
                   f"{len(set(days))} | {len(set(x.get('loc') for x in r))} | "
                   f"{len(set(x.get('typ') for x in r))} |")
    out.append("")

    thin = [m for m in have if len({x.get("d") for x in data[m] if x.get("d")}) < 10]
    if thin:
        out += [f"**Coverage warning.** In {', '.join(thin)} the sample covers fewer than 10 "
                "distinct upload days. Postings from the same day are alike (the same "
                "employers and batches), so such a sample describes those days, not the "
                "month, and its distances are noisier than the floor below assumes. "
                "Fetch more pages (script 50, `--pages 12`) before relying on a flag or on "
                "its absence.", ""]
    constant = [k for k, f in (("location code", "loc"), ("type", "typ"))
                if have and all(len({x.get(f) for x in data[m]}) <= 1 for m in have)]
    if constant:
        out += [f"**Uninformative fields.** The {' and '.join(constant)} take a single value in "
                "every sampled month, so their distances are always 0 and say nothing "
                "about stability.", ""]

    floors = {m: noise_floor(data[m], rng) for m in have}
    out += ["## Transitions between consecutive months", "",
            "Distance between month A and the next month B, and the 95th percentile of the "
            "same distance between two random halves of the larger-sample month. "
            "`FLAG` = above the noise floor.", "",
            "| From | To | Title words | Floor | Location mix | Floor | Type mix | Floor | Description length | Floor |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    flagged = []
    for a, b in zip(months, months[1:]):
        if not data[a] or not data[b]:
            out.append(f"| {a} | {b} | no sample | | | | | | | |")
            continue
        m = metrics_pair(data[a], data[b])
        fl = floors[a] if len(data[a]) >= len(data[b]) else floors[b]
        cells = []
        for k in ("words", "loc", "type", "len"):
            flag = m[k] == m[k] and fl[k] == fl[k] and m[k] > fl[k]
            if flag:
                flagged.append((a, b, k))
            cells += [f"{m[k]:.3f}" + (" **FLAG**" if flag else ""), f"{fl[k]:.3f}"]
        out.append(f"| {a} | {b} | " + " | ".join(cells) + " |")
    out.append("")

    if flagged:
        out.append("**Flagged transitions:** " + "; ".join(
            f"{a} to {b} ({k})" for a, b, k in flagged) + ".")
    else:
        out.append("**No transition is above the sampling noise floor** for the location mix, "
                   "the type mix or the description length.")
    out.append("")
    out.append("Reading: a flag in the month of an event does not show a policy effect; "
               "it shows that the collected mix changed at that point, so a comparison "
               "across that boundary compares different kinds of postings. The mix is "
               "checked on four fields only; a change in, for example, the scraped "
               "category that these fields do not reflect would not show here.")

    path = Path(f"docs/collection_stability_{args.source}.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
