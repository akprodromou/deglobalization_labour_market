"""
Month 3, step 2b: expand the lexicon with sentence-embedding similarity.

The brief: encode the seed terms with multilingual-e5, retrieve semantically
close phrases from the postings that are not in the seed list.

How it works
  1. Candidate phrases: all 1- to 4-word phrases that occur in at least
     --min-df postings (Apriori counting, corpus_io.frequent_ngrams; phrases
     never cross a sentence, comma or bracket; no stop word at either end).
     If there are more than --max-candidates, the most frequent are kept.
  2. Each seed term and each of its variants is encoded, and so is each
     candidate, with the model's "query: " prefix (the e5 convention for
     symmetric similarity between short texts), L2-normalised.
  3. For every seed term the --k nearest candidates by cosine similarity are
     retrieved (FAISS inner-product index if faiss is installed, otherwise a
     plain matrix product: with a few hundred thousand phrases both are fast).
  4. A candidate is dropped if it is, contains, or is part of a seed term
     (same overlap rule as script 55). The rest go to a review sheet, ordered
     by the best similarity, with the seed it was closest to and the number
     of different seeds that retrieved it.

Nothing is added automatically. Similarity is a reason to look at a phrase,
not a verdict that it belongs to a channel: "customs clearance" will be close
to "customs compliance" whatever the channel. A person reads the sheet.

Output
    data/lexicon/candidates_embedding.csv   term, nearest_seed, channel, sim,
        n_seeds, df, example, keep (fill 1), channel_assigned (fill)

Run on Google Colab (GPU runtime), after putting the repo, the corpus file and
lexicon/seed_lexicon.csv in place:
    !pip install -q sentence-transformers faiss-cpu scikit-learn
    !python -m diagnostics.56_lexicon_embedding_expansion
Locally (CPU) it also works, more slowly: roughly a few hundred phrases per second.

    --model intfloat/multilingual-e5-base   (default; LaBSE also named in the brief:
                                             --model sentence-transformers/LaBSE --prefix "")
    --encoder debug   character n-gram hashing, NOT a semantic model: for testing
                      that the pipeline runs end to end without downloading a model.
"""

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus, posting_text, frequent_ngrams
    from diagnostics.lexicon_io import read_lexicon, context
except ImportError:
    from corpus_io import load_corpus, posting_text, frequent_ngrams
    from lexicon_io import read_lexicon, context

CORPUS = Path("data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl")
SEEDS = Path("lexicon/seed_lexicon.csv")
OUT_CSV = Path("data/lexicon/candidates_embedding.csv")
MAX_CHARS = 6000


def seed_overlap(g, seed_forms):
    gt = g.split()
    for sf in seed_forms:
        st = sf.split()
        if g in sf or sf in g:
            return True
        for k in range(1, min(len(gt), len(st))):
            if gt[-k:] == st[:k] or gt[:k] == st[-k:]:
                return True
    return False


def make_encoder(kind, model_name, prefix, device):
    if kind == "debug":
        from sklearn.feature_extraction.text import HashingVectorizer

        hv = HashingVectorizer(analyzer="char_wb", ngram_range=(3, 5), n_features=512,
                               alternate_sign=False, norm="l2")

        def enc(texts):
            return hv.transform([t.replace("query: ", "") for t in texts]).toarray().astype("float32")

        return enc
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name, device=device)

    def enc(texts):
        return model.encode([prefix + t for t in texts], batch_size=256, show_progress_bar=True,
                            normalize_embeddings=True, convert_to_numpy=True).astype("float32")

    return enc


