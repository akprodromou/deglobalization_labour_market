"""
Month 3, step 2a: how often do the seed terms occur, and which n-grams go with them?

Reads the day-stratified corpus (script 52), drops exact duplicates, and does two things.

1. SEED COVERAGE. For each seed term (lexicon/seed_lexicon.csv) it counts the
   postings that contain it (raw count and day-weighted estimate for the
   population) and the share of postings that contain at least one seed term,
   by month. This is the first thing to look at: a seed term that occurs in
   fewer than a handful of postings cannot anchor an expansion, and if almost
   nothing is flagged the corpus does not carry the vocabulary at all.

2. TF-IDF EXPANSION. Postings containing a seed term form the "flagged" set,
   the rest the "other" set. Candidate terms are the uni-, bi- and tri-grams
   (scikit-learn CountVectorizer, the TF-IDF weight is added below) found in
   at least --min-flagged-df flagged postings. Each candidate is ranked by how
   much more often it appears in flagged postings than in the others: the
   log odds ratio of its document frequencies (Haldane-Anscombe correction,
   +0.5 in every cell) divided by its standard error, i.e. a z-score. The mean
   TF-IDF weight in the flagged postings (sublinear tf, idf over the whole
   corpus) is reported next to it. The ranking is only a way of ordering the
   list for human review: nothing is added to the lexicon automatically.

   Guards: n-grams starting or ending with a stop word are dropped, as are
   those that contain a seed term, those found under fewer than
   --min-titles distinct posting titles (a repeated advertisement from one
   employer would otherwise dominate), and a shorter n-gram wholly inside a
   longer candidate with almost the same flagged count.

Outputs
    docs/lexicon_seed_coverage.md             counts per seed term and per month
    data/lexicon/candidates_tfidf.csv         review sheet (untracked: holds text
                                              snippets from postings)

Review sheet columns: term, n, df_flagged, df_other, z, mean_tfidf, titles,
example, keep (fill 1), channel (fill with one of the channels).

Run (project root, venv active):
    python -m diagnostics.55_lexicon_seed_coverage_tfidf
    python -m diagnostics.55_lexicon_seed_coverage_tfidf --min-flagged-df 4 --top 1500
"""

import argparse
import csv
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

try:
    from diagnostics.corpus_io import load_corpus, posting_text, STOP
    from diagnostics.lexicon_io import read_lexicon, compile_lexicon, match_terms, context
except ImportError:          # run as a plain script from the same folder
    from corpus_io import load_corpus, posting_text, STOP
    from lexicon_io import read_lexicon, compile_lexicon, match_terms, context

CORPUS = Path("data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl")
SEEDS = Path("lexicon/seed_lexicon.csv")
OUT_MD = Path("docs/lexicon_seed_coverage.md")
OUT_CSV = Path("data/lexicon/candidates_tfidf.csv")
MAX_CHARS = 6000          # characters of each posting that are searched
SPARSE = 5                # seed terms with fewer postings are called sparse


def seed_overlap(g, seed_forms):
    """True if the n-gram is part of a seed term or runs into one at an edge
    ("critical raw", "raw materials", "work with critical")."""
    gt = g.split()
    for sf in seed_forms:
        st = sf.split()
        if g in sf or sf in g:
            return True
        for k in range(1, min(len(gt), len(st))):
            if gt[-k:] == st[:k] or gt[:k] == st[-k:]:
                return True
    return False


