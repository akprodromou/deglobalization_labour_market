"""
Month 3, step 5: Skill Surge Index (indicator 1 of the brief), computed quarter by quarter.

    SSI(s, t) = share(s, t) / share(s, baseline)

share(s, t) = weighted share of ALL postings of quarter t that contain the skill s.
A value of 3.2 means the skill appears 3.2 times as often as in the baseline; below 1.0 it
is shrinking. "Skill" is taken at four levels, so that the rare ones can borrow strength:

    ANY            the posting contains at least one lexicon term (the lexicon-flagged set)
    channel:<c>    at least one lexicon term of channel c (taken from the lexicon file, no model involved)
    term:<s>       one lexicon term
    tag:<c>        the posting is tagged with channel c by the model (optional, --tags); this is the
                   "validated" reading: the lexicon found a term AND the model judged the posting to be
                   about the channel. Tag-based series carry the tagger's errors (see the methodology document).

Baseline. The brief uses 2019, but the corpus starts in 2024 (OJA is excluded), so the baseline is
the period BEFORE the Critical Raw Materials Act (23 May 2024): 1 January to 30 April 2024 by default
(--base-first, --base-last). It holds only about 1,100 postings, so baseline shares are noisy and many
ratios are wide; every ratio therefore comes with a 95% interval, and a term is shown in the report only if at least
--min-base postings that contain it were taken in the baseline (default 10). The CSV keeps all series.
Quarters 2024Q1 and 2024Q2 overlap the baseline (April belongs to 2024Q2): their ratios are not
independent of it. The last quarter (2026Q3) is incomplete.

Weights and intervals as in script 64: day weights from the corpus (duplicates removed, all files read as
one corpus), bootstrap resampling postings inside each day. The ratio's interval is the 2.5 and 97.5
percentile of share_t / share_baseline over the draws (draws with a zero baseline share are dropped; when
the observed baseline share is zero the index is undefined and is left empty).

The composition of a thin baseline can differ from later quarters (employers, sources): run script 33 before
reading a surge as a change in demand.

Run (project root, venv active; same file list as script 64):
    python -m diagnostics.65_skill_surge_index \\
        --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl \\
                 data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl \\
        --flagged data/tagged/flagged_corpus_jobbland.se_2024-01_2026-09.jsonl \\
        --tags data/tagged/tags_qwen2.5_7b_tagging_v8.jsonl
Writes docs/skill_surge_index.md and data/tagged/skill_surge_index.csv.
"""

import argparse
import csv
import json
import tempfile
from collections import defaultdict
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

CHANNELS = ["reshoring", "defense", "critical materials", "energy security",
            "trade compliance", "diversification"]


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


def quarter(day):
    return f"{day[:4]}Q{(int(day[5:7]) - 1) // 3 + 1}"


