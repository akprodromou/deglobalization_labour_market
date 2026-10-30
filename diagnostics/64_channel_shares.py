"""
Month 3, step 4: weighted channel shares by month and around the two events.

What it computes. For every month, and for a window before and after each event,
the share of ALL postings (flagged or not) whose tag is a given channel:

    share = sum of day weights of postings tagged with the channel / sum of day weights of all postings

Postings the lexicon did not flag count as "none"; postings whose tag was invalid
(the model's answer could not be read) also count as "none" and are reported.
Two readings are given for each channel: any intensity, and medium or high
intensity only (intensity is exploratory, see the methodology document).

Weights. The corpus (script 52) takes up to 100 postings a day out of a day total
that varies from a few to 3,000+. A posting of day d stands for
(day total / postings taken that day) postings, after exact duplicates are removed
(corpus_io.load_corpus, the same rule as the tagger). All corpus files are read as ONE
corpus, in the same way as the merged file of the Colab notebook, so that the
duplicate removal matches the tagged set.

Intervals. 95% bootstrap intervals, resampling inside each day (the day is the
stratum, as in script 60): the postings of a day are redrawn from the day's
channel mix with a multinomial draw, the weights stay fixed. The population
correction for sampling a large part of a small day is ignored, so intervals for
very small days are slightly wide, never narrow.

Events (dates are the publication dates):
    CRMA         2024-05-23  EU Critical Raw Materials Act
    AccelerateEU 2026-04-22

The window is --window-days days before the event (event day not included) and the
same number from the event day on. Compare the number of postings taken in each
window before you read the difference: the first months of 2024 hold only 191 to
410 postings a month, so the window before the CRMA is thin.

Run (project root, venv active):
    python -m diagnostics.65_channel_shares \\
        --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl \\
                 data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl \\
                 data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl \\
                 data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl \\
        --tags data/tagged/tags_qwen2.5_7b_tagging_v8.jsonl

Options: --window-days (default 90), --boot (draws, default 1000), --seed.
Writes docs/channel_shares.md and data/tagged/channel_shares_monthly.csv.
"""

import argparse
import csv
import json
import tempfile
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

CHANNELS = ["reshoring", "defense", "critical materials", "energy security",
            "trade compliance", "diversification"]
INTENS = ["low", "medium", "high"]
EVENTS = {"CRMA": date(2024, 5, 23), "AccelerateEU": date(2026, 4, 22)}


def categories():
    cats = ["none"]
    for ch in CHANNELS:
        for it in INTENS:
            cats.append(f"{ch}|{it}")
    return cats


def load_all(paths):
    """Read several corpus files as one corpus (same duplicate rule as the merged file)."""
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


