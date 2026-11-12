"""
Month 4: how good are the inferred titles? (companion to script 99; offline, runs on the Mac)

Validation postings (titled, title hidden from the model):
  * share answered UNKNOWN
  * agreement with the real title: exact match after normalisation, and word overlap (F1 of the content words).
    The real titles are the cleaned titles of script 90 and often carry an employer or place ("nurse for kava sundsvall"), so word overlap
    is a LOWER bound: the judgement that counts is the manual one below.
  * by confidence level (high, medium, low)
Manual check: a random sample of --sheet-n pairs (real title, inferred title, start of the description is NOT shown) goes to
data/tagged/title_check_sheet_<label>.csv with an empty column `same_occupation` to fill with 1 (same occupation, even if worded
differently), 0.5 (related: same field, wrong level or specialisation) or 0. Run the script again with --sheet-in <filled file> to get the
agreement rate with a 95% interval (Wilson), overall and by confidence.
Inferred titles of the title-less postings: share UNKNOWN, confidence mix, the 40 most frequent titles.

Run (project root, venv active):
    python -m diagnostics.99b_score_title_inference --label jobbland
    python -m diagnostics.99b_score_title_inference --label jobbland --sheet-in data/tagged/title_check_sheet_jobbland_filled.csv

Output: docs/title_inference_<label>.md and data/tagged/title_check_sheet_<label>.csv
"""

import argparse
import csv
import json
import math
import random
import re
from collections import Counter
from pathlib import Path

STOP = {"a", "an", "the", "and", "or", "for", "of", "at", "to", "in", "with", "on", "m", "f", "d", "w", "job", "jobs"}


def words(t):
    ws = re.findall(r"[^\W\d_]+", (t or "").lower())
    return [w[:-1] if len(w) > 4 and w.endswith("s") else w for w in ws if w not in STOP]


def f1(a, b):
    A, B = set(words(a)), set(words(b))
    if not A or not B:
        return 0.0
    ov = len(A & B)
    if not ov:
        return 0.0
    p, r = ov / len(B), ov / len(A)
    return 2 * p * r / (p + r)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--label", required=True)
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--sheet-n", type=int, default=100)
    ap.add_argument("--sheet-in")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    inp = a.inp or f"data/tagged/inferred_titles_{a.label}.jsonl"
    recs = [json.loads(l) for l in open(inp, encoding="utf-8") if l.strip()]
    val = [r for r in recs if r["kind"] == "validation"]
    inf = [r for r in recs if r["kind"] == "inferred"]
    L = [f"# Inferred titles: {a.label}\n", f"{len(val):,} validation postings (title hidden), {len(inf):,} title-less postings.\n", "## Validation against the real title\n"]
    ans = [r for r in val if r["title_inferred"] != "UNKNOWN"]
    L.append(f"UNKNOWN: {len(val) - len(ans):,} of {len(val):,} ({(len(val) - len(ans)) / max(len(val), 1):.0%}).\n")
    if ans:
        ex = sum(" ".join(words(r["title_inferred"])) == " ".join(words(r["true_title"])) for r in ans)
        sc = [f1(r["true_title"], r["title_inferred"]) for r in ans]
        L.append(f"Of the {len(ans):,} answered: exact match after normalisation {ex / len(ans):.0%}; mean word overlap (F1) {sum(sc) / len(sc):.2f}; "
                 f"overlap of at least 0.5 in {sum(s >= 0.5 for s in sc) / len(sc):.0%}; no common word in {sum(s == 0 for s in sc) / len(sc):.0%}. A lower bound: see the manual check.\n")
        L.append("| confidence | answered | overlap F1 >= 0.5 | mean F1 |")
        L.append("|---|---|---|---|")
        for c in ("high", "medium", "low"):
            sub = [(r, f1(r["true_title"], r["title_inferred"])) for r in ans if r["confidence"] == c]
            if sub:
                L.append(f"| {c} | {len(sub)} | {sum(s >= 0.5 for _, s in sub) / len(sub):.0%} | {sum(s for _, s in sub) / len(sub):.2f} |")
        L.append("")
    sheet_p = f"data/tagged/title_check_sheet_{a.label}.csv"
    if ans and not a.sheet_in:
        rnd = random.Random(a.seed)
        pick = rnd.sample(ans, min(a.sheet_n, len(ans)))
        with open(sheet_p, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["id", "confidence", "true_title", "inferred_title", "same_occupation"])
            for r in pick:
                w.writerow([r["id"], r["confidence"], r["true_title"], r["title_inferred"], ""])
        L.append(f"Manual check sheet with {len(pick)} pairs written to `{sheet_p}`. Fill `same_occupation` (1, 0.5, 0) and rerun with `--sheet-in`.\n")
    if a.sheet_in:
        rows = list(csv.DictReader(open(a.sheet_in, encoding="utf-8-sig")))
        vals = [(r["confidence"], float(str(r["same_occupation"]).replace(",", "."))) for r in rows if str(r["same_occupation"]).strip() != ""]
        if vals:
            k = sum(v for _, v in vals)
            lo, hi = wilson(k, len(vals))
            full = sum(v == 1 for _, v in vals)
            L.append("## Manual check\n")
            L.append(f"{len(vals)} pairs judged. Same occupation (1) in {full / len(vals):.0%}; counting related (0.5) as half: {k / len(vals):.0%} "
                     f"(95% interval {lo:.0%} to {hi:.0%}, Wilson, treating 0.5 as half a success).\n")
            L.append("| confidence | pairs | score (1 = same, 0.5 = related) |")
            L.append("|---|---|---|")
            for c in ("high", "medium", "low"):
                sub = [v for cc, v in vals if cc == c]
                if sub:
                    L.append(f"| {c} | {len(sub)} | {sum(sub) / len(sub):.0%} |")
            L.append("")
    L.append("## Inferred titles of the title-less postings\n")
    if inf:
        unk = sum(r["title_inferred"] == "UNKNOWN" for r in inf)
        cc = Counter(r["confidence"] for r in inf if r["title_inferred"] != "UNKNOWN")
        L.append(f"UNKNOWN: {unk:,} of {len(inf):,} ({unk / len(inf):.0%}). Confidence of the answered: " + ", ".join(f"{k} {v}" for k, v in cc.most_common()) + ".\n")
        top = Counter(" ".join(words(r["title_inferred"])) for r in inf if r["title_inferred"] != "UNKNOWN").most_common(40)
        L.append("Most frequent inferred titles (normalised): " + "; ".join(f"{t} ({n})" for t, n in top) + ".\n")
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/title_inference_{a.label}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"docs/title_inference_{a.label}.md written")


if __name__ == "__main__":
    main()