def edge_ok(g):
    toks = g.split()
    return toks[0] not in STOP and toks[-1] not in STOP and len(toks[0]) > 1 and len(toks[-1]) > 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", default=str(CORPUS))
    ap.add_argument("--seeds", default=str(SEEDS))
    ap.add_argument("--min-flagged-df", type=int, default=3,
                    help="an n-gram must occur in this many flagged postings")
    ap.add_argument("--min-titles", type=int, default=2,
                    help="... under this many distinct titles")
    ap.add_argument("--top", type=int, default=1000, help="rows kept in the review sheet")
    args = ap.parse_args()

    rows, dropped = load_corpus(Path(args.corpus))
    N = len(rows)
    W = sum(r["w"] for r in rows)
    print(f"{N:,} postings after dropping {dropped:,} exact duplicates")
    lex = compile_lexicon(read_lexicon(Path(args.seeds)))
    texts = [posting_text(r["item"], MAX_CHARS) for r in rows]

    # ---- 1. seed coverage
    per_term = defaultdict(lambda: [0, 0.0, Counter()])    # raw, weighted, months
    flagged = []
    by_month = defaultdict(lambda: [0.0, 0.0, 0, 0])       # weight all, weight flagged, n, n flagged
    for k, (r, t) in enumerate(zip(rows, texts)):
        hits = match_terms(lex, t)
        month = r["day"][:7]
        by_month[month][0] += r["w"]
        by_month[month][2] += 1
        if hits:
            flagged.append(k)
            by_month[month][1] += r["w"]
            by_month[month][3] += 1
        for row, _ in hits:
            c = per_term[row["term"]]
            c[0] += 1
            c[1] += r["w"]
            c[2][month] += 1
    F = len(flagged)
    fw = sum(rows[k]["w"] for k in flagged)

    lines = ["# Seed coverage and TF-IDF expansion", "",
             f"Corpus: {Path(args.corpus).name}. {N:,} distinct postings after dropping "
             f"{dropped:,} exact duplicates; day-weighted population {W:,.0f}. "
             f"Text searched: title plus the first {MAX_CHARS:,} characters of the description.", "",
             f"Postings containing at least one seed term: **{F:,}** "
             f"({F / N:.1%} of the sample; {fw / W:.1%} weighted).", "",
             "## Seed terms", "",
             "| Term | Channel | Postings | Weighted estimate | Months with a hit | Flag |",
             "|---|---|---:|---:|---:|---|"]
    sparse = []
    for row in sorted(read_lexicon(Path(args.seeds)), key=lambda x: (x["channel"], x["term"])):
        raw, wt, mo = per_term.get(row["term"], [0, 0.0, Counter()])
        flag = ""
        if raw < SPARSE:
            flag = "sparse"
            sparse.append(row["term"])
        lines.append(f"| {row['term']} | {row['channel']} | {raw} | {wt:,.0f} | {len(mo)} | {flag} |")
    lines += ["", f"{len(sparse)} of the seed terms occur in fewer than {SPARSE} postings "
                  "(marked `sparse`). They stay in the lexicon, but they cannot anchor an expansion.", "",
              "## Flagged share by month", "",
              "| Month | Postings | Flagged | Weighted share flagged |", "|---|---:|---:|---:|"]
    for m in sorted(by_month):
        a, b, n, nf = by_month[m]
        lines.append(f"| {m} | {n:,} | {nf:,} | {b / a:.2%} |")

    if F < 50:
        lines += ["", f"**Warning: only {F} flagged postings.** The expansion below rests on too "
                      "little text to say much. Options: widen the seed list, add the 2024 sources "
                      "(other countries, other boards) to the corpus, or lower --min-flagged-df."]
        print(f"WARNING: only {F} flagged postings")

    # ---- 2. TF-IDF expansion
    cand_rows = []
    if F >= 5:
        fl_texts = [texts[k] for k in flagged]
        oth_idx = [k for k in range(N) if k not in set(flagged)]
        oth_texts = [texts[k] for k in oth_idx]
        cv = CountVectorizer(ngram_range=(1, 3), lowercase=True, min_df=args.min_flagged_df,
                             token_pattern=r"(?u)\b[^\W\d_]{2,}\b")
        Xf = cv.fit_transform(fl_texts)                     # vocabulary from flagged postings only
        vocab = cv.get_feature_names_out()
        cv2 = CountVectorizer(ngram_range=(1, 3), lowercase=True, vocabulary=cv.vocabulary_,
                              token_pattern=r"(?u)\b[^\W\d_]{2,}\b", binary=True)
        Xo = cv2.transform(oth_texts)
        df_f = np.asarray((Xf > 0).sum(axis=0)).ravel()
        df_o = np.asarray(Xo.sum(axis=0)).ravel()
        n_f, n_o = Xf.shape[0], Xo.shape[0]
        # tf-idf in flagged postings: (1 + ln tf) * idf, idf over the whole corpus
        idf = np.log((N + 1) / (df_f + df_o + 1)) + 1
        Xf_s = Xf.astype(float).tocsr()
        Xf_s.data = 1 + np.log(Xf_s.data)
        mean_tfidf = np.asarray(Xf_s.sum(axis=0)).ravel() / n_f * idf
        a, b, c, d = df_f + .5, n_f - df_f + .5, df_o + .5, n_o - df_o + .5
        z = np.log(a / b) - np.log(c / d)
        z = z / np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)

        seed_rx = [rx for _, rx in lex]
        seed_forms = set()
        for row_ in read_lexicon(Path(args.seeds)):
            for form in [row_["term"]] + row_["variants"]:
                seed_forms.add(" ".join(re.split(r"[-\s+]+", form.lower())).strip())
        titles_f = [(rows[k]["item"].get("title") or "").strip().lower() for k in flagged]
        order = np.argsort(-z)
        kept = []
        for j in order:
            g = vocab[j]
            if not edge_ok(g) or z[j] <= 0:
                continue
            if any(rx.search(g) for rx in seed_rx) or seed_overlap(g, seed_forms):
                continue
            cand_rows.append((g, int(df_f[j]), int(df_o[j]), float(z[j]), float(mean_tfidf[j]), j))
            if len(cand_rows) >= args.top * 4:
                break

        # titles and snippets for the candidates (one pass over the flagged postings)
        out = []
        for g, dff, dfo, zz, mt, j in cand_rows:
            rx = re.compile(r"(?<!\w)" + re.escape(g) + r"(?!\w)", re.IGNORECASE)
            ts, ex = set(), ""
            for k, t in zip(flagged, fl_texts):
                if rx.search(t):
                    ts.add((rows[k]["item"].get("title") or "").strip().lower())
                    if not ex:
                        ex = context(t, rx.search(t).group(0))
            if len(ts) >= args.min_titles:
                out.append({"term": g, "n": len(g.split()), "df_flagged": dff, "df_other": dfo,
                            "z": round(zz, 2), "mean_tfidf": round(mt, 3), "titles": len(ts),
                            "example": ex})
        # a shorter n-gram wholly inside a longer one with almost the same flagged count is dropped
        out.sort(key=lambda r: (-r["n"], -r["df_flagged"]))
        final = []
        for r in out:
            if any(r["term"] in f["term"] and r["term"] != f["term"] and
                   f["df_flagged"] >= 0.8 * r["df_flagged"] for f in final):
                continue
            final.append(r)
        final.sort(key=lambda r: -r["z"])
        final = final[:args.top]
        OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=["term", "n", "df_flagged", "df_other", "z",
                                              "mean_tfidf", "titles", "example", "keep", "channel"])
            w.writeheader()
            for r in final:
                w.writerow({**r, "keep": "", "channel": ""})
        lines += ["", "## TF-IDF expansion", "",
                  f"Flagged postings {n_f:,}, other postings {n_o:,}. {len(final):,} candidate "
                  f"n-grams written to `{OUT_CSV}` (found in at least {args.min_flagged_df} flagged "
                  f"postings under at least {args.min_titles} distinct titles; ranked by z-score). "
                  "Top 25:", "",
                  "| Term | Flagged | Other | z | Mean TF-IDF | Titles |", "|---|---:|---:|---:|---:|---:|"]
        for r in final[:25]:
            lines.append(f"| {r['term']} | {r['df_flagged']} | {r['df_other']} | {r['z']} | "
                         f"{r['mean_tfidf']} | {r['titles']} |")
        lines += ["", "Read the list as candidates, not as findings. In a corpus dominated by a few "
                      "employers, an n-gram can be frequent in flagged postings because of who "
                      "posts them (boilerplate of one defence employer, say) and not because of "
                      "the concept. The `titles` column and the example snippet are there to help "
                      "you tell the difference."]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD}" + (f" and {OUT_CSV} ({len(final)} candidates)" if cand_rows else ""))
    print("Review the sheet: put 1 in `keep` and one channel in `channel` for each term to add.")


if __name__ == "__main__":
    main()
