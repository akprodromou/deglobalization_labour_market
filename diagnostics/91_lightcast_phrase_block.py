"""
Month 4, step 3: Lightcast phrase block for the occupation clustering (extra block of input D), ONE board per run.

What it does. Every posting's full text (title and description, boilerplate removed, via corpus_io.posting_text, the
same text as script 69b) is searched for the SELECTED terms of lexicon/lightcast_block_terms.csv (the author's Lightcast
list: Section 1 supply chain and logistics, plus battery, semiconductor, space and electronics terms of Section 3;
Section 2 and the general manufacturing terms are in the file but not selected). Matching is exact phrase matching:
lower case, hyphens and slashes read as spaces, parentheses removed ("Kinaxis (Software)" -> "kinaxis"), whole words,
an optional plural -s / -es at the end. Terms are matched independently, so "supply chain" is also counted inside
"supply chain management". An acronym is NOT added as a variant (too many false hits).

This is a separate block, like the Tracker skills: it is never mixed into the ESCO skill vectors, and it is NOT a
channel tag or part of lexicon v7 (frozen). It only gives the clustering words for topics where ESCO is weak
(battery production, semiconductor fabrication, space manufacturing, supply-chain risk).

Output, per board:
    data/tagged/lightcast_block_<label>.jsonl   {"id", "day", "terms": [selected terms found]}   (all postings, empty list if none)
    docs/lightcast_block_<label>.md             postings per term (unweighted) with 3 contexts to read, share of postings with
                                                at least one term, by group
Run (project root; no GPU, no extra package; one board per run):
    python -m diagnostics.91_lightcast_phrase_block --corpus <the board's corpus files> --label jobbland
Options: --terms lexicon/lightcast_block_terms.csv   --limit N (test)
"""

import argparse
import csv
import json
import re
import tempfile
from collections import defaultdict
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus, posting_text
except ImportError:
    from corpus_io import load_corpus, posting_text

FULL = 10 ** 9


def norm(s):
    s = (s or "").lower()
    s = re.sub(r"[-‐-―/]", " ", s)
    return re.sub(r"\s+", " ", s)


def term_key(term):
    t = re.sub(r"\([^)]*\)", " ", term)          # drop parentheses and what is inside
    return norm(t).strip()


def load_terms(path):
    terms = {}                                    # key -> (term as written, group)
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        if str(r["selected"]).strip() == "1":
            k = term_key(r["term"])
            if k:
                terms.setdefault(k, (r["term"], r["group"]))
    return terms


def make_rx(key):
    return re.compile(r"(?<![a-z0-9])" + re.escape(key) + r"(?:s|es)?(?![a-z0-9])")


def find_terms(text, rxs):
    found = {}
    for key, rx in rxs.items():
        if key in text:                            # cheap substring test first
            m = rx.search(text)
            if m:
                found[key] = m
    return found


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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--terms", default="lexicon/lightcast_block_terms.csv")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    terms = load_terms(args.terms)
    rxs = {k: make_rx(k) for k in terms}
    rows, dup = load_all(args.corpus)
    if args.limit:
        rows = rows[:args.limit]
    out = Path(f"data/tagged/lightcast_block_{args.label}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    count = defaultdict(int)
    ctx = defaultdict(list)
    grp_any = defaultdict(int)
    any_term = 0
    with open(out, "w", encoding="utf-8") as f:
        for i, r in enumerate(rows):
            text = norm(posting_text(r["item"], FULL))
            found = find_terms(text, rxs)
            for k, m in found.items():
                count[k] += 1
                if len(ctx[k]) < 3:
                    a, b = max(0, m.start() - 70), min(len(text), m.end() + 70)
                    ctx[k].append(text[a:b])
            if found:
                any_term += 1
                for g in {terms[k][1] for k in found}:
                    grp_any[g] += 1
            f.write(json.dumps({"id": str(r["item"]["id"]), "day": r["day"],
                                "terms": sorted(terms[k][0] for k in found)}, ensure_ascii=False) + "\n")
            if (i + 1) % 10000 == 0:
                print(f"  {i+1:,}/{len(rows):,}")
    n = len(rows)
    md = [f"# Lightcast phrase block: {args.label}", "",
          f"{n:,} postings after removing {dup:,} duplicates; {len(terms)} selected terms. Terms found in {any_term:,} postings "
          f"({any_term/max(1,n):.1%}); unweighted counts.", "", "Postings with at least one term, by group (a posting can be in several):", ""]
    md += [f"- {g}: {c:,} ({c/max(1,n):.1%})" for g, c in sorted(grp_any.items(), key=lambda x: -x[1])]
    md += ["", "## Postings per term, with three contexts to read", ""]
    for k, c in sorted(count.items(), key=lambda x: -x[1]):
        md.append(f"### {terms[k][0]} ({terms[k][1]}): {c:,} postings")
        md += [f"- {x}" for x in ctx[k]]
        md.append("")
    silent = sorted(terms[k][0] for k in terms if k not in count)
    md += [f"## Terms with no posting ({len(silent)})", "", ", ".join(silent), ""]
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/lightcast_block_{args.label}.md").write_text("\n".join(md), encoding="utf-8")
    print(f"{n:,} postings ({dup:,} duplicates removed); terms found in {any_term:,} postings -> {out}, docs/lightcast_block_{args.label}.md")


if __name__ == "__main__":
    main()
