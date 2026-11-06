"""
Month 3, step 8: a separate posting-level indicator of explicit sovereignty wording (no model, no channel tag).

Why it exists. The channel tags say what a job does. Sovereignty wording in a posting (a company paragraph about
"sovereign solutions", a mission to build a "sovereign cloud") can also be read as evidence that the employer and
its customers are trying to reduce dependence on foreign suppliers. That reading is an upper bound: the wording
may be marketing and says nothing about the role. It is therefore counted here, apart from the validated
channels, and reported beside them.

What it computes. For every month, and for a window before and after each event given with --event, the weighted
share of ALL postings that contain at least one term of a tier:

    boilerplate     generic company wording ("sovereign solutions", "sovereign capabilities")
    discourse       sovereignty as a policy aim ("digital sovereignty", "strategic autonomy")
    infrastructure  concrete sovereign technology ("sovereign cloud", "sovereign AI", "alternative to American")
    compliance      qualification names (SecNumCloud, EUCS, Gaia-X), mostly skill or compliance requirements
    any             at least one term of any tier

    share = sum of day weights of postings with the tier / sum of day weights of all postings

Weights and intervals are those of script 64 (day-stratified weights, exact duplicates removed, 95% bootstrap
intervals that redraw the postings of each day from the day's own mix; the population correction is ignored, so
intervals for small days are slightly wide, never narrow).

Text. Title plus the first 6,000 characters of the description, WITHOUT the boilerplate removal of the tagger:
the company paragraph is exactly where this wording sits.

Terms. lexicon/sovereignty_wording_terms.csv (columns as lexicon.csv; the `channel` column holds the tier).
The terms are literal; check the contexts file before you quote a share (a term can match a different meaning).

Run (project root, venv active), one run per board:
    python -m diagnostics.80_sovereignty_wording_indicator \
        --corpus data/raw/corpus_lesjeudis_com_2024-08_2025-04.jsonl data/raw/corpus_lesjeudis_com_2025-05_2025-09.jsonl \
        --label lesjeudis \
        --event InvestAI=2025-02-11

Options: --terms, --event NAME=YYYY-MM-DD (repeatable), --window-days (default 90), --boot (default 1000), --seed,
--contexts (snippets per term, default 3).
Writes docs/sovereignty_wording_<label>.md (contains posting snippets: keep it out of git) and
data/tagged/sovereignty_wording_<label>_monthly.csv.
"""

import argparse
import csv
import hashlib
import random
import re
import tempfile
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus
    from diagnostics.lexicon_io import read_lexicon, compile_lexicon, match_terms, context
except ImportError:
    from corpus_io import load_corpus
    from lexicon_io import read_lexicon, compile_lexicon, match_terms, context

