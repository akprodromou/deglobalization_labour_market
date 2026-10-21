"""
Month 3, step 3c: score the LLM tags against the hand annotation.

Reads the annotated sheet (data/tagging/annotation_sheet.csv), the hidden key
(strata and weights) and one or more tags files (--tags, repeat the option to
compare models on the same sample). Writes docs/tagging_results.md.

What is reported, for each model (no pass/fail threshold: the numbers are
reported with intervals and the models are compared, as in the paper the brief
cites, Kavargyris et al. 2025):

  * Channel, one-vs-rest per channel: precision, recall and F1, and the macro
    average over the channels that occur in the annotation. Precision of a
    channel = weighted share of the postings the model put in it that the
    annotator put in it; recall = weighted share of the annotator's postings
    of that channel that the model found.
  * "Any channel against none": does the posting relate to deglobalisation at all.
  * Lexicon precision: weighted share of flagged postings the annotator calls
    `none` (the lexicon matched a word, the work is about something else).
  * Intensity: among postings where model and annotator agree on a channel
    other than none, exact agreement and quadratic-weighted kappa
    (low < medium < high), with the confusion table.
  * Lexicon recall, if the sheet had unflagged postings (--unflagged in script 59):
    the weighted share of unflagged postings that the annotator calls relevant.
  * If a pass-2 sheet exists: your own consistency (Cohen's kappa for channel,
    weighted kappa for intensity) between pass 1 and pass 2.

Weights. Every annotated posting carries its sampling weight (script 59).
95% intervals are percentile bootstrap intervals that resample postings inside
each stratum (2,000 draws, fixed seed). `unclear` annotations are left out and
their share is reported. Postings the model could not tag (invalid answer) are
scored as a wrong prediction.

Run (project root):
    python -m diagnostics.60_score_tagging --tags data/tagged/tags_qwen2.5_7b_tagging_v1.jsonl \\
                                           --tags data/tagged/tags_mistral_tagging_v1.jsonl
"""

import argparse
import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

CHANNELS = ["reshoring", "defense", "critical materials", "energy security",
            "trade compliance", "diversification"]
LEVEL = {"low": 1, "medium": 2, "high": 3}
SHEET = Path("data/tagging/annotation_sheet.csv")
KEY = Path("data/tagging/annotation_key.jsonl")
PASS2 = Path("data/tagging/annotation_sheet_pass2.csv")
OUT = Path("docs/tagging_results.md")
SEED = 20261021
DRAWS = 2000


def norm_label(v):
    return (v or "").strip().lower().replace("defence", "defense")


def read_sheet(path):
    out = {}
    for r in csv.DictReader(open(path, encoding="utf-8-sig", newline="")):
        out[str(r["posting_id"])] = (norm_label(r["channel"]), norm_label(r["intensity"]))
    return out


def pct(v, q):
    v = sorted(v)
    return v[min(len(v) - 1, max(0, int(round(q * (len(v) - 1)))))]


def fmt(x):
    return "n/a" if x is None else f"{x:.2f}"


def ci(vals):
    vals = [v for v in vals if v is not None]
    if len(vals) < DRAWS * 0.5:
        return "n/a"
    return f"{pct(vals, .025):.2f} to {pct(vals, .975):.2f}"


def prf(items, cls):
    """Weighted precision, recall, F1 of class `cls` (one against rest)."""
    tp = sum(w for w, t, p in items if t == cls and p == cls)
    fp = sum(w for w, t, p in items if t != cls and p == cls)
    fn = sum(w for w, t, p in items if t == cls and p != cls)
    pr = tp / (tp + fp) if tp + fp else None
    rc = tp / (tp + fn) if tp + fn else None
    if rc is None:                      # the annotator found no posting of this channel
        f1 = None
    elif tp == 0:                       # postings exist but none was found: F1 is 0
        f1 = 0.0
    else:
        f1 = 2 * pr * rc / (pr + rc)
    return pr, rc, f1


def binary_prf(items):
    tp = sum(w for w, t, p in items if t != "none" and p != "none")
    fp = sum(w for w, t, p in items if t == "none" and p != "none")
    fn = sum(w for w, t, p in items if t != "none" and p == "none")
    pr = tp / (tp + fp) if tp + fp else None
    rc = tp / (tp + fn) if tp + fn else None
    f1 = 2 * pr * rc / (pr + rc) if pr and rc else None
    return pr, rc, f1


