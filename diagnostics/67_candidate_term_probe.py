"""
Month 3, step 7: how many postings would new lexicon terms add, and what do they say?

Reads a CSV of candidate terms (same columns as lexicon.csv), matches each term in the downloaded corpus
(title and first 6,000 characters, boilerplate removed, as the tagger does) and reports, per term:

  * postings taken that contain it, and how many of these the CURRENT lexicon did not flag (the "new" ones)
  * weighted share of all postings, in five periods: all months, January to April 2024, September to
    December 2024, December 2024, December 2025 (the periods the event comparisons use)
  * three short contexts, drawn at random, to judge by eye whether the term is about the channel

Use it before a term enters the lexicon: a term with a handful of postings adds no power, and a term whose
contexts are mostly irrelevant (a single metal in a cable, "solar" in door-to-door sales) lowers the lexicon's
precision. The model tagger then labels such postings none, so the cost is tagging time and noise in the
lexicon-only series, not wrong tags.

Run (project root, venv active):
    python -m diagnostics.67_candidate_term_probe \\
        --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl \\
                 data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl \\
        --terms lexicon/lexicon_additions_approved.csv lexicon/lexicon_candidates_critical_materials.csv \\
        --flagged data/tagged/flagged_corpus_jobbland.se_2024-01_2026-09.jsonl
Writes docs/candidate_term_probe.md (contexts are snippets of postings: keep the file out of git) and
data/tagged/candidate_term_probe.csv.
"""

import argparse
import csv
import json
import random
import re
import tempfile
from collections import defaultdict
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus, posting_text
    from diagnostics.lexicon_io import read_lexicon, compile_lexicon, match_terms, context
except ImportError:
    from corpus_io import load_corpus, posting_text
    from lexicon_io import read_lexicon, compile_lexicon, match_terms, context

SEARCH_CHARS = 6000
PERIODS = {
    "all": lambda d: True,
    "Jan-Apr 2024": lambda d: "2024-01-01" <= d <= "2024-04-30",
    "Sep-Dec 2024": lambda d: "2024-09-01" <= d <= "2024-12-31",
    "Dec 2024": lambda d: d[:7] == "2024-12",
    "Dec 2025": lambda d: d[:7] == "2025-12",
}


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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--terms", nargs="+", required=True)
    ap.add_argument("--flagged", required=True)
    ap.add_argument("--contexts", type=int, default=3)
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--out-md", default="docs/candidate_term_probe.md")
    ap.add_argument("--out-csv", default="data/tagged/candidate_term_probe.csv")
    args = ap.parse_args()

    rows, dup = load_all(args.corpus)
    flagged = {json.loads(l)["posting_id"] for l in open(args.flagged, encoding="utf-8") if l.strip()}
    cand = []
    for p in args.terms:
        cand += read_lexicon(p)
    lex = compile_lexicon(cand)
    print(f"{len(rows):,} postings ({dup:,} duplicates removed); {len(cand)} candidate terms")

    pop = {k: sum(r["w"] for r in rows if f(r["day"])) for k, f in PERIODS.items()}
    hits = defaultdict(list)      # term -> [(row, matched string, text)]
    for r in rows:
        text = posting_text(r["item"], SEARCH_CHARS)
        for entry, m in match_terms(lex, text):
            hits[entry["term"]].append((r, m, text))

    rng = random.Random(args.seed)
    out = []
    L = ["# Candidate lexicon terms: counts and contexts", "",
         f"{len(rows):,} postings after removing {dup:,} duplicates. Share = weighted share of all postings in the period (%). "
         "'New' = postings the current lexicon did not flag. Contexts are random snippets: read them, then decide.", "",
         "| Term | Channel | Taken | New | All | Jan-Apr 2024 | Sep-Dec 2024 | Dec 2024 | Dec 2025 | Note |", "|---|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    detail = []
    for c in cand:
        h = hits.get(c["term"], [])
        new = sum(1 for r, _, _ in h if str(r["item"]["id"]) not in flagged)
        shares = {k: (100 * sum(r["w"] for r, _, _ in h if f(r["day"])) / pop[k] if pop[k] else float("nan")) for k, f in PERIODS.items()}
        taken_p = {k: sum(1 for r, _, _ in h if f(r["day"])) for k, f in PERIODS.items()}
        L.append(f"| {c['term']} | {c['channel']} | {len(h)} | {new} | {shares['all']:.3f} | {shares['Jan-Apr 2024']:.3f} ({taken_p['Jan-Apr 2024']}) | "
                 f"{shares['Sep-Dec 2024']:.3f} ({taken_p['Sep-Dec 2024']}) | {shares['Dec 2024']:.3f} ({taken_p['Dec 2024']}) | "
                 f"{shares['Dec 2025']:.3f} ({taken_p['Dec 2025']}) | {c.get('note', '')} |")
        out.append([c["term"], c["channel"], len(h), new] + [round(shares[k], 4) for k in PERIODS] + [taken_p[k] for k in PERIODS])
        sample = rng.sample(h, min(args.contexts, len(h)))
        detail.append(f"### {c['term']} ({c['channel']}): {len(h)} postings taken, {new} new")
        for r, m, text in sample:
            snip = re.sub(r"\s+", " ", context(text, m, 110))
            detail.append(f"- {r['day']} | {str(r['item'].get('title', ''))[:70]} | ...{snip}...")
        detail.append("")
    L += ["", "Brackets: postings taken in the period. A cell with fewer than about 10 postings taken cannot carry a comparison.", ""] + detail
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text("\n".join(L), encoding="utf-8")
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["term", "channel", "taken", "new"] + [f"share_{k}" for k in PERIODS] + [f"taken_{k}" for k in PERIODS])
        wr.writerows(out)
    print(f"Wrote {args.out_md} and {args.out_csv}")


if __name__ == "__main__":
    main()
