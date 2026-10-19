"""
Month 3: draw the validation sample and write the sheet to be labelled by hand.

Reads the day-stratified corpus of script 52, removes postings whose
description is an exact copy of an earlier one (the sheet must not ask for
the same posting twice), and draws a sample in three strata defined by a broad
keyword screen. The screen is deliberately generous (it is not the classifier)
and only decides where to look:

    stratum 1: the text contains a metals word
    stratum 2: a manufacturing word but no metals word
    stratum 3: neither

Every stratum is sampled uniformly. Because the strata are known, the score
script can weight each labelled posting back to the population, and any
classifier built later can be scored on this same sample (precision, recall
and prevalence with confidence intervals). The sample does not depend on the
classifier, so it cannot leak anything from training.

Weights. Each corpus posting stands for (day total / postings taken that day)
postings of its day (script 52). Inside a stratum the draw is uniform, so a
sampled posting's final weight is that day weight times N_stratum / n_stratum.
Dropping exact duplicates changes the number taken per day, so the day weight
is recomputed after the drop (an approximation: the population is treated as
distinct texts).

Files written (data/labelling/ is not tracked by git: it holds employer text):
    validation_sheet.csv   what you label: item, posting_id, title, text,
                           manufacturing, metals, note (no stratum, no screen
                           flags, no prediction: labelling is blind)
    validation_key.jsonl   hidden: stratum, weight, screen flags per posting_id
    validation_sheet_pass2.csv (with --pass2 N) a random N of the same
                           postings in a new order, to be labelled again after
                           a few days to measure your own consistency

Run (project root, venv active):
    python -m diagnostics.53_make_labelling_sheet
    python -m diagnostics.53_make_labelling_sheet --n1 100 --n2 150 --n3 150
    python -m diagnostics.53_make_labelling_sheet --pass2 50     # later, after pass 1
"""

import argparse
import csv
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

CORPUS = Path("data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl")
OUT_DIR = Path("data/labelling")
SEED = 20261018
TEXT_CHARS = 1200      # characters of description shown on the sheet
SCREEN_CHARS = 1500    # characters of description searched by the screen

# The corpus is almost entirely English (about 98% of postings), with Swedish
# in about 2%, so both languages are listed. Terms match at the START of a word
# only (regex \b): plain substring matching made "iron" hit "environment" in
# 39% of postings.
METALS = ["stål", "järn", "metall", "aluminium", "koppar", "plåt", "svets", "gjuteri",
          "gjutning", "valsverk", "smide", "smed", "bearbetning", "cnc", "legering",
          "rostfri", "steel", "metal", "iron", "aluminum", "aluminium", "copper",
          "welding", "welder", "foundry", "machining", "stainless", "alloy"]
MANUF = ["tillverk", "produktion", "industri", "fabrik", "verkstad", "montage",
         "montör", "maskinoperatör", "operatör", "automation", "mekanik",
         "livsmedelsindustri", "pappersbruk", "sågverk", "bryggeri",
         "manufactur", "factory", "assembly", "production", "plant operator",
         "machine operator", "industrial", "fabricat", "mill ", "process engineer"]
_METALS_RX = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in METALS) + ")")
_MANUF_RX = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in MANUF) + ")")


def norm(t):
    return re.sub(r"\W+", " ", (t or "").lower()).strip()


def screen(item):
    t = ((item.get("title") or "") + " " + (item.get("description") or "")[:SCREEN_CHARS]).lower()
    m = bool(_METALS_RX.search(t))
    f = m or bool(_MANUF_RX.search(t))
    return m, f


def load_corpus(path):
    """Deduplicated postings with their day weights."""
    by_day = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            for it in r["items"]:
                by_day[r["day"]].append((r["total"], it))
    seen, out, dropped = set(), [], 0
    for day in sorted(by_day):
        kept = []
        for total, it in by_day[day]:
            h = hashlib.md5(norm(it.get("description")).encode()).hexdigest()
            if h in seen:
                dropped += 1
                continue
            seen.add(h)
            kept.append((total, it))
        for total, it in kept:
            out.append({"item": it, "day": day, "w": total / len(kept)})
    return out, dropped


def write_sheet(path, rows, hidden=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["item", "posting_id", "title", "text", "manufacturing", "metals", "note"])
        for k, r in enumerate(rows, 1):
            it = r["item"]
            text = re.sub(r"\s+", " ", (it.get("description") or ""))[:TEXT_CHARS]
            w.writerow([k, str(it["id"]), (it.get("title") or "").strip(), text, "", "", ""])


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", default=str(CORPUS))
    ap.add_argument("--n1", type=int, default=100, help="stratum 1 (metals words)")
    ap.add_argument("--n2", type=int, default=150, help="stratum 2 (manufacturing words only)")
    ap.add_argument("--n3", type=int, default=150, help="stratum 3 (neither)")
    ap.add_argument("--pass2", type=int, default=0,
                    help="write a repeat sheet of N postings of the existing sample and stop")
    args = ap.parse_args()

    rows, dropped = load_corpus(Path(args.corpus))
    print(f"{len(rows):,} postings after dropping {dropped:,} exact duplicates")
    by_id = {str(r["item"]["id"]): r for r in rows}
    rng = random.Random(SEED)

    key_path = OUT_DIR / "validation_key.jsonl"
    if args.pass2:
        keys = [json.loads(l) for l in open(key_path, encoding="utf-8") if l.strip()]
        pick = random.Random(SEED + 1).sample(keys, min(args.pass2, len(keys)))
        pick = [by_id[str(k["posting_id"])] for k in pick if str(k["posting_id"]) in by_id]
        random.Random(SEED + 2).shuffle(pick)
        write_sheet(OUT_DIR / "validation_sheet_pass2.csv", pick)
        print(f"Wrote {OUT_DIR / 'validation_sheet_pass2.csv'} ({len(pick)} postings). "
              "Label it at least three days after pass 1, without looking at pass 1.")
        return

    strata = {1: [], 2: [], 3: []}
    for r in rows:
        m, f = screen(r["item"])
        r["metals_hit"], r["manuf_hit"] = m, f
        strata[1 if m else 2 if f else 3].append(r)
    want = {1: args.n1, 2: args.n2, 3: args.n3}
    chosen, keys = [], []
    print("stratum | corpus postings | weighted share of population | sampled")
    tot_w = sum(r["w"] for r in rows)
    for s in (1, 2, 3):
        pool = strata[s]
        n = min(want[s], len(pool))
        take = rng.sample(pool, n) if n else []
        sw = sum(r["w"] for r in pool)
        print(f"   {s}    | {len(pool):>8,}        | {sw / tot_w:>6.1%}                    | {n}")
        for r in take:
            chosen.append(r)
            keys.append({"posting_id": str(r["item"]["id"]), "stratum": s, "day": r["day"],
                         "weight": r["w"] * len(pool) / n,
                         "screen_metals": r["metals_hit"], "screen_manufacturing": r["manuf_hit"]})
    rng.shuffle(chosen)
    write_sheet(OUT_DIR / "validation_sheet.csv", chosen)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(key_path, "w", encoding="utf-8") as f:
        for k in keys:
            f.write(json.dumps(k, ensure_ascii=False) + "\n")
    print(f"\nWrote {OUT_DIR / 'validation_sheet.csv'} ({len(chosen)} postings) and {key_path}")
    print("Label the two columns `manufacturing` and `metals` with yes / no / unclear, "
          "following docs/labelling_protocol.md. Do not open validation_key.jsonl.")


if __name__ == "__main__":
    main()
