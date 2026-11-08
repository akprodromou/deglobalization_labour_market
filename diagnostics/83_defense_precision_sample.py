"""
Month 3, step 8c: a blind sample to measure the precision of one channel's tags on a board that has no labels yet
(lesjeudis.com, channel defense by default).

Two modes.

1. Draw (default). Takes the postings tagged with the channel in the final tag files, splits them by the model's
   intensity (high, medium, low), draws --n postings in equal numbers per stratum (fixed seed) and writes
       data/tagging_lj/<channel>_sample_sheet.csv   what you label BLIND (channel, intensity, note empty; the model's
                                                    tag is not shown); never overwritten if it exists
       data/tagging_lj/<channel>_sample_key.jsonl   the model's tag and the stratum sizes (needed for scoring)
   You see what the tagger saw: title and the first 3,000 characters of the description (boilerplate removed), plus
   short passages around matched lexicon terms that lie further in.
   Label `channel` with one of: reshoring, defense, critical materials, energy security, trade compliance,
   diversification, none, unclear, using the annotation guide. `intensity`: low, medium, high (empty for none).

2. Score (--score). Reads the filled sheet and the key and reports the weighted precision of the channel tag (share of
   sampled postings you also labelled with the channel, each posting weighted by its stratum size) with a 95% bootstrap
   interval, the precision per stratum, and intensity agreement among postings you labelled with the channel.
   Unclear postings are left out. Writes docs/<channel>_precision_sample.md.

Run (project root, venv active):
    python -m diagnostics.83_defense_precision_sample \
        --tags data/tagged/tags_v12_lesjeudis.com_2024-08_2025-04.post.jsonl data/tagged/tags_v12_lesjeudis.com_2025-05_2025-09.post.jsonl \
        --corpus data/raw/corpus_lesjeudis.com_2024-08_2025-04.jsonl data/raw/corpus_lesjeudis.com_2025-05_2025-09.jsonl
    (label the sheet, then)
    python -m diagnostics.83_defense_precision_sample --score data/tagging_lj/defense_sample_sheet.csv --key data/tagging_lj/defense_sample_key.jsonl
Options: --channel (default defense), --n (default 60), --seed (default 2026), --lexicon, --out-dir.
"""
import argparse, csv, json, random
from collections import defaultdict
from pathlib import Path
import numpy as np

try:
    from diagnostics.corpus_io import load_corpus, posting_text
    from diagnostics.lexicon_io import read_lexicon, compile_lexicon, match_terms, context
except ImportError:
    from corpus_io import load_corpus, posting_text
    from lexicon_io import read_lexicon, compile_lexicon, match_terms, context

STRATA = ["high", "medium", "low"]
LABELS = {"reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification", "none", "unclear"}


def draw(a):
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    sheet, keyp = out / f"{a.channel}_sample_sheet.csv", out / f"{a.channel}_sample_key.jsonl"
    if sheet.exists():
        raise SystemExit(f"{sheet} exists and is never overwritten (it may hold your labels). Move it away to draw again.")
    tagged = {}
    for p in a.tags:
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                if r.get("ok") and r.get("channel") == a.channel:
                    tagged[str(r["posting_id"])] = r
    items = {}
    for p in a.corpus:
        rows, _ = load_corpus(p)
        for r in rows:
            items[str(r["item"]["id"])] = r["item"]
    comp = compile_lexicon(read_lexicon(a.lexicon))
    strata = {s: sorted(k for k, r in tagged.items() if r["intensity"] == s and k in items) for s in STRATA}
    sizes = {s: len(v) for s, v in strata.items()}
    print(f"{sum(sizes.values())} postings tagged {a.channel} and found in the corpus; strata {sizes}")
    rng = random.Random(a.seed)
    per = a.n // len(STRATA)
    chosen = []
    for s in STRATA:
        pool = strata[s]
        chosen += [(s, k) for k in rng.sample(pool, min(per, len(pool)))]
    rng.shuffle(chosen)
    with open(sheet, "w", newline="", encoding="utf-8-sig") as f, open(keyp, "w", encoding="utf-8") as kf:
        w = csv.writer(f)
        w.writerow(["item", "posting_id", "title", "terms_found", "text", "channel", "intensity", "note"])
        for i, (s, k) in enumerate(chosen, 1):
            it = items[k]
            full = posting_text(it)
            head = full[:3000]
            late = []
            for row, m in match_terms(comp, full):
                at = full.lower().find(m.lower())
                if at > 3000 and len(late) < 3:
                    late.append(context(full, m, width=200))
            text = head + ("\n\n[passages beyond character 3,000 around matched terms]\n- " + "\n- ".join(late) if late else "")
            terms = "; ".join(sorted({row["term"] for row, _ in match_terms(comp, full)}))
            w.writerow([i, k, (it.get("title") or "").strip(), terms, text, "", "", ""])
            kf.write(json.dumps({"item": i, "posting_id": k, "stratum": s, "stratum_size": sizes[s], "stratum_n": per if sizes[s] >= per else sizes[s],
                                 "model_channel": tagged[k]["channel"], "model_intensity": tagged[k]["intensity"],
                                 "model_evidence": tagged[k].get("evidence", "")}, ensure_ascii=False) + "\n")
    print(f"wrote {sheet} ({len(chosen)} postings) and {keyp}. Label channel and intensity, then run with --score.")


