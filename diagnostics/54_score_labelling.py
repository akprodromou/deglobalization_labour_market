"""
Month 3: score the hand labels (and, later, a classifier) against the sample.

Reads the filled sheet (data/labelling/validation_sheet.csv), the hidden key
(validation_key.jsonl, written by script 53) and, optionally, a file of
predictions. For each label (`manufacturing`, `metals`) it reports:

  * how many postings were labelled yes / no / unclear, and the weighted
    share of unclear (a posting the text does not let you decide);
  * the weighted prevalence of the label among decidable postings;
  * for the predictor: precision, recall and F1 with 95% bootstrap
    intervals, resampling inside each stratum, and the decision against the
    thresholds fixed in docs/labelling_protocol.md.

Weights. The key holds one weight per sampled posting (day weight times
stratum size over stratum draw, see script 53), so the sample is weighted back
to the population of distinct 2026 postings in the source. Unclear labels are
left out of precision, recall and prevalence and reported separately.

Predictor. Without --predictions the predictor is the keyword screen of
script 53 (a baseline, not the classifier): `manufacturing` = any
manufacturing or metals word, `metals` = a metals word. With --predictions the
file must be JSON lines with `posting_id`, `manufacturing` (0/1) and `metals`
(0/1). Use it to score the classifier on exactly the same labelled sample.

Consistency (pass 2). With --pass2 the script also compares your two labelling
passes on the postings they share (percent agreement and Cohen's kappa).

Offline; no credentials.

Run (project root, venv active):
    python -m diagnostics.54_score_labelling
    python -m diagnostics.54_score_labelling --pass2 data/labelling/validation_sheet_pass2.csv
    python -m diagnostics.54_score_labelling --predictions data/labelling/classifier_predictions.jsonl

Output: docs/labelling_results.md
"""

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

LAB_DIR = Path("data/labelling")
SEED = 20261018
BOOT = 2000
# Fixed in docs/labelling_protocol.md before any label was made.
PRECISION_MIN = 0.80
RECALL_MIN = 0.70
LABELS = ["manufacturing", "metals"]


def parse(v):
    v = (v or "").strip().lower()
    if not v:
        return "missing"
    if v[0] == "y" or v == "1":
        return 1
    if v[0] == "n" or v == "0":
        return 0
    return None   # unclear / can't tell / ?


def read_sheet(path):
    out = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            out[r["posting_id"]] = {lab: parse(r.get(lab)) for lab in LABELS}
    return out


