"""
Month 4: does the MIX of postings change when the day volume changes? (stage 2 check: board -> Skillab database)

Our random page per day is a valid sample of the day's postings in the Skillab database. Whether that database is a stable
picture of the board is a separate question. If the day total jumps (1,000 one day, 10,000 the next) and the mix of postings
(IT 20% -> 3%) jumps with it, the postings entered the database through a changed mechanism, and shares across the jump
are not comparable. If the mix stays within what two ordinary stretches of days differ by, the jump is volume and pooling is defensible.
This test can show a change of mechanism. It cannot show that ingestion is random.

Composition is measured four ways: cluster (script 92 labels), Month 3 channel (six channels + none), sector (the `sectors`
field of the posting, first label; "(none)" when empty) and posting type is NOT used. Each is a distribution over categories.

Distance: Jensen-Shannon divergence (base 2, 0 to 1) between two pooled distributions. Each sampled day counts once (the day's page
composition), not by day total: weighting by day total would let the largest days decide the mix and hide a change on the small ones.
Equal sizes: before every distance both groups are cut at random to the same number of postings (the smaller group's), in the
observed comparison and in every shuffle. Without this, a group of low-volume days (a few postings a day) always looks different
from a group of full pages, whatever the mix, because the distance grows when a sample is small.
Noise floor: the whole DAYS are shuffled between the two groups many times (a page clumps postings of the same employers, so
postings are never shuffled one by one), keeping the group sizes. p = share of shuffles with a distance at least as large;
"excess" = observed distance minus the mean shuffled distance (JS is biased upward in small samples, the shuffle shows by how much).

Part 1, volume split: days of the period are cut into thirds by day total; low third vs high third. Trends in the mix can
mimic this, so the same split is also made inside each calendar quarter (days ranked inside the quarter; groups pooled) as a check.
Part 2, jumps: at each sampled day the mean day total of the next --span-days sampled days is divided by that of the previous
--span-days. A ratio >= --ratio (or <= 1/--ratio) marks a jump (the strongest point of each stretch is kept; windows spanning a
long gap in the sampled days are skipped); the --span-days before and after are compared.
Part 3, placebo: the same comparison for stretches with no jump (ratio inside 1/--placebo-ratio .. --placebo-ratio, windows not overlapping).
It shows how large the distance is between two ordinary stretches and how often the shuffle test rejects there.
If jumps sit far above the placebo distribution, the mix moved with the volume.

Run (project root, venv active), jobbland example:
    python -m diagnostics.97_composition_stability --board jobbland --input A --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl --tags data/tagged/tags_v12_jobbland.final.post.jsonl

Output: docs/composition_stability_<board>_<input>.md and data/cluster/composition_stability_<board>_<input>.csv
"""

import argparse
import csv
import json
import tempfile
from collections import Counter
from datetime import date
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

CH = ["reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"]


def load_all(paths):
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tmp:
        for p in paths:
            for line in open(p, encoding="utf-8"):
                if line.strip():
                    tmp.write(line.rstrip("\n") + "\n")
        name = tmp.name
    try:
        return load_corpus(name)
    finally:
        Path(name).unlink()


def week(day):
    iso = date.fromisoformat(day).isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def quarter(day):
    y, m, _ = day.split("-")
    return f"{y}-Q{(int(m) - 1) // 3 + 1}"


def sector(item):
    v = item.get("sectors")
    if isinstance(v, list):
        v = v[0] if v else None
    if isinstance(v, dict):
        v = v.get("label") or v.get("name") or v.get("id")
    if v in (None, "", "empty"):
        return "(none)"
    return str(v)


def js(p, q):
    p, q = p / p.sum(), q / q.sum()
    m = (p + q) / 2

    def kl(x, y):
        k = x > 0
        return float((x[k] * np.log2(x[k] / y[k])).sum())
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def rare(v, n, rng):
    """Random subsample of n postings from a vector of category counts (all of it if it holds <= n)."""
    v = v.astype(np.int64)
    if v.sum() <= n:
        return v.astype(float)
    return rng.multivariate_hypergeometric(v, int(n)).astype(float)