def read_tags(path):
    tags, invalid = {}, 0
    for line in open(path, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("ok") and r.get("channel") in CHANNELS and r.get("intensity") in INTENS:
            tags[str(r["posting_id"])] = f'{r["channel"]}|{r["intensity"]}'
        elif r.get("ok") and r.get("channel") == "none":
            tags[str(r["posting_id"])] = "none"
        else:
            invalid += 1
            tags[str(r["posting_id"])] = "none"
    return tags, invalid


def build_days(rows, tags, cats):
    """One record per day: weight, postings taken, counts per category."""
    idx = {c: i for i, c in enumerate(cats)}
    days = defaultdict(lambda: [0.0, 0, np.zeros(len(cats))])
    for r in rows:
        d = days[r["day"]]
        d[0] = r["w"]
        d[1] += 1
        d[2][idx[tags.get(str(r["item"]["id"]), "none")]] += 1
    keys = sorted(days)
    w = np.array([days[k][0] for k in keys])
    n = np.array([days[k][1] for k in keys])
    c = np.array([days[k][2] for k in keys])
    return keys, w, n, c


def group_matrix(keys, groups):
    """0/1 matrix (groups x days) from a list of sets of day strings."""
    m = np.zeros((len(groups), len(keys)))
    pos = {k: i for i, k in enumerate(keys)}
    for g, members in enumerate(groups):
        for k in members:
            if k in pos:
                m[g, pos[k]] = 1
    return m


def shares(G, w, counts, cats, mode):
    """Share of the population per group x channel. counts: days x cats (observed or drawn)."""
    pop = G @ (w * counts.sum(axis=1))                        # weighted postings per group
    out = np.zeros((G.shape[0], len(CHANNELS)))
    for j, ch in enumerate(CHANNELS):
        sel = [i for i, c in enumerate(cats) if c.startswith(ch + "|")
               and (mode == "any" or c.endswith(("|medium", "|high")))]
        out[:, j] = G @ (w * counts[:, sel].sum(axis=1)) / np.where(pop > 0, pop, np.nan)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--tags", required=True)
    ap.add_argument("--window-days", type=int, default=90)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--out-md", default="docs/channel_shares.md")
    ap.add_argument("--out-csv", default="data/tagged/channel_shares_monthly.csv")
    args = ap.parse_args()

    cats = categories()
    rows, dup = load_all(args.corpus)
    tags, invalid = read_tags(args.tags)
    keys, w, n, c = build_days(rows, tags, cats)
    tagged_in_corpus = sum(1 for r in rows if str(r["item"]["id"]) in tags)
    print(f"{len(rows):,} postings after removing {dup:,} duplicates; {tagged_in_corpus:,} carry a tag "
          f"({len(tags):,} tags read, {invalid} invalid answers counted as none)")

    months = sorted({k[:7] for k in keys})
    groups = [{k for k in keys if k[:7] == m} for m in months]
    labels = list(months)
    for name, ev in EVENTS.items():
        pre = {(ev - timedelta(days=i)).isoformat() for i in range(1, args.window_days + 1)}
        post = {(ev + timedelta(days=i)).isoformat() for i in range(0, args.window_days)}
        groups += [pre, post]
        labels += [f"{name} before", f"{name} after"]
    G = group_matrix(keys, groups)
    taken = G @ n
    population = G @ (w * n)

    rng = np.random.default_rng(args.seed)
    prob = c / n[:, None]
    obs = {m: shares(G, w, c, cats, m) for m in ("any", "mh")}
    boots = {m: np.zeros((args.boot,) + obs[m].shape) for m in ("any", "mh")}
    for b in range(args.boot):
        draw = np.array([rng.multinomial(int(n[i]), prob[i]) for i in range(len(keys))])
        for m in ("any", "mh"):
            boots[m][b] = shares(G, w, draw, cats, m)

    def ci(m, g, j):
        v = boots[m][:, g, j]
        v = v[~np.isnan(v)]
        return (np.percentile(v, 2.5), np.percentile(v, 97.5)) if len(v) else (np.nan, np.nan)

    # monthly csv
    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["month", "postings_taken", "weighted_postings", "channel", "reading", "share", "ci_low", "ci_high"])
        for g, m in enumerate(months):
            for mode, nm in (("any", "any intensity"), ("mh", "medium or high")):
                for j, ch in enumerate(CHANNELS):
                    lo, hi = ci(mode, g, j)
                    wr.writerow([m, int(taken[g]), round(population[g]), ch, nm,
                                 round(obs[mode][g, j], 5), round(lo, 5), round(hi, 5)])

    # report
    L = ["# Weighted channel shares", "",
         f"Tags: `{Path(args.tags).name}`. Share = weighted share of all postings (flagged or not) with the channel as tag. "
         f"95% intervals from {args.boot} bootstrap draws inside each day. Unflagged and invalid-answer postings count as none "
         f"({invalid} invalid answers). Values in per cent.", ""]
    for mode, title in (("any", "Any intensity"), ("mh", "Medium or high intensity only")):
        L += [f"## Events: {title}", "",
              "| Event | Channel | Before | After | Change (points) | 95% interval of the change |", "|---|---|---:|---:|---:|---|"]
        for name in EVENTS:
            gb, ga = labels.index(f"{name} before"), labels.index(f"{name} after")
            for j, ch in enumerate(CHANNELS):
                a, b_ = obs[mode][gb, j], obs[mode][ga, j]
                diff = boots[mode][:, ga, j] - boots[mode][:, gb, j]
                diff = diff[~np.isnan(diff)]
                lo, hi = (np.percentile(diff, 2.5), np.percentile(diff, 97.5)) if len(diff) else (np.nan, np.nan)
                L.append(f"| {name} | {ch} | {100*a:.2f} | {100*b_:.2f} | {100*(b_-a):+.2f} | {100*lo:+.2f} to {100*hi:+.2f} |")
        L.append("")
    L += ["## Postings behind each window", "",
          "| Window | Days | Postings taken | Weighted postings (population) |", "|---|---:|---:|---:|"]
    for name in EVENTS:
        for side in ("before", "after"):
            g = labels.index(f"{name} {side}")
            L.append(f"| {name} {side} | {int(G[g].sum())} | {int(taken[g]):,} | {population[g]:,.0f} |")
    L += ["", "Days with postings in a window can be fewer than the window length (the corpus ends in September 2026). "
          "A window with a few hundred postings gives wide intervals: read the interval, not the point change.", "",
          "## Monthly shares, any intensity", "",
          "| Month | Taken | " + " | ".join(CHANNELS) + " |", "|---|---:|" + "---:|" * len(CHANNELS)]
    for g, m in enumerate(months):
        L.append(f"| {m} | {int(taken[g]):,} | " + " | ".join(f"{100*obs['any'][g, j]:.2f}" for j in range(len(CHANNELS))) + " |")
    L += ["", "Intervals for every month are in the CSV."]
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {args.out_md} and {args.out_csv}")


if __name__ == "__main__":
    main()