TIERS = ["boilerplate", "discourse", "infrastructure", "compliance"]
COLS = TIERS + ["any"]


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
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--terms", default="lexicon/sovereignty_wording_terms.csv")
    ap.add_argument("--label", required=True)
    ap.add_argument("--event", action="append", default=[])
    ap.add_argument("--window-days", type=int, default=90)
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--contexts", type=int, default=3)
    a = ap.parse_args()

    rows_terms = read_lexicon(a.terms)
    bad = [r["term"] for r in rows_terms if r["channel"] not in TIERS]
    if bad:
        raise SystemExit(f"terms with an unknown tier (channel column): {bad}")
    compiled = compile_lexicon(rows_terms)
    tier_of = {r["term"]: r["channel"] for r in rows_terms}

    events = {}
    for e in a.event:
        name, _, d = e.partition("=")
        events[name] = date.fromisoformat(d)

    rows, dropped = load_all(a.corpus)
    print(f"{len(rows):,} postings after removing {dropped:,} exact duplicates")

    days = defaultdict(lambda: [0.0, 0, np.zeros(len(COLS))])
    term_n = defaultdict(int)
    conc = defaultdict(lambda: defaultdict(list))      # month -> tier -> list of context fingerprints (one per posting and tier)
    EMP_KEYS = ("company", "employer", "company_name", "organisation", "organization", "hiring_organization")
    emp_seen = False
    snippets = defaultdict(list)
    rng = random.Random(a.seed)
    for r in rows:
        txt = text_of(r["item"])
        hits = match_terms(compiled, txt)
        d = days[r["day"]]
        d[0] = r["w"]
        d[1] += 1
        tiers = {tier_of[h[0]["term"]] for h in hits}
        month = r["day"][:7]
        emp = next((str(r["item"][k]).strip().lower() for k in EMP_KEYS if r["item"].get(k)), None)
        emp_seen = emp_seen or emp is not None
        for t in tiers:
            first = next(h for h in hits if tier_of[h[0]["term"]] == t)
            ctx = re.sub(r"\W+", " ", context(txt, first[1], width=60).lower()).strip()
            fp = hashlib.md5(ctx.encode()).hexdigest()[:10]
            conc[month][t].append((fp, emp or fp))
        for i, t in enumerate(TIERS):
            if t in tiers:
                d[2][i] += 1
        if tiers:
            d[2][len(TIERS)] += 1
        for row, m in hits:
            term_n[row["term"]] += 1
            k = (row["term"])
            seen = term_n[row["term"]]
            snip = context(txt, m)
            if len(snippets[k]) < a.contexts:
                snippets[k].append(snip)
            else:                                   # reservoir sampling: every hit equally likely to be kept
                j = rng.randint(0, seen - 1)
                if j < a.contexts:
                    snippets[k][j] = snip

    keys = sorted(days)
    w = np.array([days[k][0] for k in keys])
    n = np.array([days[k][1] for k in keys])
    c = np.array([days[k][2] for k in keys])
    months = sorted({k[:7] for k in keys})
    groups = [("month " + m, {k for k in keys if k.startswith(m)}) for m in months]
    for name, ev in events.items():
        before = {(ev - timedelta(days=i)).isoformat() for i in range(1, a.window_days + 1)}
        after = {(ev + timedelta(days=i)).isoformat() for i in range(0, a.window_days)}
        groups += [(f"{name}: {a.window_days} days before", before), (f"{name}: {a.window_days} days from event", after)]
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
    csv_path = Path(f"data/tagged/sovereignty_wording_{a.label}_monthly.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["group", "postings_taken"] + [f"{t}_share" for t in COLS] + [f"{t}_lo" for t in COLS] + [f"{t}_hi" for t in COLS])
        for g, (name, members) in enumerate(groups):
            taken = int(sum(n[pos[k]] for k in members if k in pos))
            wr.writerow([name, taken] + [f"{x:.5f}" for x in obs[g]] + [f"{x:.5f}" for x in lo[g]] + [f"{x:.5f}" for x in hi[g]])

    md = [f"# Sovereignty wording indicator: {a.label}", "",
          "Share of all postings (day-weighted) that contain at least one term of the tier, with 95% bootstrap intervals. "
          "This is an upper bound on sovereignty-driven demand: the wording may be marketing and says nothing about the role. "
          "It is not a channel tag and is not mixed with the channel shares.", "",
          f"Postings read: {len(rows):,} (exact duplicates removed: {dropped:,}). Terms file: `{a.terms}`.", "",
          "| group | postings taken | " + " | ".join(COLS) + " |", "|---|---|" + "---|" * len(COLS)]
    for g, (name, members) in enumerate(groups):
        taken = int(sum(n[pos[k]] for k in members if k in pos))
        cells = [f"{100 * obs[g][i]:.2f}% ({100 * lo[g][i]:.2f} to {100 * hi[g][i]:.2f})" if not np.isnan(obs[g][i]) else "n/a"
                 for i in range(len(COLS))]
        md.append(f"| {name} | {taken} | " + " | ".join(cells) + " |")
    md += ["", "## Concentration (unweighted): how many different texts and employers sit behind each tier", "",
           "`postings / distinct contexts / share of the most frequent context`. A tier whose rise comes from one repeated paragraph "
           "(one employer's recruiting wave) shows many postings but few distinct contexts."
           + (" `distinct employers` is added because the corpus carries an employer field." if emp_seen else
              " The corpus carries no employer field, so the distinct context stands in for the employer."), "",
           "| month | " + " | ".join(TIERS) + " |", "|---|" + "---|" * len(TIERS)]
    conc_csv = []
    for m in months:
        cells = []
        for t in TIERS:
            L = conc[m][t]
            if not L:
                cells.append("0")
                conc_csv.append([m, t, 0, 0, 0, 0.0])
                continue
            fps = [x[0] for x in L]
            top = max(fps.count(f) for f in set(fps))
            emps = len({x[1] for x in L})
            cells.append(f"{len(L)} / {len(set(fps))} / {100 * top / len(L):.0f}%" + (f" / {emps} employers" if emp_seen else ""))
            conc_csv.append([m, t, len(L), len(set(fps)), emps, round(top / len(L), 3)])
        md.append(f"| {m} | " + " | ".join(cells) + " |")
    with open(Path(f"data/tagged/sovereignty_wording_{a.label}_concentration.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["month", "tier", "postings", "distinct_contexts", "distinct_employers_or_contexts", "top_context_share"])
        wr.writerows(conc_csv)
    md += ["", "## Postings (unweighted) per term, with contexts to check by eye", ""]
    for r in rows_terms:
        t = r["term"]
        md.append(f"### {t} ({r['channel']}): {term_n.get(t, 0)} postings")
        for s in snippets.get(t, []):
            md.append(f"- {s}")
        md.append("")
    doc_path = Path(f"docs/sovereignty_wording_{a.label}.md")
    doc_path.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {doc_path} and {csv_path}")


if __name__ == "__main__":
    main()
