"""
Month 3: firm watchlist as an UPPER-BOUND sensitivity indicator (no model, no channel tag).

Why it exists. Some deglobalization investments are tied to named firms (chip makers, defence primes, cable makers).
Postings that name such a firm are counted here, apart from the validated channels, as an upper bound: a posting can name
a firm as a customer, a partner or a competitor, and the role may have nothing to do with the firm's programme. The
indicator is never added to the channel shares and no event is inferred from it alone.

What it computes. For every firm of the watchlist (and for `any firm`), by month and for a window before and after each
event given with --event: the day-weighted share of ALL postings whose title or first 6,000 characters of the description
contain one of the firm's aliases (case-insensitive, whole words; no boilerplate removal). Weights, duplicate removal and
95% bootstrap intervals are those of scripts 64, 80 and 84. If tag files are given (--tags, `.post.jsonl`), the report also
cross-tabulates the postings that name a firm with the final channel of the posting (unflagged postings count as none).

Watchlist file: firm_watchlist_candidates.csv (columns firm, aliases separated by |, sector, channel_hint, note). A firm
without aliases is skipped. Aliases are literal: read the contexts file before quoting a share (the contexts of every alias
are listed with a few snippets).

Run (project root), one run per board, for example:
    python -m diagnostics.88_firm_watchlist_indicator \\
        --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl \\
                 data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl \\
        --tags data/tagged/tags_v12_jobbland.final.post.jsonl --label jobbland \\
        --event CRMA=2024-05-23 --event AccelerateEU=2026-04-22
Writes docs/firm_watchlist_<label>.md and data/tagged/firm_watchlist_<label>_monthly.csv.
"""
import argparse
import csv
import json
import random
import re
import tempfile
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus


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


