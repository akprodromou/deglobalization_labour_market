"""
Month 3, step 3b: draw the 300 postings to annotate by hand (the brief's evaluation set).

The population is the set of lexicon-flagged postings (data/tagged/flagged_*.jsonl,
duplicates already dropped, day weights from the corpus). They are drawn in
strata defined by the channel one model predicted (the "sampling model", the
tags file given with --tags): one stratum per channel plus `none`, plus
`unparsed` if some answers were invalid. Equal numbers are drawn from every
stratum as far as the stratum has postings, and what a small stratum cannot
fill goes to the others. Drawing equal numbers is what gives the rare channels
(defense, critical materials ...) enough annotated postings to be scored at
all; the stratum weights bring everything back to the population.

The sheet does not show the prediction. It shows the title, the lexicon terms
found in the posting (the same evidence the model was given) and the text.
Other models can be scored on the same sample: the weights come from the
sampling design, not from the model being scored.

Sheet columns to fill (see the annotation guide in docs/tagging_annotation_guide.md,
which uses the same channel and intensity definitions as the prompt):
    channel    one of: reshoring, defense, critical materials, energy security,
               trade compliance, diversification, none, unclear
    intensity  high / medium / low (leave empty when channel is none or unclear)
    note       free text; the date of each sitting in the first row of the sitting

Files (data/tagging/ is not tracked by git: it holds employer text)
    annotation_sheet.csv        what you annotate
    annotation_key.jsonl        hidden: stratum, weight, terms per posting_id
    annotation_sheet_pass2.csv  (--pass2 N) a random N of the same postings in a new
                                order, to annotate again at least three days later

Run (project root):
    python -m diagnostics.59_make_tagging_sheet --tags data/tagged/tags_qwen2.5_7b_tagging_v1.jsonl
    python -m diagnostics.59_make_tagging_sheet --pass2 50          # later
    # round 2: draw AFTER the revised prompt has tagged everything, with that run's tags as the strata;
    # other seed, round-1 postings left out, own folder
    python -m diagnostics.59_make_tagging_sheet --tags data/tagged/tags_qwen2.5_7b_tagging_v7.jsonl \\
        --seed 20261028 --exclude-key data/tagging/annotation_key.jsonl --out-dir data/tagging_r2 \\
        --n 300 --unflagged 0
    python -m diagnostics.59_make_tagging_sheet --pass2 50 --out-dir data/tagging_r2   # round-2 pass 2
Options: --n 300  --take-all-terms "customs agency,customs service" (annotate every flagged posting with
one of these terms, as an extra stratum outside the 300)  --unflagged 0   (--unflagged N adds N postings WITHOUT a lexicon
term, outside the 300, to estimate how much the lexicon misses; they are scored
by script 60 as lexicon recall.)
"""

import argparse
import csv
import json
import random
import re
from collections import defaultdict
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

CORPUS = Path("data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl")
OUT_DIR = Path("data/tagging")
SEED = 20261021
TEXT_CHARS = 1800


