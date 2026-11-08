"""
Month 4 (optional, supervisor suggestion): match job-posting sentences to Lightcast skills by embedding similarity.

Which Lightcast skills? lexicon/lightcast_sovereign_skills.csv (skill, group, description). group "sovereign" are the
skills about sovereign cloud and data; group "context" are skills reported separately (Private Cloud, High
Performance Computing), because they are common in ordinary IT postings. Add rows as more skills are found
(Lightcast API access requested).

How it works
  1. Each posting (title + description, boilerplate stripped, as the tagger sees it) is split into sentences.
     Identical sentences are encoded once (company paragraphs repeat across thousands of postings).
  2. Skill = "name. description" and every sentence are encoded with multilingual-e5 ("query: " prefix, as in script 56),
     L2-normalised; similarity is the cosine.
  3. Per posting and skill the best sentence is kept. A posting "requires" a skill when the best similarity is at least
     --threshold. The threshold is chosen from the review sheet, not assumed: label the sheet (keep = 1 when the
     sentence really says the skill is needed or used), look at where the 1s stop, and set --threshold there.
  4. Output: monthly weighted share of postings per skill group (day weights of the corpus), at several thresholds.

Nothing is tagged as a deglobalization channel here: a skill mention is a separate indicator (see the evaluation report:
a mention of "sovereign cloud" in a list of topics does not make a posting diversification).

Outputs
    data/lexicon/skill_match_review.csv   skill, band, sim, posting_id, title, sentence, keep (fill 1)
    data/tagged/skill_match_postings.csv  posting_id, day, skill, group, sim, sentence (best per posting and skill, sim >= --min-sim)
    docs/skill_match_report.md            postings per skill and month, weighted shares at the thresholds

Run on Google Colab (GPU), same setup as script 56:
    !pip install -q sentence-transformers scikit-learn
    !python -m diagnostics.79_lightcast_skill_match --corpus data/raw/corpus_jobbland.se_2024-01_2026-09.jsonl --tag jobbland
Another board: --tag lesjeudis (the outputs get the tag). Test without a model: --encoder debug.
"""
import argparse, csv, re, sys, random
from collections import defaultdict
from pathlib import Path
import numpy as np

try:
    from diagnostics.corpus_io import load_corpus, posting_text
except ImportError:
    from corpus_io import load_corpus, posting_text

SPLIT = re.compile(r"(?<=[.!?;:])\s+|\s*[•·\n]\s*")


def sentences(text):
    out = []
    for s in SPLIT.split(text):
        s = s.strip(" -\t")
        if 25 <= len(s) <= 400:
            out.append(s)
    return out