def nearest(seed_vecs, cand_vecs, k):
    """Indices and cosine similarities of the k nearest candidates per seed vector."""
    try:
        import faiss

        index = faiss.IndexFlatIP(cand_vecs.shape[1])
        index.add(cand_vecs)
        sims, idx = index.search(seed_vecs, k)
        return idx, sims
    except ImportError:
        out_i, out_s = [], []
        for v in seed_vecs:
            s = cand_vecs @ v
            top = np.argpartition(-s, min(k, len(s) - 1))[:k]
            top = top[np.argsort(-s[top])]
            out_i.append(top)
            out_s.append(s[top])
        return np.array(out_i), np.array(out_s)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", default=str(CORPUS))
    ap.add_argument("--seeds", default=str(SEEDS))
    ap.add_argument("--model", default="intfloat/multilingual-e5-base")
    ap.add_argument("--prefix", default="query: ")
    ap.add_argument("--encoder", default="model", choices=["model", "debug"])
    ap.add_argument("--device", default=None, help="cuda / cpu (default: automatic)")
    ap.add_argument("--min-df", type=int, default=5, help="a phrase must occur in this many postings")
    ap.add_argument("--max-n", type=int, default=4)
    ap.add_argument("--max-candidates", type=int, default=300000)
    ap.add_argument("--k", type=int, default=30, help="neighbours retrieved per seed term")
    ap.add_argument("--top", type=int, default=1500, help="rows in the review sheet")
    args = ap.parse_args()

    rows, dropped = load_corpus(Path(args.corpus))
    texts = [posting_text(r["item"], MAX_CHARS) for r in rows]
    print(f"{len(rows):,} postings ({dropped:,} exact duplicates dropped)")
    print("Counting phrases ...")
    df = frequent_ngrams(texts, min_df=args.min_df, max_n=args.max_n)
    cands = sorted(df, key=lambda g: -df[g])[:args.max_candidates]
    print(f"{len(df):,} frequent phrases, {len(cands):,} kept as candidates")

    lex = read_lexicon(Path(args.seeds))
    seed_forms, queries, qmap = set(), [], []
    for row in lex:
        for form in [row["term"]] + row["variants"]:
            seed_forms.add(" ".join(re.split(r"[-\s+]+", form.lower())).strip())
            queries.append(form.lower())
            qmap.append(row)
    cands = [g for g in cands if not seed_overlap(g, seed_forms)]
    print(f"{len(cands):,} candidates after removing seed overlaps")

    enc = make_encoder(args.encoder, args.model, args.prefix, args.device)
    print("Encoding seeds and candidates ...")
    qv = enc(queries)
    cv = enc(cands)
    idx, sims = nearest(qv, cv, min(args.k, len(cands)))

    best = {}                                   # candidate -> [sim, seed row, set of seed terms]
    for qi in range(len(queries)):
        for j, s in zip(idx[qi], sims[qi]):
            g = cands[j]
            b = best.setdefault(g, [-1.0, None, set()])
            b[2].add(qmap[qi]["term"])
            if s > b[0]:
                b[0], b[1] = float(s), qmap[qi]
    ranked = sorted(best.items(), key=lambda kv: -kv[1][0])[:args.top]

    # one snippet per candidate: first posting that contains the phrase
    low = [t.lower() for t in texts]
    out = []
    for g, (s, row, seeds) in ranked:
        ex = ""
        rx = re.compile(r"(?<!\w)" + re.escape(g) + r"(?!\w)")
        for t, orig in zip(low, texts):
            m = rx.search(t)
            if m:
                ex = context(orig, m.group(0))
                break
        out.append({"term": g, "nearest_seed": row["term"], "channel": row["channel"],
                    "sim": round(s, 3), "n_seeds": len(seeds), "df": df[g], "example": ex,
                    "keep": "", "channel_assigned": ""})
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()) if out else ["term"])
        w.writeheader()
        w.writerows(out)
    print(f"Wrote {OUT_CSV} ({len(out)} candidates). Put 1 in `keep` and a channel in "
          "`channel_assigned` for each term to add.")
    if args.encoder == "debug":
        print("NOTE: --encoder debug is not a semantic model; use it only to test the pipeline.")


if __name__ == "__main__":
    main()