def pct(v, q):
    v = sorted(x for x in v if x == x)
    if not v:
        return float("nan")
    k = (len(v) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def stats(items):
    """items: list of (weight, truth, pred). Returns precision, recall, f1."""
    tp = sum(w for w, t, p in items if t and p)
    pp = sum(w for w, t, p in items if p)
    tt = sum(w for w, t, p in items if t)
    prec = tp / pp if pp else float("nan")
    rec = tp / tt if tt else float("nan")
    f1 = 2 * prec * rec / (prec + rec) if prec == prec and rec == rec and prec + rec else float("nan")
    return prec, rec, f1


def boot(items_by_stratum, rng):
    res = {"prec": [], "rec": [], "f1": [], "prev": []}
    for _ in range(BOOT):
        sample = []
        for s, items in items_by_stratum.items():
            sample += [items[rng.randrange(len(items))] for _ in items]
        p, r, f = stats(sample)
        res["prec"].append(p)
        res["rec"].append(r)
        res["f1"].append(f)
        sw = sum(w for w, t, _ in sample)
        res["prev"].append(sum(w for w, t, _ in sample if t) / sw if sw else float("nan"))
    return {k: (pct(v, 0.025), pct(v, 0.975)) for k, v in res.items()}


def kappa(a, b):
    n = len(a)
    if not n:
        return float("nan")
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--sheet", default=str(LAB_DIR / "validation_sheet.csv"))
    ap.add_argument("--key", default=str(LAB_DIR / "validation_key.jsonl"))
    ap.add_argument("--predictions", default=None)
    ap.add_argument("--pass2", default=None)
    args = ap.parse_args()

    sheet = read_sheet(args.sheet)
    keys = {}
    for line in open(args.key, encoding="utf-8"):
        if line.strip():
            k = json.loads(line)
            keys[str(k["posting_id"])] = k
    pred = None
    if args.predictions:
        pred = {}
        for line in open(args.predictions, encoding="utf-8"):
            if line.strip():
                r = json.loads(line)
                pred[str(r["posting_id"])] = r
    predictor = "classifier predictions" if pred is not None else "keyword screen of script 53 (baseline)"

    out = ["# Validation of the labels and of the predictor\n",
           f"Predictor scored: {predictor}. Sample: {len(keys)} postings drawn in three strata "
           "(1 metals words, 2 manufacturing words only, 3 neither); weights bring the sample "
           "back to the population of distinct 2026 postings in the source. Intervals are 95% "
           f"bootstrap intervals resampling inside each stratum ({BOOT} draws). "
           f"Thresholds for accepting the manufacturing flag, fixed before labelling: precision "
           f">= {PRECISION_MIN:.2f} and recall >= {RECALL_MIN:.2f}.\n"]

    for lab in LABELS:
        rows = []   # weight, stratum, truth, pred
        counts = Counter()
        unclear_w = tot_w = 0.0
        for pid, k in keys.items():
            truth = sheet.get(pid, {}).get(lab, "missing")
            w = k["weight"]
            if truth == "missing":
                counts["missing"] += 1
                continue
            tot_w += w
            if truth is None:
                counts["unclear"] += 1
                unclear_w += w
                continue
            counts["yes" if truth else "no"] += 1
            if pred is not None:
                p = int(pred.get(pid, {}).get(lab, 0))
            else:
                p = int(k["screen_metals"] if lab == "metals" else k["screen_manufacturing"])
            rows.append((w, k["stratum"], truth, p))
        out.append(f"## Label: {lab}\n")
        out.append(f"Labelled yes {counts['yes']}, no {counts['no']}, unclear {counts['unclear']}, "
                   f"not yet labelled {counts['missing']}. Weighted share of unclear among labelled: "
                   f"{(unclear_w / tot_w if tot_w else float('nan')):.1%}.\n")
        if not rows:
            out.append("No decidable labels yet.\n")
            continue
        by_s = defaultdict(list)
        for w, s, t, p in rows:
            by_s[s].append((w, t, p))
        rng = random.Random(SEED)
        ci = boot(by_s, rng)
        allitems = [(w, t, p) for w, s, t, p in rows]
        prec, rec, f1 = stats(allitems)
        prev = sum(w for w, t, p in allitems if t) / sum(w for w, t, p in allitems)
        out.append("| Quantity | Estimate | 95% interval |\n|---|---:|---:|")
        out.append(f"| Prevalence among decidable postings | {prev:.1%} | {ci['prev'][0]:.1%} to {ci['prev'][1]:.1%} |")
        out.append(f"| Precision | {prec:.2f} | {ci['prec'][0]:.2f} to {ci['prec'][1]:.2f} |")
        out.append(f"| Recall | {rec:.2f} | {ci['rec'][0]:.2f} to {ci['rec'][1]:.2f} |")
        out.append(f"| F1 | {f1:.2f} | {ci['f1'][0]:.2f} to {ci['f1'][1]:.2f} |")
        out.append("")
        out.append("Yes / no labels per stratum: " + "; ".join(
            f"stratum {s}: {sum(1 for _, t, _ in v if t)} yes, {sum(1 for _, t, _ in v if not t)} no"
            for s, v in sorted(by_s.items())) + ".\n")
        if lab == "manufacturing":
            ok_p, ok_r = prec >= PRECISION_MIN, rec >= RECALL_MIN
            border = (ci["prec"][0] < PRECISION_MIN <= prec) or (ci["rec"][0] < RECALL_MIN <= rec)
            verdict = ("**Accepted**" if ok_p and ok_r and not border else
                       "**Borderline: the point estimates meet the thresholds but the lower end of an interval does not**" if ok_p and ok_r else
                       "**Not accepted**")
            out.append(f"Decision for the manufacturing flag: {verdict} (precision {prec:.2f} "
                       f"against {PRECISION_MIN:.2f}, recall {rec:.2f} against {RECALL_MIN:.2f}).\n")
        else:
            out.append("The metals label is descriptive only: the group is too small to pass the "
                       "volume rule (docs/sector_month_counts_steel.md), so no acceptance rule applies.\n")

    if args.pass2:
        p2 = read_sheet(args.pass2)
        out.append("## Consistency between the two labelling passes\n")
        for lab in LABELS:
            pairs = [(sheet[i][lab], p2[i][lab]) for i in p2 if i in sheet
                     and sheet[i][lab] != "missing" and p2[i][lab] != "missing"]
            a = ["unclear" if x is None else x for x, _ in pairs]
            b = ["unclear" if y is None else y for _, y in pairs]
            agree = sum(1 for x, y in zip(a, b) if x == y) / len(a) if a else float("nan")
            out.append(f"- `{lab}`: {len(a)} postings in both passes, agreement {agree:.0%}, "
                       f"Cohen's kappa {kappa(a, b):.2f}.")
        out.append("\nA kappa below about 0.6 means the rules in the protocol are too vague: "
                   "tighten them and label again before using the results.\n")

    path = Path("docs/labelling_results.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