def text_of(item, n=6000):
    return ((item.get("title") or "").strip() + ". " + (item.get("description") or ""))[:n]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--watchlist", default="firm_watchlist_candidates.csv")
    ap.add_argument("--tags", nargs="*", default=[])
    ap.add_argument("--label", required=True)
    ap.add_argument("--event", action="append", default=[])
    ap.add_argument("--window-days", type=int, default=90)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--contexts", type=int, default=3)
    a = ap.parse_args()

    firms = []
    for r in csv.DictReader(open(a.watchlist, encoding="utf-8-sig")):
        aliases = [x.strip() for x in (r.get("aliases") or "").split("|") if x.strip()]
        if not aliases:
            print(f"skipped (no alias): {r['firm']}")
            continue
        rx = re.compile(r"(?<![\w])(?:" + "|".join(re.escape(x) for x in aliases) + r")(?![\w])", re.I)
        firms.append((r["firm"], rx, r.get("sector", ""), r.get("channel_hint", "")))
    names = [f[0] for f in firms] + ["any firm"]
    events = {}
    for e in a.event:
        n, _, d = e.partition("=")
        events[n] = date.fromisoformat(d)

    tags = {}
    for p in a.tags:
        for line in open(p, encoding="utf-8"):
            if line.strip():
                t = json.loads(line)
                tags[str(t["posting_id"])] = t.get("channel") or "invalid"

    rows, dropped = load_all(a.corpus)
    print(f"{len(rows):,} postings after removing {dropped:,} exact duplicates")
    days = defaultdict(lambda: [0.0, 0, np.zeros(len(names))])
    cross = defaultdict(Counter)       # firm -> channel -> postings (unweighted)
    snippets = defaultdict(list)
    seen = Counter()
    rng = random.Random(a.seed)
    for r in rows:
        txt = text_of(r["item"])
        d = days[r["day"]]
        d[0] = r["w"]
        d[1] += 1
        any_hit = False
        ch = tags.get(str(r["item"]["id"]), "none") if tags else None
        for i, (name, rx, _, _) in enumerate(firms):
            m = rx.search(txt)
            if not m:
                continue
            any_hit = True
            d[2][i] += 1
            if ch is not None:
                cross[name][ch] += 1
            seen[name] += 1
            snip = txt[max(0, m.start() - 70): m.end() + 70].replace("\n", " ")
            if len(snippets[name]) < a.contexts:
                snippets[name].append(snip)
            else:
                j = rng.randint(0, seen[name] - 1)
                if j < a.contexts:
                    snippets[name][j] = snip
        if any_hit:
            d[2][len(firms)] += 1
            if ch is not None:
                cross["any firm"][ch] += 1
                seen["any firm"] += 1

    keys = sorted(days)
    w = np.array([days[k][0] for k in keys])
    n = np.array([days[k][1] for k in keys])
    c = np.array([days[k][2] for k in keys])
    months = sorted({k[:7] for k in keys})
    groups = [("month " + m, {k for k in keys if k.startswith(m)}) for m in months]
    for nm, ev in events.items():
        before = {(ev - timedelta(days=i)).isoformat() for i in range(1, a.window_days + 1)}
        after = {(ev + timedelta(days=i)).isoformat() for i in range(0, a.window_days)}
        groups += [(f"{nm}: {a.window_days} days before", before), (f"{nm}: {a.window_days} days from event", after)]
    pos = {k: i for i, k in enumerate(keys)}
    G = np.zeros((len(groups), len(keys)))
    for g, (_, members) in enumerate(groups):
        for k in members:
            if k in pos:
                G[g, pos[k]] = 1

    def share(counts):
        pop = G @ (w * n)
        num = G @ (w[:, None] * counts)
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(pop[:, None] > 0, num / pop[:, None], np.nan)

    obs = share(c)
    nprng = np.random.default_rng(a.seed)
    p = np.divide(c, n[:, None], out=np.zeros_like(c), where=n[:, None] > 0)
    boots = np.zeros((a.boot,) + obs.shape)
    for b in range(a.boot):
        boots[b] = share(nprng.binomial(n[:, None].astype(int), p).astype(float))
    lo, hi = np.nanpercentile(boots, 2.5, axis=0), np.nanpercentile(boots, 97.5, axis=0)

    Path("data/tagged").mkdir(parents=True, exist_ok=True)
    Path("docs").mkdir(exist_ok=True)
    csv_path = Path(f"data/tagged/firm_watchlist_{a.label}_monthly.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["group", "postings_taken", "firm", "share", "ci_low", "ci_high"])
        for g, (name, members) in enumerate(groups):
            taken = int(sum(n[pos[k]] for k in members if k in pos))
            for i, nm in enumerate(names):
                wr.writerow([name, taken, nm, f"{obs[g][i]:.5f}", f"{lo[g][i]:.5f}", f"{hi[g][i]:.5f}"])

    md = [f"# Firm watchlist indicator: {a.label}", "",
          "Share of all postings (day-weighted) that name a firm of the watchlist, with 95% bootstrap intervals. This is an upper "
          "bound: a posting can name a firm as a customer, partner or competitor. It is not a channel tag and is not mixed with the "
          "channel shares.", "", f"Postings read: {len(rows):,} (exact duplicates removed: {dropped:,}). Watchlist: `{a.watchlist}`.", "",
          "## Postings that name each firm (unweighted)", "", "| firm | sector | channel hint | postings |" + (" tagged channel of those postings |" if tags else ""),
          "|---|---|---|---:|" + ("---|" if tags else "")]
    for nm, _, sec, hint in firms:
        extra = ""
        if tags:
            extra = " " + ", ".join(f"{k} {v}" for k, v in cross[nm].most_common()) + " |"
        md.append(f"| {nm} | {sec} | {hint} | {seen.get(nm, 0)} |" + extra)
    md.append(f"| any firm | | | {seen.get('any firm', 0)} |" + ((" " + ", ".join(f"{k} {v}" for k, v in cross['any firm'].most_common()) + " |") if tags else ""))
    md += ["", "## Weighted share by period (any firm)", "", "| group | postings taken | any firm |", "|---|---:|---|"]
    for g, (name, members) in enumerate(groups):
        taken = int(sum(n[pos[k]] for k in members if k in pos))
        i = len(firms)
        md.append(f"| {name} | {taken} | {100 * obs[g][i]:.2f}% ({100 * lo[g][i]:.2f} to {100 * hi[g][i]:.2f}) |" if not np.isnan(obs[g][i]) else f"| {name} | {taken} | n/a |")
    md += ["", "The share of each single firm by period is in the CSV.", "", "## Contexts to check by eye", ""]
    for nm, *_ in firms:
        md.append(f"### {nm}: {seen.get(nm, 0)} postings")
        md += [f"- {s}" for s in snippets.get(nm, [])]
        md.append("")
    Path(f"docs/firm_watchlist_{a.label}.md").write_text("\n".join(md), encoding="utf-8")
    print(f"wrote docs/firm_watchlist_{a.label}.md and {csv_path}")


if __name__ == "__main__":
    main()
