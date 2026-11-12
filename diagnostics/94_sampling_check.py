"""
Month 4: does clumping inside a day make the within-day bootstrap too narrow?

Three checks on one board, using the day-stratified corpus of script 52.

1. Employer concentration per day. A day's page holds about 100 adjacent postings. If a few employers
   supply most of them, the postings are not independent draws. Reported: share of postings without an
   employer, and per day the top employer's share and the effective number of employers (1 / sum of squared
   shares); quantiles over days.
2. Three 95% intervals for the weighted quarterly share of an indicator (default: any Month 3 flag):
     A  posting bootstrap inside each day (the method of scripts 60 and 84: independent postings)
     B  employer-cluster bootstrap inside each day (whole employers redrawn: allows for clumping)
     C  week-block bootstrap (whole ISO weeks redrawn: allows for clumping AND for day-to-day variation)
   Reported per quarter: share, the three interval widths, and the ratios B/A and C/A.
   Design effect from clumping = (B/A) squared. A ratio near 1 means the independence assumption costs little.
3. Reading rule (not a test of significance): B/A well above 1 means the within-day interval is too narrow;
   C/A above B/A means day-to-day variation adds more; C/A below 1 means weeks are less variable than
   binomial noise (possible with few weeks).

Indicator. --tags takes the tag files (same rule as script 84: flagged = channel other than none and valid).
Without --tags, --title-regex defines it (case-insensitive, on the raw title).

Run (project root, venv active), jobbland example:
    python -m diagnostics.94_sampling_check --label jobbland --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl --tags data/tagged/tags_v12_jobbland.final.post.jsonl

Writes docs/sampling_check_<label>.md and data/tagged/sampling_check_<label>.csv.
"""

import argparse
import csv
import json
import re
import tempfile
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

CHANNELS = {"reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"}


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