def jse(A, B, n, rng):
    return js(rare(A, n, rng) + 1e-12, rare(B, n, rng) + 1e-12)


def compare(M, ga, gb, rng, n_perm, reps=5):
    """M = days x categories posting counts. ga, gb = day index arrays.

    Both groups are cut to the same number of postings (the smaller group's) before every distance, observed and shuffled alike:
    the Jensen-Shannon distance of two samples grows when a sample is small, so groups of unequal size would differ by size alone."""
    A, B = M[ga].sum(0), M[gb].sum(0)
    if A.sum() == 0 or B.sum() == 0:
        return None
    n = int(min(A.sum(), B.sum()))
    d = float(np.mean([jse(A, B, n, rng) for _ in range(reps)]))
    idx = np.concatenate([ga, gb])
    na = len(ga)
    nulls = np.empty(n_perm)
    for i in range(n_perm):
        sh = rng.permutation(idx)
        nulls[i] = jse(M[sh[:na]].sum(0), M[sh[na:]].sum(0), n, rng)
    return {"js": d, "null": float(nulls.mean()), "excess": d - float(nulls.mean()), "p": float((nulls >= d).mean() + 1 / n_perm), "n": n}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--labels")
    ap.add_argument("--tags", nargs="+")
    ap.add_argument("--titles", help="titles file of script 90 (has_title); default data/tagged/titles_<board>.jsonl, else the title field of the posting")
    ap.add_argument("--titled-only", action="store_true", help="leave out postings without a title (check whether a shift is only the arrival of title-less postings)")
    ap.add_argument("--from", dest="d_from", default="0000-00-00")
    ap.add_argument("--to", dest="d_to", default="9999-99-99")
    ap.add_argument("--ratio", type=float, default=3.0, help="change of the mean day total (next span days / previous span days) that marks a jump")
    ap.add_argument("--placebo-ratio", type=float, default=1.5, help="stretches whose ratio is inside 1/x..x are placebo stretches")
    ap.add_argument("--span-days", type=int, default=14, help="sampled days compared on each side of a jump")
    ap.add_argument("--min-taken", type=int, default=100, help="postings a group of days needs to be compared")
    ap.add_argument("--perm", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=1)
    a, _ignored = ap.parse_known_args()  # accepts the extra arguments of script 93, so its command can be reused
    rng = np.random.default_rng(a.seed)
    labels_p = a.labels or f"data/cluster/labels_{a.board}_{a.input}.jsonl"

    rows, dup = load_all(a.corpus)
    rows = [r for r in rows if a.d_from <= r["day"] <= a.d_to]
    titles_p = a.titles or f"data/tagged/titles_{a.board}.jsonl"
    notitle = set()
    if Path(titles_p).exists():
        for l in open(titles_p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                if not r.get("has_title", True):
                    notitle.add(str(r["id"]))
    else:
        print(f"NOTE: {titles_p} not found, a posting counts as title-less when its title field is empty")
        notitle = {str(r["item"]["id"]) for r in rows if not (r["item"].get("title") or "").strip()}
    n_nt = sum(str(r["item"]["id"]) in notitle for r in rows)
    n_all = len(rows)
    month_tbl = [(r["day"][:7], str(r["item"]["id"]) in notitle, r["w"]) for r in rows]
    if a.titled_only:
        rows = [r for r in rows if str(r["item"]["id"]) not in notitle]
    lab = {}
    if Path(labels_p).exists():
        for l in open(labels_p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                lab[str(r["id"])] = int(r["cluster"])
    else:
        print(f"NOTE: {labels_p} not found, the cluster dimension is left out")
    flag = {}
    for p in a.tags or []:
        if not Path(p).exists():
            raise SystemExit(f"tags file not found: {p}")
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                if r.get("ok") and r.get("channel") in CH:
                    flag[str(r["posting_id"])] = r["channel"]

    days = sorted({r["day"] for r in rows})
    di = {d: i for i, d in enumerate(days)}
    D = len(days)
    dix = np.array([di[r["day"]] for r in rows])
    w = np.array([r["w"] for r in rows])
    ids = [str(r["item"]["id"]) for r in rows]
    taken_d = np.bincount(dix, minlength=D)
    pop_d = np.bincount(dix, weights=w, minlength=D)

    dims = {}
    cats = {
        "cluster": [("c%d" % lab[i]) if i in lab else "(unlabelled)" for i in ids] if lab else None,
        "channel": [flag.get(i, "none") for i in ids],
        "sector": [sector(r["item"]) for r in rows],
    }
    for name, vals in cats.items():
        if vals is None:
            continue
        u = sorted(set(vals))
        ui = {c: k for k, c in enumerate(u)}
        M = np.zeros((D, len(u)))
        np.add.at(M, (dix, np.array([ui[v] for v in vals])), 1.0)
        dims[name] = (u, M)

    out, L = [], []
    L.append(f"# Composition stability: {a.board} input {a.input}\n")
    L.append(f"Days {days[0]} to {days[-1]}: {D} sampled days, {len(rows):,} postings taken (duplicates removed: {dup}). "
             f"Distance = Jensen-Shannon (0 to 1); p from {a.perm} shuffles of whole days; excess = distance minus the mean shuffled distance.\n")

    # ---- field fill by quarter
    L.append("## 0. Field fill and volume by quarter\n")
    L.append("| quarter | sampled days | postings taken | mean day total | sector field filled | labelled by script 92 |")
    L.append("|---|---|---|---|---|---|")
    qd0 = np.array([quarter(d) for d in days])
    sec_none = np.array([v == "(none)" for v in cats["sector"]])
    dq = np.array([quarter(days[i]) for i in dix])
    for q in sorted(set(qd0)):
        m_ = dq == q
        dd = qd0 == q
        lab_share = f"{np.mean([x != '(unlabelled)' for x, mm in zip(cats['cluster'], m_) if mm]):.0%}" if cats["cluster"] else "-"
        L.append(f"| {q} | {dd.sum()} | {m_.sum():,} | {pop_d[dd].mean():,.0f} | {1 - sec_none[m_].mean():.0%} | {lab_share} |")
    L.append("")

    L.append(f"Postings without a title: {n_nt:,} of {n_all:,} taken"
             + (" (left out of every test below: --titled-only)" if a.titled_only else "") + ".\n")
    L.append("Share of postings without a title by month, before any exclusion (taken; weighted):\n")
    L.append("| month | postings taken | without title (taken) | without title (weighted) |")
    L.append("|---|---|---|---|")
    mo = np.array([m for m, _, _ in month_tbl])
    nt_flag = np.array([f for _, f, _ in month_tbl])
    wt_ = np.array([x for _, _, x in month_tbl])
    for m_ in sorted(set(mo)):
        k_ = mo == m_
        L.append(f"| {m_} | {k_.sum():,} | {nt_flag[k_].mean():.0%} | {wt_[k_ & nt_flag].sum() / wt_[k_].sum():.0%} |")
    L.append("")

    # ---- part 1: volume split
    L.append("## 1. Low-volume against high-volume days\n")
    order = np.argsort(pop_d, kind="stable")
    k = D // 3
    low, high = order[:k], order[-k:]
    L.append(f"Thirds by day total: low = {k} days (median total {np.median(pop_d[low]):,.0f}), high = {k} days (median total {np.median(pop_d[high]):,.0f}).\n")
    L.append("| composition | JS | shuffled mean | excess | p |")
    L.append("|---|---|---|---|---|")
    for name, (u, M) in dims.items():
        r = compare(M, low, high, rng, a.perm)
        if r:
            L.append(f"| {name} | {r['js']:.3f} | {r['null']:.3f} | {r['excess']:.3f} | {r['p']:.3f} |")
            out.append({"part": "volume split", "what": "all days", "dimension": name, **r})
    L.append("")
    L.append("Same split inside each calendar quarter AND weekday (days ranked within the same quarter and weekday; thirds pooled). A trend in the mix, "
             "or a weekend/weekday difference, would not survive this.\n")
    qd = np.array([quarter(d) + "|" + str(date.fromisoformat(d).weekday()) for d in days])
    lo2, hi2 = [], []
    for q in sorted(set(qd)):
        ix = np.where(qd == q)[0]
        if len(ix) < 6:
            continue
        o = ix[np.argsort(pop_d[ix], kind="stable")]
        kk = len(o) // 3
        lo2 += list(o[:kk])
        hi2 += list(o[-kk:])
    lo2, hi2 = np.array(lo2), np.array(hi2)
    L.append("| composition | JS | shuffled mean | excess | p |")
    L.append("|---|---|---|---|---|")
    for name, (u, M) in dims.items():
        # shuffle inside quarters: swap labels only between days of the same quarter
        A, B = M[lo2].sum(0), M[hi2].sum(0)
        n_eq = int(min(A.sum(), B.sum()))
        d = float(np.mean([jse(A, B, n_eq, rng) for _ in range(5)]))
        nulls = np.empty(a.perm)
        qlo, qhi = qd[lo2], qd[hi2]
        for i in range(a.perm):
            sa, sb = [], []
            for q in set(qlo) | set(qhi):
                pool = np.concatenate([lo2[qlo == q], hi2[qhi == q]])
                s = rng.permutation(pool)
                sa += list(s[:(qlo == q).sum()])
                sb += list(s[(qlo == q).sum():])
            nulls[i] = jse(M[sa].sum(0), M[sb].sum(0), n_eq, rng)
        L.append(f"| {name} | {d:.3f} | {nulls.mean():.3f} | {d - nulls.mean():.3f} | {(nulls >= d).mean() + 1 / a.perm:.3f} |")
        out.append({"part": "volume split", "what": "inside quarters", "dimension": name, "js": d, "null": float(nulls.mean()),
                    "excess": d - float(nulls.mean()), "p": float((nulls >= d).mean() + 1 / a.perm)})
    L.append("")

    # ---- parts 2 and 3: jumps and placebo
    S = a.span_days
    cal = np.array([date.fromisoformat(d).toordinal() for d in days])
    med = np.mean
    cand = []
    for i in range(S, D - S + 1):
        bef, aft = np.arange(i - S, i), np.arange(i, i + S)
        if cal[i + S - 1] - cal[i - S] > 2 * S + 6:
            continue
        if taken_d[bef].sum() < a.min_taken or taken_d[aft].sum() < a.min_taken:
            continue
        mb, ma = med(pop_d[bef]), med(pop_d[aft])
        r = ma / mb if mb > 0 else np.inf
        cand.append((i, r, bef, aft, mb, ma))
    jumps, plac = [], []
    taken_pos = []
    for c in sorted((c for c in cand if c[1] >= a.ratio or c[1] <= 1 / a.ratio), key=lambda c: -abs(np.log(c[1]) if np.isfinite(c[1]) else 99)):
        if all(abs(c[0] - t) >= S for t in taken_pos):
            jumps.append(c)
            taken_pos.append(c[0])
    jumps.sort(key=lambda c: c[0])
    last = -10 ** 9
    for c in cand:
        if 1 / a.placebo_ratio <= c[1] <= a.placebo_ratio and c[0] - last >= 2 * S and all(abs(c[0] - t) >= 2 * S for t in taken_pos):
            plac.append(c)
            last = c[0]

    L.append(f"## 2. Jumps in the day total (mean of the next {S} sampled days / mean of the previous {S}: >= {a.ratio:g} or <= 1/{a.ratio:g})\n")
    L.append(f"{len(jumps)} jumps compared ({S} sampled days before against {S} after, the strongest change in each stretch); "
             f"{len(plac)} stretches with no jump (ratio within 1/{a.placebo_ratio:g} to {a.placebo_ratio:g}, no overlap) kept as placebo.\n")
    head = "| first day after the jump | ratio | mean day total before -> after | " + " | ".join(f"{n}: JS (excess, p)" for n in dims) + " |"
    L.append(head)
    L.append("|" + "---|" * (3 + len(dims)))
    for (i, r, bef, aft, mb, ma) in jumps:
        cells = []
        for name, (u, M) in dims.items():
            v = compare(M, bef, aft, rng, a.perm)
            if v:
                out.append({"part": "jump", "what": days[i], "dimension": name, "ratio": r, **v})
            cells.append(f"{v['js']:.3f} ({v['excess']:+.3f}, p={v['p']:.3f})" if v else "-")
        L.append(f"| {days[i]} | {r:.1f} | {mb:,.0f} -> {ma:,.0f} | " + " | ".join(cells) + " |")
    L.append("")

    L.append("## 3. Placebo: stretches without a jump\n")
    L.append("| composition | stretches | median JS | 95th percentile JS | median excess | share with p < 0.05 |")
    L.append("|---|---|---|---|---|---|")
    pl_by = {n: [] for n in dims}
    sub = plac if len(plac) <= 60 else [plac[i] for i in rng.choice(len(plac), 60, replace=False)]
    for (i, r, bef, aft, mb, ma) in sub:
        for name, (u, M) in dims.items():
            v = compare(M, bef, aft, rng, a.perm)
            if v:
                pl_by[name].append(v)
                out.append({"part": "placebo", "what": days[i], "dimension": name, "ratio": r, **v})
    for name, vs in pl_by.items():
        if vs:
            js_ = np.array([v["js"] for v in vs])
            L.append(f"| {name} | {len(vs)}{' (random 60 of ' + str(len(plac)) + ')' if len(plac) > 60 else ''} | {np.median(js_):.3f} | {np.percentile(js_, 95):.3f} | "
                     f"{np.median([v['excess'] for v in vs]):+.3f} | {np.mean([v['p'] < 0.05 for v in vs]):.0%} |")
    L.append("")
    L.append("## Reading notes\n")
    L += ["- A jump whose JS and excess clearly exceed the placebo 95th percentile, with p near 0, is evidence that the mix moved with the volume. Jumps inside the placebo range are consistent with volume only.",
          "- Real day-to-day variation (weekday effects, seasonality, events) is inside the placebo, so a stable-mechanism board will not show 5% rejections exactly; compare the jumps with the placebo, not with 0.05.",
          "- Page clumping: the shuffle moves whole days, so it already includes the clumping within a page.",
          "- The cluster dimension depends on script 92 (clusters are fitted on all postings); the channel and sector dimensions do not.",
          "- Passing the test does not show that Skillab's ingestion is random; failing it shows that it was not stable."]
    Path("docs").mkdir(exist_ok=True)
    Path("data/cluster").mkdir(parents=True, exist_ok=True)
    tag = f"{a.board}_{a.input}" + ("_titled" if a.titled_only else "")
    Path(f"docs/composition_stability_{tag}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    with open(f"data/cluster/composition_stability_{tag}.csv", "w", newline="", encoding="utf-8") as f:
        keys = ["part", "what", "dimension", "ratio", "js", "null", "excess", "p"]
        wr = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(out)
    print(f"docs/composition_stability_{tag}.md written ({len(jumps)} jumps, {len(plac)} placebo boundaries)")


if __name__ == "__main__":
    main()