def fmt(x, nd=2):
    return "" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{nd}f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--flagged", required=True)
    ap.add_argument("--lexicon", default="lexicon/lexicon.csv")
    ap.add_argument("--tags", default=None)
    ap.add_argument("--base-first", default="2024-01-01")
    ap.add_argument("--base-last", default="2024-04-30")
    ap.add_argument("--min-base", type=int, default=10)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--out-md", default="docs/skill_surge_index.md")
    ap.add_argument("--out-csv", default="data/tagged/skill_surge_index.csv")
    args = ap.parse_args()

    rows, dup = load_all(args.corpus)
    chan_of = {r["term"]: r["channel"] for r in csv.DictReader(open(args.lexicon, encoding="utf-8-sig"))}
    flagged = {}
    for line in open(args.flagged, encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            flagged[str(r["posting_id"])] = r["terms"]
    tags = {}
    if args.tags:
        for line in open(args.tags, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                if r.get("ok") and r.get("channel") in CHANNELS:
                    tags[str(r["posting_id"])] = r["channel"]

    series = ["ANY"] + [f"channel:{c}" for c in CHANNELS]
    terms = sorted({t for ts in flagged.values() for t in ts})
    series += [f"term:{t}" for t in terms]
    if tags:
        series += [f"tag:{c}" for c in CHANNELS]
    sidx = {s: i for i, s in enumerate(series)}
    S = len(series)

    def member(pid):
        v = np.zeros(S, dtype=np.int32)
        ts = flagged.get(pid)
        if ts is None:
            return None
        v[sidx["ANY"]] = 1
        for t in ts:
            v[sidx[f"term:{t}"]] = 1
            c = chan_of.get(t)
            if c in CHANNELS:
                v[sidx[f"channel:{c}"]] = 1
        if tags and pid in tags:
            v[sidx[f"tag:{tags[pid]}"]] = 1
        return v

    by_day = defaultdict(lambda: {"w": 0.0, "n": 0, "rows": []})
    missing = 0
    for r in rows:
        d = by_day[r["day"]]
        d["w"] = r["w"]
        d["n"] += 1
        m = member(str(r["item"]["id"]))
        if m is not None:
            d["rows"].append(m)
    in_corpus = sum(len(d["rows"]) for d in by_day.values())
    print(f"{len(rows):,} postings ({dup:,} duplicates removed); {in_corpus:,} of {len(flagged):,} flagged postings found in the corpus; "
          f"{len(terms)} lexicon terms occur; {S} series")

    keys = sorted(by_day)
    w = np.array([by_day[k]["w"] for k in keys])
    n = np.array([by_day[k]["n"] for k in keys])
    M = [np.array(by_day[k]["rows"]) if by_day[k]["rows"] else np.zeros((0, S), dtype=np.int32) for k in keys]
    C = np.array([m.sum(axis=0) for m in M], dtype=float)                      # days x series

    quarters = sorted({quarter(k) for k in keys})
    groups = [[i for i, k in enumerate(keys) if quarter(k) == q] for q in quarters]
    base = [i for i, k in enumerate(keys) if args.base_first <= k <= args.base_last]
    groups.append(base)
    labels = quarters + ["baseline"]
    G = np.zeros((len(groups), len(keys)))
    for g, idxs in enumerate(groups):
        G[g, idxs] = 1
    B = len(labels) - 1
    taken = G @ n
    pop = G @ (w * n)
    print(f"baseline {args.base_first} to {args.base_last}: {int(taken[B]):,} postings taken, about {pop[B]:,.0f} in the population")
    if taken[B] == 0:
        raise SystemExit("No postings in the baseline period: check --base-first / --base-last.")

    def share(counts):
        return (G @ (w[:, None] * counts)) / pop[:, None]

    obs = share(C)
    taken_series = G @ C                                                        # postings taken containing the series

    rng = np.random.default_rng(args.seed)
    f_idx = [i for i in range(len(keys)) if len(M[i])]
    boot = np.zeros((args.boot,) + obs.shape, dtype=np.float32)
    for b in range(args.boot):
        Cb = np.zeros_like(C)
        for i in f_idx:
            f = len(M[i])
            p = np.full(f + 1, 1.0 / n[i])
            p[f] = (n[i] - f) / n[i]
            k = rng.multinomial(int(n[i]), p)
            Cb[i] = k[:f] @ M[i]
        boot[b] = share(Cb)

    def index_ci(g, s):
        base_obs = obs[B, s]
        if base_obs <= 0:
            return None, None, None
        ratio_obs = obs[g, s] / base_obs
        bb = boot[:, B, s]
        ok = bb > 0
        if ok.sum() < 20:
            return ratio_obs, None, None
        r = boot[ok, g, s] / bb[ok]
        return ratio_obs, float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))

    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["series", "quarter", "postings_taken", "taken_with_series", "share", "baseline_share",
                     "baseline_taken_with_series", "index", "ci_low", "ci_high"])
        for s, name in enumerate(series):
            for g, q in enumerate(quarters):
                ix, lo, hi = index_ci(g, s)
                wr.writerow([name, q, int(taken[g]), int(taken_series[g, s]), round(float(obs[g, s]), 6),
                             round(float(obs[B, s]), 6), int(taken_series[B, s]),
                             "" if ix is None else round(ix, 4), "" if lo is None else round(lo, 4),
                             "" if hi is None else round(hi, 4)])

    def cell(g, s):
        ix, lo, hi = index_ci(g, s)
        if ix is None:
            return "undefined"
        return f"{ix:.2f} ({fmt(lo)} to {fmt(hi)})" if lo is not None else f"{ix:.2f}"

    L = ["# Skill Surge Index", "",
         f"Baseline: {args.base_first} to {args.base_last} ({int(taken[B]):,} postings taken, about {pop[B]:,.0f} in the population). "
         f"Index = weighted share of postings in the quarter that contain the skill / the same share in the baseline; 1.00 = unchanged. "
         f"95% bootstrap intervals in brackets ({args.boot} draws, resampling inside each day). 2024Q1 and 2024Q2 overlap the baseline; "
         f"2026Q3 is incomplete. A thin baseline gives wide intervals: read the interval, not the point value.", ""]
    names = [("ANY", "Any lexicon term")] + [(f"channel:{c}", f"Lexicon channel: {c}") for c in CHANNELS]
    if tags:
        names += [(f"tag:{c}", f"Model-tagged channel: {c}") for c in CHANNELS]
    L += ["## Baseline counts", "", "| Series | Postings taken with the skill in the baseline | Baseline share (%) |", "|---|---:|---:|"]
    for sname, label in names:
        s = sidx[sname]
        L.append(f"| {label} | {int(taken_series[B, s])} | {100 * obs[B, s]:.2f} |")
    L.append("")
    for block, title in (("ANY|channel", "Lexicon-based series"), ("tag", "Model-tagged channels (validated reading)")):
        sel = [x for x in names if (x[0] == "ANY" or x[0].startswith("channel:"))] if block == "ANY|channel" else [x for x in names if x[0].startswith("tag:")]
        if not sel:
            continue
        L += [f"## {title}", "", "| Quarter | " + " | ".join(l for _, l in sel) + " |", "|---|" + "---|" * len(sel)]
        for g, q in enumerate(quarters):
            L.append(f"| {q}{' (incomplete)' if q == quarters[-1] else ''} | " + " | ".join(cell(g, sidx[sn]) for sn, _ in sel) + " |")
        L.append("")

    pick = [q for q in quarters if q[-2:] in ("Q2", "Q4") and q > "2024Q2"][-4:]
    ok_terms = [t for t in terms if taken_series[B, sidx[f"term:{t}"]] >= args.min_base]
    L += [f"## Terms with at least {args.min_base} baseline postings", ""]
    if ok_terms:
        L += ["| Term | Channel | Baseline postings | " + " | ".join(pick) + " |", "|---|---|---:|" + "---|" * len(pick)]
        for t in sorted(ok_terms, key=lambda t: -taken_series[B, sidx[f"term:{t}"]]):
            s = sidx[f"term:{t}"]
            L.append(f"| {t} | {chan_of.get(t, '')} | {int(taken_series[B, s])} | " + " | ".join(cell(quarters.index(q), s) for q in pick) + " |")
    else:
        L.append("No single term reaches the minimum in the baseline: single-term indices are not reported. "
                 "Use the channel series; the CSV has every term with its baseline count.")
    L += ["", f"{sum(1 for t in terms if taken_series[B, sidx[f'term:{t}']] == 0)} of {len(terms)} occurring terms have no baseline posting at all: "
          "their index is undefined. Terms that first appear after the baseline are listed in the CSV with an empty index."]
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {args.out_md} and {args.out_csv}")


if __name__ == "__main__":
    main()