def wkappa(pairs, weights=None):
    """Quadratic-weighted kappa for ordinal levels 1..3, optional sample weights."""
    ks = [1, 2, 3]
    w = weights or [1.0] * len(pairs)
    tot = sum(w)
    if not tot:
        return None
    O = {(a, b): 0.0 for a in ks for b in ks}
    for (a, b), x in zip(pairs, w):
        O[(a, b)] += x / tot
    ra = {a: sum(O[(a, b)] for b in ks) for a in ks}
    rb = {b: sum(O[(a, b)] for a in ks) for b in ks}
    num = sum(((a - b) ** 2) * O[(a, b)] for a in ks for b in ks)
    den = sum(((a - b) ** 2) * ra[a] * rb[b] for a in ks for b in ks)
    return 1 - num / den if den else None


def ckappa(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else None


def build(sheet, key, tags):
    """Items: (stratum, weight, true channel, true intensity, predicted channel, predicted intensity)."""
    items, unclear, total = [], 0.0, 0.0
    for k in key:
        pid = k["posting_id"]
        if pid not in sheet:
            continue
        t_ch, t_in = sheet[pid]
        if k.get("flagged", True):
            total += k["weight"]
        if t_ch in ("", "unclear"):
            if t_ch == "unclear" and k.get("flagged", True):
                unclear += k["weight"]
            continue
        r = tags.get(pid)
        if r is None:
            p_ch, p_in = "none", ""
        elif r["ok"]:
            p_ch, p_in = r["channel"], r["intensity"]
        else:
            p_ch, p_in = "invalid", ""
        items.append((k["stratum"], k["weight"], t_ch, t_in, p_ch, p_in, k.get("flagged", True)))
    return items, unclear, total


def stats(items):
    fl = [(w, t, p) for s, w, t, ti, p, pi, f in items if f]
    res = {}
    for c in CHANNELS:
        res[c] = prf(fl, c)
    f1s = [res[c][2] for c in CHANNELS if res[c][2] is not None and any(t == c for _, t, _ in fl)]
    res["macro_f1"] = sum(f1s) / len(f1s) if f1s else None
    res["any"] = binary_prf(fl)
    tw = sum(w for w, _, _ in fl)
    res["lex_prec"] = 1 - sum(w for w, t, _ in fl if t == "none") / tw if tw else None
    agree = [(w, LEVEL.get(ti), LEVEL.get(pi)) for s, w, t, ti, p, pi, f in items
             if f and t == p and t not in ("none", "invalid") and LEVEL.get(ti) and LEVEL.get(pi)]
    sw = sum(w for w, _, _ in agree)
    res["int_agree"] = sum(w for w, a, b in agree if a == b) / sw if sw else None
    res["int_kappa"] = wkappa([(a, b) for _, a, b in agree], [w for w, _, _ in agree]) if agree else None
    unf = [(w, t) for s, w, t, ti, p, pi, f in items if not f]
    uw = sum(w for w, _ in unf)
    res["lex_miss"] = sum(w for w, t in unf if t != "none") / uw if uw else None
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--sheet", default=str(SHEET))
    ap.add_argument("--key", default=str(KEY))
    ap.add_argument("--tags", action="append", required=True)
    ap.add_argument("--pass2", default=str(PASS2))
    args = ap.parse_args()

    sheet = read_sheet(Path(args.sheet))
    key = [json.loads(l) for l in open(args.key, encoding="utf-8") if l.strip()]
    lines = ["# Tagging evaluation", "",
             "Sample: postings drawn in strata by one model's predicted channel, equal numbers per stratum, "
             "weighted back to the population of lexicon-flagged postings (script 59). Intervals are 95% "
             "bootstrap intervals resampling inside each stratum. No acceptance threshold is applied: "
             "models are compared on the same sample.", ""]
    summary = []
    for tpath in args.tags:
        tags = {}
        for l in open(tpath, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                tags[r["posting_id"]] = r
        items, unclear, total = build(sheet, key, tags)
        n_ann = sum(1 for k in key if sheet.get(k["posting_id"], ("", ""))[0] != "")
        base = stats(items)
        rng = random.Random(SEED)
        by_s = defaultdict(list)
        for it in items:
            by_s[it[0]].append(it)
        boots = []
        for _ in range(DRAWS):
            samp = []
            for s, v in by_s.items():
                scale = len(v)
                draw = [rng.choice(v) for _ in v]
                samp += draw
            boots.append(stats(samp))
        name = Path(tpath).stem
        invalid = sum(1 for k in key if k["posting_id"] in tags and not tags[k["posting_id"]]["ok"])
        lines += [f"## {name}", "",
                  f"Annotated {n_ann} of {len(key)} sheet rows; `unclear`: {unclear / total:.1%} of the weighted "
                  f"flagged sample (left out); invalid model answers in the sample: {invalid}.", "",
                  "| Channel | Precision | 95% interval | Recall | 95% interval | F1 | 95% interval |",
                  "|---|---:|---|---:|---|---:|---|"]
        for c in CHANNELS:
            pr, rc, f1 = base[c]
            n_true = sum(1 for it in items if it[2] == c and it[6])
            lines.append(f"| {c} (n={n_true}) | {fmt(pr)} | {ci([b[c][0] for b in boots])} | {fmt(rc)} | "
                         f"{ci([b[c][1] for b in boots])} | {fmt(f1)} | {ci([b[c][2] for b in boots])} |")
        pr, rc, f1 = base["any"]
        lines.append(f"| **any channel vs none** | {fmt(pr)} | {ci([b['any'][0] for b in boots])} | {fmt(rc)} | "
                     f"{ci([b['any'][1] for b in boots])} | {fmt(f1)} | {ci([b['any'][2] for b in boots])} |")
        lines += ["", f"Macro-F1 over the channels present in the annotation: **{fmt(base['macro_f1'])}** "
                      f"({ci([b['macro_f1'] for b in boots])}).", "",
                  f"Lexicon precision (flagged postings that are about a channel at all): "
                  f"{fmt(base['lex_prec'])} ({ci([b['lex_prec'] for b in boots])}).", ""]
        if base["int_kappa"] is not None or base["int_agree"] is not None:
            lines += [f"Intensity, where model and annotator agree on the channel: exact agreement "
                      f"{fmt(base['int_agree'])} ({ci([b['int_agree'] for b in boots])}); quadratic-weighted "
                      f"kappa {fmt(base['int_kappa'])} ({ci([b['int_kappa'] for b in boots])}).", ""]
            conf = Counter((ti, pi) for s, w, t, ti, p, pi, f in items
                           if f and t == p and t not in ("none", "invalid") and LEVEL.get(ti) and LEVEL.get(pi))
            lines += ["| Annotator \\ model (unweighted counts) | low | medium | high |", "|---|---:|---:|---:|"]
            for a in ("low", "medium", "high"):
                lines.append(f"| {a} | " + " | ".join(str(conf[(a, b)]) for b in ("low", "medium", "high")) + " |")
            lines.append("")
        if base["lex_miss"] is not None:
            lines += [f"Lexicon misses: {fmt(base['lex_miss'])} of postings WITHOUT a lexicon term were judged "
                      f"relevant by the annotator ({ci([b['lex_miss'] for b in boots])}).", ""]
        summary.append((name, base["macro_f1"], base["any"][2]))

    if len(summary) > 1:
        best = max(summary, key=lambda s: -1 if s[1] is None else s[1])
        lines += ["## Comparison", "", "| Model | Macro-F1 | F1 any channel vs none |", "|---|---:|---:|"]
        for n, m, a in summary:
            lines.append(f"| {n}{' (best macro-F1)' if n == best[0] else ''} | {fmt(m)} | {fmt(a)} |")
        lines.append("")

    p2 = Path(args.pass2)
    if p2.exists():
        s2 = read_sheet(p2)
        both = [(sheet[p], s2[p]) for p in s2 if p in sheet and sheet[p][0] and s2[p][0]]
        if both:
            k_ch = ckappa([a[0] for a, b in both], [b[0] for a, b in both])
            agree = sum(a[0] == b[0] for a, b in both) / len(both)
            ip = [(LEVEL[a[1]], LEVEL[b[1]]) for a, b in both
                  if a[0] == b[0] and a[0] not in ("none", "unclear") and a[1] in LEVEL and b[1] in LEVEL]
            lines += ["## Annotator consistency (pass 1 against pass 2)", "",
                      f"{len(both)} postings annotated twice. Channel: agreement {agree:.1%}, Cohen's kappa "
                      f"{fmt(k_ch)}. Intensity (same channel both times, {len(ip)} postings): weighted kappa "
                      f"{fmt(wkappa(ip) if ip else None)}.", ""]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