def read_flags(paths):
    flags = {}
    for p in paths:
        for line in open(p, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            flags[str(r["posting_id"])] = int(bool(r.get("ok")) and r.get("channel") in CHANNELS)
    return flags


def org_key(it, i, mode="organization"):
    """Cluster key. organization: the employer field. text: first 80 characters of the description, a proxy for
    employers that post from one template (use when the employer field is empty, as on jobbland.se)."""
    src = it.get("organization") if mode == "organization" else (it.get("description") or "")[:80]
    o = re.sub(r"\W+", " ", (src or "").lower()).strip()
    return o if o else f"__missing_{i}"  # a posting without employer is its own cluster


def quarter(day):
    y, m, _ = day.split("-")
    return f"{y}-Q{(int(m) - 1) // 3 + 1}"


def week(day):
    y, w, _ = date.fromisoformat(day).isocalendar()
    return f"{y}-W{w:02d}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--tags", nargs="+")
    ap.add_argument("--title-regex")
    ap.add_argument("--cluster-by", choices=["organization", "text"], default="organization",
                    help="what counts as one employer in interval B (text = first 80 characters of the description)")
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--min-days", type=int, default=20, help="quarters with fewer sampled days are skipped")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    if not args.tags and not args.title_regex:
        ap.error("give --tags or --title-regex")
    rng = np.random.default_rng(args.seed)
    rows, dup = load_all(args.corpus)
    flags = read_flags(args.tags) if args.tags else None
    rx = re.compile(args.title_regex, re.I) if args.title_regex else None

    days = defaultdict(lambda: {"W": 0.0, "org": [], "y": []})
    for i, r in enumerate(rows):
        it = r["item"]
        d = days[r["day"]]
        d["W"] += r["w"]  # day total (weights sum to it)
        d["org"].append(org_key(it, i, args.cluster_by))
        y = flags.get(str(it["id"]), 0) if flags is not None else int(bool(rx.search(it.get("title") or "")))
        d["y"].append(y)

    # 1. employer concentration
    top, eff, miss, n_all = [], [], 0, 0
    for k, d in days.items():
        c = defaultdict(int)
        for o in d["org"]:
            c[o] += 1
            n_all += 1
            miss += o.startswith("__missing_")
        s = np.array(list(c.values()), float)
        s = s / s.sum()
        top.append(s.max())
        eff.append(1.0 / (s ** 2).sum())
    q = lambda a: [float(np.quantile(a, x)) for x in (0.1, 0.5, 0.9)]

    # 2. intervals per quarter
    byq = defaultdict(list)
    for k in sorted(days):
        byq[quarter(k)].append(k)
    out = []
    for qq, ks in sorted(byq.items()):
        if len(ks) < args.min_days:
            continue
        W = np.array([days[k]["W"] for k in ks])
        n = np.array([len(days[k]["y"]) for k in ks])
        c = np.array([sum(days[k]["y"]) for k in ks], float)
        est = (W * c / n).sum() / W.sum()
        # A: binomial inside each day
        cs = rng.binomial(n[None, :], (c / n)[None, :], size=(args.boot, len(ks)))
        A = ((W * cs / n).sum(1)) / W.sum()
        # B: employer clusters inside each day
        num = np.zeros(args.boot)
        for j, k in enumerate(ks):
            d = days[k]
            g = defaultdict(lambda: [0, 0])
            for o, y in zip(d["org"], d["y"]):
                g[o][0] += 1
                g[o][1] += y
            m = np.array([v[0] for v in g.values()], float)
            s = np.array([v[1] for v in g.values()], float)
            idx = rng.integers(0, len(m), size=(args.boot, len(m)))
            num += W[j] * s[idx].sum(1) / m[idx].sum(1)
        B = num / W.sum()
        # C: whole ISO weeks
        wk = defaultdict(lambda: [0.0, 0.0])
        for j, k in enumerate(ks):
            w_ = wk[week(k)]
            w_[0] += W[j] * c[j] / n[j]
            w_[1] += W[j]
        a = np.array(list(wk.values()))
        idx = rng.integers(0, len(a), size=(args.boot, len(a)))
        C = a[idx, 0].sum(1) / a[idx, 1].sum(1)
        wd = lambda x: float(np.quantile(x, 0.975) - np.quantile(x, 0.025))
        wa, wb, wc = wd(A), wd(B), wd(C)
        out.append({"quarter": qq, "days": len(ks), "postings": int(n.sum()), "weeks": len(a), "share": est,
                    "width_A": wa, "width_B": wb, "width_C": wc,
                    "B_over_A": wb / wa if wa else float("nan"), "C_over_A": wc / wa if wa else float("nan")})

    Path("docs").mkdir(exist_ok=True)
    Path("data/tagged").mkdir(parents=True, exist_ok=True)
    with open(f"data/tagged/sampling_check_{args.label}.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(out[0].keys()) if out else ["quarter"])
        wr.writeheader()
        wr.writerows(out)
    ind = "any Month 3 flag" if flags is not None else f"title matches /{args.title_regex}/"
    md = [f"# Sampling check: {args.label}", "",
          f"Indicator: {ind}. {len(rows):,} postings after {dup:,} exact duplicates, {len(days):,} sampled days, {args.boot} draws. "
          f"Intervals are 95%; widths are in share units (0.01 = 1 percentage point).", "",
          "## Employer concentration inside a day", "",
          f"Cluster key: {args.cluster_by}. Postings without a key: {miss / n_all:.1%}. Each of those counts as its own cluster.", "",
          "| measure | 10th pct of days | median day | 90th pct of days |", "|---|---|---|---|",
          "| top employer's share of the day's page | " + " | ".join(f"{x:.1%}" for x in q(top)) + " |",
          "| effective number of employers per page | " + " | ".join(f"{x:.1f}" for x in q(eff)) + " |", "",
          "## Interval widths per quarter", "",
          "A = postings redrawn inside each day; B = employers redrawn inside each day; C = whole ISO weeks redrawn.", "",
          "| quarter | days | weeks | postings | share | width A | width B | width C | B/A | C/A |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in out:
        md.append(f"| {r['quarter']} | {r['days']} | {r['weeks']} | {r['postings']} | {r['share']:.3f} | {r['width_A']:.4f} | "
                  f"{r['width_B']:.4f} | {r['width_C']:.4f} | {r['B_over_A']:.2f} | {r['C_over_A']:.2f} |")
    md += ["", "Reading: B/A above 1 means the within-day interval is too narrow because of employer clumping (design effect = (B/A) squared). "
           "C/A above B/A means day-to-day variation adds to it. Quarters with few weeks give noisy C."]
    # weekly series: which weeks drive the week-block intervals
    wkd = defaultdict(lambda: [0.0, 0.0, 0, 0, set()])
    for k, d in days.items():
        w_ = wkd[week(k)]
        n_ = len(d["y"])
        w_[0] += d["W"] * sum(d["y"]) / n_
        w_[1] += d["W"]
        w_[2] += n_
        w_[3] += sum(d["y"])
        w_[4].add(k)
    qshare = {r["quarter"]: r["share"] for r in out}
    wrows = []
    for wk_, v in sorted(wkd.items()):
        first = min(v[4])
        wrows.append({"week": wk_, "quarter": quarter(first), "days": len(v[4]), "postings": v[2], "flagged": v[3],
                      "share": v[0] / v[1], "weighted_postings": v[1]})
    with open(f"data/tagged/weekly_share_{args.label}.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(wrows[0].keys()))
        wr.writeheader()
        wr.writerows(wrows)
    dev = sorted((r for r in wrows if r["quarter"] in qshare and r["postings"] >= 20),
                 key=lambda r: -abs(r["share"] - qshare[r["quarter"]]))[:10]
    md += ["", "## Weeks furthest from their quarter's share", "",
           "Weeks with at least 20 sampled postings. Full series in data/tagged/weekly_share_" + args.label + ".csv.", "",
           "| week | quarter | days | postings | flagged | weekly share | quarter share | weighted postings |", "|---|---|---|---|---|---|---|---|"]
    for r in dev:
        md.append(f"| {r['week']} | {r['quarter']} | {r['days']} | {r['postings']} | {r['flagged']} | {r['share']:.3f} | "
                  f"{qshare[r['quarter']]:.3f} | {r['weighted_postings']:,.0f} |")
    Path(f"docs/sampling_check_{args.label}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