def make_encoder(kind, model_name, prefix):
    if kind == "debug":                      # character n-gram hashing: NOT semantic, only tests the pipeline
        def enc(texts):
            m = np.zeros((len(texts), 512), dtype=np.float32)
            for i, t in enumerate(texts):
                t = t.lower()
                for j in range(len(t) - 2):
                    m[i, hash(t[j:j + 3]) % 512] += 1
            n = np.linalg.norm(m, axis=1, keepdims=True); n[n == 0] = 1
            return m / n
        return enc
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    return lambda texts: model.encode([prefix + t for t in texts], batch_size=128, normalize_embeddings=True,
                                      show_progress_bar=False).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, nargs="+")
    ap.add_argument("--skills", default="lexicon/lightcast_sovereign_skills.csv")
    ap.add_argument("--tag", default="corpus")
    ap.add_argument("--model", default="intfloat/multilingual-e5-base")
    ap.add_argument("--prefix", default="query: ")
    ap.add_argument("--encoder", default="model", choices=["model", "debug"])
    ap.add_argument("--max-chars", type=int, default=6000)
    ap.add_argument("--min-sim", type=float, default=0.78, help="keep matches from this similarity (output file)")
    ap.add_argument("--thresholds", type=float, nargs="+", default=[0.80, 0.84, 0.88])
    ap.add_argument("--per-band", type=int, default=4, help="review sentences per skill and similarity band")
    ap.add_argument("--limit", type=int, default=0, help="only the first N postings (tests)")
    ap.add_argument("--chunk", type=int, default=20000)
    args = ap.parse_args()

    skills = list(csv.DictReader(open(args.skills, encoding="utf-8-sig")))
    names = [s["skill"] for s in skills]
    rows = []
    for p in args.corpus:
        r, _ = load_corpus(Path(p)); rows += r
    if args.limit:
        rows = rows[:args.limit]
    print(f"{len(rows):,} postings, {len(skills)} skills")

    post_sents, uniq, index = [], [], {}
    for r in rows:
        ss = sentences(posting_text(r["item"], args.max_chars))
        ids = []
        for s in ss:
            k = index.get(s)
            if k is None:
                k = index[s] = len(uniq); uniq.append(s)
            ids.append(k)
        post_sents.append(ids)
    print(f"{len(uniq):,} distinct sentences")

    enc = make_encoder(args.encoder, args.model, args.prefix)
    sv = enc([f"{s['skill']}. {s['description']}" for s in skills])
    sims = np.zeros((len(uniq), len(skills)), dtype=np.float16)
    for a in range(0, len(uniq), args.chunk):
        sims[a:a + args.chunk] = (enc(uniq[a:a + args.chunk]) @ sv.T).astype(np.float16)
        print(f"  encoded {min(a + args.chunk, len(uniq)):,} / {len(uniq):,}")

    Path("data/tagged").mkdir(parents=True, exist_ok=True); Path("data/lexicon").mkdir(parents=True, exist_ok=True)
    Path("docs").mkdir(exist_ok=True)
    best = []                                # per posting: {skill_index: (sim, sentence_id)}
    for ids in post_sents:
        d = {}
        for k in ids:
            for j in range(len(skills)):
                v = float(sims[k, j])
                if v >= args.min_sim and (j not in d or v > d[j][0]):
                    d[j] = (v, k)
        best.append(d)

    with open(f"data/tagged/skill_match_postings_{args.tag}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["posting_id", "day", "skill", "group", "sim", "sentence"])
        for r, d in zip(rows, best):
            for j, (v, k) in d.items():
                w.writerow([r["item"]["id"], r["day"], names[j], skills[j]["group"], f"{v:.3f}", uniq[k]])

    bands = [(0.78, 0.82), (0.82, 0.86), (0.86, 0.90), (0.90, 1.01)]
    rng = random.Random(0)
    with open(f"data/lexicon/skill_match_review_{args.tag}.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["skill", "band", "sim", "posting_id", "title", "sentence", "keep"])
        for j, s in enumerate(names):
            for lo, hi in bands:
                pool, seen = [], set()
                for r, d in zip(rows, best):
                    if j in d and lo <= d[j][0] < hi and uniq[d[j][1]] not in seen:
                        seen.add(uniq[d[j][1]]); pool.append((r, d[j]))
                for r, (v, k) in rng.sample(pool, min(args.per_band, len(pool))):
                    w.writerow([s, f"{lo:.2f}-{min(hi, 1):.2f}", f"{v:.3f}", r["item"]["id"],
                                (r["item"].get("title") or "")[:80], uniq[k], ""])

    months = sorted({r["day"][:7] for r in rows})
    wt = defaultdict(float); hit = defaultdict(float)
    for r, d in zip(rows, best):
        m, wgt = r["day"][:7], r.get("w", 1.0)
        wt[m] += wgt
        for t in args.thresholds:
            for g in {skills[j]["group"] for j, (v, _) in d.items() if v >= t}:
                hit[(m, g, t)] += wgt
            for j, (v, _) in d.items():
                if v >= t:
                    hit[(m, names[j], t)] += wgt
    labels = sorted({s["group"] for s in skills}) + names
    with open(f"docs/skill_match_report_{args.tag}.md", "w", encoding="utf-8") as f:
        f.write(f"# Lightcast skill matching: {args.tag}\n\nWeighted share of postings (%), by month and similarity threshold. "
                "Choose the threshold from the labelled review sheet before reading these figures. "
                "Groups: any skill of the group.\n\n")
        for t in args.thresholds:
            f.write(f"## Threshold {t:.2f}\n\n| Month | " + " | ".join(labels) + " |\n|---|" + "---:|" * len(labels) + "\n")
            for m in months:
                f.write(f"| {m} | " + " | ".join(f"{100 * hit[(m, l, t)] / wt[m]:.2f}" for l in labels) + " |\n")
            f.write("\n")
    print("wrote the review sheet, the postings file and the report for tag", args.tag)


if __name__ == "__main__":
    main()