def allocate(sizes, n):
    """Equal allocation over strata, capped by stratum size, remainder redistributed."""
    alloc = {s: 0 for s in sizes}
    left, open_ = n, [s for s in sizes if sizes[s] > 0]
    while left > 0 and open_:
        share = max(1, left // len(open_))
        for s in list(open_):
            take = min(share, sizes[s] - alloc[s], left)
            alloc[s] += take
            left -= take
            if alloc[s] >= sizes[s]:
                open_.remove(s)
            if left == 0:
                break
    return alloc


def write_sheet(path, rows, terms):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["item", "posting_id", "title", "terms_found", "text", "channel", "intensity", "note"])
        for k, r in enumerate(rows, 1):
            it = r["item"]
            text = re.sub(r"\s+", " ", it.get("description") or "")[:TEXT_CHARS]
            w.writerow([k, str(it["id"]), (it.get("title") or "").strip(),
                        "; ".join(terms.get(str(it["id"]), [])), text, "", "", ""])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", default=str(CORPUS))
    ap.add_argument("--tags", default=None, help="tags file of the sampling model")
    ap.add_argument("--flagged", default=None)
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--unflagged", type=int, default=0)
    ap.add_argument("--take-all-terms", default="",
                    help="comma-separated lexicon terms; every flagged posting containing one of them is "
                         "annotated (a stratum taken whole, outside the --n sample, weight 1 per posting's "
                         "day weight), e.g. the customs-authority postings")
    ap.add_argument("--take-all-label", default="take_all")
    ap.add_argument("--pass2", type=int, default=0)
    ap.add_argument("--seed", type=int, default=SEED, help="random seed (use another one for a second sample)")
    ap.add_argument("--exclude-key", action="append", default=[],
                    help="annotation_key.jsonl of an earlier sample: its postings are left out, so a new "
                         "sample (e.g. for testing a revised prompt) is fresh. Repeatable.")
    ap.add_argument("--out-dir", default=str(OUT_DIR), help="folder for the sheet and key (default data/tagging)")
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    seed = args.seed
    excluded = set()
    for kp in args.exclude_key:
        excluded |= {json.loads(l)["posting_id"] for l in open(kp, encoding="utf-8") if l.strip()}

    rows, dropped = load_corpus(Path(args.corpus))
    by_id = {str(r["item"]["id"]): r for r in rows}
    flag_path = Path(args.flagged) if args.flagged else \
        Path("data/tagged") / f"flagged_{Path(args.corpus).stem}.jsonl"
    flagged = {}
    for l in open(flag_path, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            flagged[r["posting_id"]] = r
    terms = {k: v["terms"] for k, v in flagged.items()}
    key_path = out_dir / "annotation_key.jsonl"

    if args.pass2:
        keys = [json.loads(l) for l in open(key_path, encoding="utf-8") if l.strip()]
        pick = random.Random(seed + 1).sample(keys, min(args.pass2, len(keys)))
        pick = [by_id[k["posting_id"]] for k in pick if k["posting_id"] in by_id]
        random.Random(seed + 2).shuffle(pick)
        write_sheet(out_dir / "annotation_sheet_pass2.csv", pick, terms)
        print(f"Wrote {out_dir / 'annotation_sheet_pass2.csv'} ({len(pick)} postings). Annotate it at "
              "least three days after pass 1, without looking at pass 1.")
        return
    if not args.tags:
        raise SystemExit("--tags is required (the tags file of the model that defines the strata)")

    pred = {}
    for l in open(args.tags, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            pred[r["posting_id"]] = r["channel"] if r["ok"] else "unparsed"
    forced_terms = {t.strip().lower() for t in args.take_all_terms.split(",") if t.strip()}
    strata, forced = defaultdict(list), []
    if excluded:
        print(f"Leaving out {len(excluded):,} postings from the earlier sample(s).")
    for pid in flagged:
        if pid in excluded:
            continue
        if pid in by_id and pid in pred:
            if forced_terms & {t.lower() for t in terms[pid]}:
                forced.append(by_id[pid])
            else:
                strata[pred[pid]].append(by_id[pid])
    missing = [p for p in flagged if p not in pred]
    if missing:
        print(f"WARNING: {len(missing):,} flagged postings have no tag in {args.tags} and are left out. "
              "Finish script 58 first.")
    sizes = {s: len(v) for s, v in strata.items()}
    alloc = allocate(sizes, args.n)
    rng = random.Random(seed)
    chosen, keys = [], []
    tw = sum(r["w"] for v in strata.values() for r in v)
    print("stratum (sampling model's channel) | flagged postings | weighted share | annotated")
    for s in sorted(sizes, key=lambda x: -sizes[x]):
        pool = strata[s]
        n = alloc[s]
        take = rng.sample(pool, n) if n else []
        print(f"  {s:<20} | {len(pool):>8,} | {sum(r['w'] for r in pool) / tw:>6.1%} | {n}")
        for r in take:
            chosen.append(r)
            keys.append({"posting_id": str(r["item"]["id"]), "stratum": s, "day": r["day"],
                         "weight": r["w"] * len(pool) / n, "flagged": True,
                         "terms": terms[str(r["item"]["id"])]})
    if forced:
        for r in forced:
            chosen.append(r)
            keys.append({"posting_id": str(r["item"]["id"]), "stratum": args.take_all_label, "day": r["day"],
                         "weight": r["w"], "flagged": True, "terms": terms[str(r["item"]["id"])]})
        print(f"  {args.take_all_label} (taken whole, outside the {args.n}) | {len(forced):>5,} postings")
    if args.unflagged:
        pool = [r for r in rows if str(r["item"]["id"]) not in flagged and str(r["item"]["id"]) not in excluded]
        take = rng.sample(pool, min(args.unflagged, len(pool)))
        for r in take:
            chosen.append(r)
            keys.append({"posting_id": str(r["item"]["id"]), "stratum": "unflagged", "day": r["day"],
                         "weight": r["w"] * len(pool) / len(take), "flagged": False, "terms": []})
        print(f"  unflagged (outside the {args.n})  | {len(pool):>8,} |        | {len(take)}")
    rng.shuffle(chosen)
    write_sheet(out_dir / "annotation_sheet.csv", chosen, terms)
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(key_path, "w", encoding="utf-8") as f:
        for k in keys:
            f.write(json.dumps(k, ensure_ascii=False) + "\n")
    print(f"\nWrote {out_dir / 'annotation_sheet.csv'} ({len(chosen)} postings) and {key_path}")
    print("Fill `channel` and `intensity` per docs/tagging_annotation_guide.md. Do not open the key.")


if __name__ == "__main__":
    main()