def score(a):
    key = {str(json.loads(l)["posting_id"]): json.loads(l) for l in open(a.key, encoding="utf-8") if l.strip()}
    ch = key[next(iter(key))]["model_channel"]
    rows = []
    for r in csv.DictReader(open(a.score, encoding="utf-8-sig")):
        lab = (r["channel"] or "").strip().lower().replace("defence", "defense")
        if lab not in LABELS:
            raise SystemExit(f"posting {r['posting_id']}: channel label '{r['channel']}' is empty or not one of {sorted(LABELS)}")
        if lab == "unclear":
            continue
        k = key[str(r["posting_id"])]
        rows.append((k["stratum"], k["stratum_size"], lab == ch, (r["intensity"] or "").strip().lower(), k["model_intensity"], lab))
    by = defaultdict(list)
    for s, size, hit, hi, mi, lab in rows:
        by[s].append((size, hit))
    def prec(draws):
        num = den = 0.0
        for s, v in draws.items():
            if not v: continue
            size = v[0][0]; h = np.mean([x[1] for x in v])
            num += size * h; den += size
        return num / den if den else np.nan
    obs = prec(by)
    rng = np.random.default_rng(2026); boots = []
    for _ in range(2000):
        d = {s: [v[i] for i in rng.integers(0, len(v), len(v))] for s, v in by.items() if v}
        boots.append(prec(d))
    lo, hi = np.nanpercentile(boots, [2.5, 97.5])
    L = [f"# Precision of the {ch} tag on the labelled sample", "",
         f"{len(rows)} labelled postings (unclear left out). Weighted precision **{obs:.2f}** (95% interval {lo:.2f} to {hi:.2f}); "
         "each posting stands for its stratum (the model's intensity), weighted by the stratum's size in the tagged set.", "",
         "| Model intensity | Stratum size | Labelled | Also labelled " + ch + " | Precision |", "|---|---:|---:|---:|---:|"]
    for s in STRATA:
        v = by.get(s, [])
        if v:
            L.append(f"| {s} | {v[0][0]} | {len(v)} | {sum(x[1] for x in v)} | {np.mean([x[1] for x in v]):.2f} |")
    order = {"low": 1, "medium": 2, "high": 3}
    agree = [(mi, hi_) for s, size, hit, hi_, mi, lab in rows if hit and hi_ in order and mi in order]
    if agree:
        L += ["", f"Intensity, among the {len(agree)} postings you also labelled {ch}: exact agreement "
              f"{sum(a_ == b for a_, b in agree)}/{len(agree)}, within one level {sum(abs(order[a_]-order[b]) <= 1 for a_, b in agree)}/{len(agree)}."]
    wrong = defaultdict(int)
    for s, size, hit, hi_, mi, lab in rows:
        if not hit: wrong[lab] += 1
    L += ["", "Postings tagged " + ch + " that you labelled otherwise: " + (", ".join(f"{k} {v}" for k, v in sorted(wrong.items())) or "none") + "."]
    p = Path("docs") / f"{ch}_precision_sample.md"; p.parent.mkdir(exist_ok=True); p.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L)); print("wrote", p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", nargs="+"); ap.add_argument("--corpus", nargs="+")
    ap.add_argument("--channel", default="defense"); ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--seed", type=int, default=2026); ap.add_argument("--lexicon", default="lexicon/lexicon.csv")
    ap.add_argument("--out-dir", default="data/tagging_lj")
    ap.add_argument("--score"); ap.add_argument("--key")
    a = ap.parse_args()
    if a.score:
        if not a.key: raise SystemExit("--score needs --key")
        score(a)
    else:
        if not (a.tags and a.corpus): raise SystemExit("drawing needs --tags and --corpus")
        draw(a)


if __name__ == "__main__":
    main()
