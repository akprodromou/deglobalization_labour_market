"""
Month 3, step 8: ESCOX at three thresholds, run locally on a small sample (the diagnostic the supervisor approved).

Question (Skillab team, 16 Oct 2026): the Tracker extracts ESCO skills with a similarity threshold of 0.5 and its
tags stop in October 2025 for jobbland.se. Is the outage a threshold effect, i.e. do postings after the outage
yield skills locally when the threshold is lowered (down to 0.45, the floor the tool's author allows)?

For each sampled month the script takes up to --n postings at random (fixed seed; unweighted, because the aim is
to compare extraction, not to estimate a population share), runs the open-source esco-skill-extractor
(github.com/KonstantinosPetrakis/esco-skill-extractor) at each threshold and reports:

  * share of postings with at least one skill, and mean number of skills per posting, per threshold
  * the Tracker's own tags in the same sample (share with at least one skill, mean number), for comparison
  * where both exist (months before the outage): overlap of the Tracker's skills with the local skills
    (share of the Tracker's skills the local run also finds, per threshold)

Reading the result. If the outage months give (almost) no skills at 0.5 and 0.45 while the tagged months give
many, the outage is not only a threshold effect and one local threshold cannot repair it. If they give skills at
0.45 at a rate close to the tagged months, one local threshold applied to all months, tagged and untagged, becomes
an option (Tracker tags at 0.5 must never be mixed with local tags at a lower threshold: the local run replaces
the Tracker tags in every month it is used for). Skills are not sectors: this probe says nothing about sectors.

Needs: pip install esco-skill-extractor (it downloads a sentence-transformer model on first use; the default
is the English all-MiniLM-L6-v2). Not run on the real package by the author of this script: the call used is
SkillExtractor(skill_threshold=...).get_skills(list_of_texts), which returns one list of ESCO URIs per text,
as the repository's README describes. Test the pipeline without the package with --mock.

Run (project root, venv active; same corpus files as script 64):
    python -m diagnostics.68_escox_threshold_probe \\
        --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl \\
                 data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl
Options: --months 2024-03 2025-03 2025-09 2025-11 2026-03 2026-08   --n 100   --thresholds 0.6 0.5 0.45
Writes docs/escox_threshold_probe.md and data/tagged/escox_threshold_probe.csv (skills per sampled posting).
"""

import argparse
import csv
import random
import tempfile
from collections import defaultdict
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus, posting_text
except ImportError:
    from corpus_io import load_corpus, posting_text

MAX_CHARS = 3000
DEFAULT_MONTHS = ["2024-03", "2025-03", "2025-09", "2025-11", "2026-03", "2026-08"]


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


def tracker_skills(item):
    """Set of identifiers of the Tracker's skill tags (uri/id when present, else lower-cased label)."""
    out = set()
    for s in item.get("skills") or []:
        if isinstance(s, dict):
            v = s.get("uri") or s.get("esco_uri") or s.get("id") or s.get("label") or s.get("name")
        else:
            v = s
        if v:
            out.add(str(v).strip().lower())
    return out


def local_ids(uris):
    return {str(u).strip().lower() for u in uris}


def mock_extractor(threshold):
    """Deterministic fake for pipeline tests: lower thresholds return more 'skills'."""
    class M:
        def get_skills(self, texts):
            out = []
            for t in texts:
                words = sorted({w for w in t.lower().split() if len(w) > 6})
                k = int(len(words) * (1.2 - threshold))
                out.append([f"mock/{w}" for w in words[:k]])
            return out
    return M()


def real_extractor(threshold):
    from esco_skill_extractor import SkillExtractor
    return SkillExtractor(skill_threshold=threshold)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--months", nargs="+", default=DEFAULT_MONTHS)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--thresholds", nargs="+", type=float, default=[0.6, 0.5, 0.45])
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--out-md", default="docs/escox_threshold_probe.md")
    ap.add_argument("--out-csv", default="data/tagged/escox_threshold_probe.csv")
    args = ap.parse_args()

    rows, dup = load_all(args.corpus)
    by_month = defaultdict(list)
    for r in rows:
        by_month[r["day"][:7]].append(r)
    rng = random.Random(args.seed)
    sample = []
    for m in args.months:
        pool = by_month.get(m, [])
        sample += [(m, r) for r in rng.sample(pool, min(args.n, len(pool)))]
    print(f"{len(rows):,} postings; sample {len(sample):,} in {len(args.months)} months")

    texts = [posting_text(r["item"], MAX_CHARS) for _, r in sample]
    local = {}
    for th in args.thresholds:
        ex = mock_extractor(th) if args.mock else real_extractor(th)
        local[th] = [local_ids(u) for u in ex.get_skills(texts)]
        print(f"threshold {th}: done")

    trk = [tracker_skills(r["item"]) for _, r in sample]
    idx = defaultdict(list)
    for i, (m, _) in enumerate(sample):
        idx[m].append(i)

    hdr = ["Month", "Postings sampled", "Tracker: with skills (%)", "Tracker: mean skills"]
    for th in args.thresholds:
        hdr += [f"{th}: with skills (%)", f"{th}: mean skills"]
    for th in args.thresholds:
        hdr += [f"{th}: Tracker skills also found (%)"]
    L = ["# ESCOX at three thresholds: do the outage months yield skills?", "",
         f"Random sample of up to {args.n} postings per month (unweighted), text = title and the first {MAX_CHARS} characters "
         f"of the description (boilerplate removed). Local = esco-skill-extractor, skill threshold as shown"
         + (" (MOCK extractor: the numbers are not real)" if args.mock else "") + ". "
         "'Tracker skills also found' is computed only on postings where the Tracker has skills.", "",
         "| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
    out = []
    for m in args.months:
        ii = idx.get(m, [])
        if not ii:
            L.append(f"| {m} | 0 |" + " |" * (len(hdr) - 2))
            continue
        n = len(ii)
        cells = [m, str(n), f"{100*sum(1 for i in ii if trk[i])/n:.0f}", f"{sum(len(trk[i]) for i in ii)/n:.1f}"]
        for th in args.thresholds:
            cells += [f"{100*sum(1 for i in ii if local[th][i])/n:.0f}", f"{sum(len(local[th][i]) for i in ii)/n:.1f}"]
        for th in args.thresholds:
            both = [i for i in ii if trk[i]]
            if both:
                tot = sum(len(trk[i]) for i in both)
                hit = sum(len(trk[i] & local[th][i]) for i in both)
                cells.append(f"{100*hit/tot:.0f}" if tot else "-")
            else:
                cells.append("-")
        L.append("| " + " | ".join(cells) + " |")
    L += ["", "A month with fewer than about 30 postings sampled cannot carry a comparison. "
          "Overlap is low by construction if the Tracker's identifiers are not URIs (labels vs URIs); check a few rows of the csv before reading it."]
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text("\n".join(L), encoding="utf-8")
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["month", "day", "posting_id", "title", "n_tracker"] + [f"n_local_{th}" for th in args.thresholds] + ["tracker_skills", f"local_skills_{args.thresholds[-1]}"])
        for i, (m, r) in enumerate(sample):
            it = r["item"]
            wr.writerow([m, r["day"], it.get("id"), str(it.get("title", ""))[:80], len(trk[i])] +
                        [len(local[th][i]) for th in args.thresholds] +
                        ["; ".join(sorted(trk[i]))[:300], "; ".join(sorted(local[args.thresholds[-1]][i]))[:300]])
    print(f"Wrote {args.out_md} and {args.out_csv}")


if __name__ == "__main__":
    main()
