"""
Month 3: ignore the lexicon term "defense" where it means the defense of a doctoral thesis.

"has documented research work after a defense", "for the position of chief physician, a public defense is also required",
"doctoral defense", "thesis defense" are university and hospital ads, not defense-sector ads. The bare term "defense" matches them.

Rule, applied to every flagged posting that has "defense" among its terms (the text is the one the flagger searched: title plus
description without boilerplate, first 6,000 characters). An occurrence of "defense" is ACADEMIC if
  A. it is directly preceded by public / doctoral / thesis / dissertation / PhD / licentiate / doctorate (at most one word in between,
     no punctuation), or by "after a(n)/the", or is directly followed by "of (a/the/his/her) thesis/dissertation/doctoral ...", or
  B. one of doctoral, doctorate, doctor of, thesis, dissertation, PhD, licentiate, disputation lies within 60 characters and
     the next word is not a defense-sector noun (industry, sector, forces, materiel, authority, systems, ...).
If EVERY occurrence of "defense" in the posting is academic, the term "defense" is removed from its `terms`.
  * no term left -> the posting is no longer flagged and its tag is dropped (it counts as `none` in scripts 64 and 65);
  * terms left   -> the tag is dropped so that script 58 tags the posting again with the shorter term list
                    (with --keep-changed the old tag is kept and only its `terms` field is updated).
A review file lists every affected posting with the snippet, so that you can read a sample before you accept the rule.

Run (project root):
    python -m diagnostics.75_phd_defense_rule --corpus data/raw/corpus_....jsonl [more files] \\
        --flagged data/tagged/flagged_....jsonl --tags data/tagged/tags_qwen2.5_7b_tagging_v9.jsonl
Both files are copied first to *.before_phd (never overwritten) and then rewritten in place.
Afterwards: script 58 again (same command, no --refresh), then 71, 64, 65.
"""
import argparse
import csv
import json
import re
import shutil
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus, posting_text
    from diagnostics.lexicon_io import term_regex
except ImportError:
    from corpus_io import load_corpus, posting_text
    from lexicon_io import term_regex

SEARCH_CHARS = 6000
TERM = "defense"
DEF_RX = re.compile(term_regex(TERM, "en"), re.I)
ACADEMIC = r"(?:public|doctoral|doctorate|thesis|dissertation|ph\.?d|licentiate)"
BEFORE_RX = re.compile(r"(?:" + ACADEMIC + r"[ \-]+(?:\w+[ \-]+)?|after[ \-]+(?:an?|the)[ \-]+)$", re.I)
AFTER_RX = re.compile(r"^\W*(?:of|for)\W+(?:(?:an?|the|his|her|their|your)\W+)?(?:thesis|dissertation|doctoral|doctorate|phd)", re.I)
NEAR_RX = re.compile(r"\b(?:doctoral|doctorate|doctor of|thesis|theses|dissertation|ph\.?d|licentiate|disputation)\b", re.I)
SECTOR_NEXT = re.compile(r"^\W*(?:industry|industries|sector|forces?|materiel|authority|authorities|agency|agencies|systems?|"
                         r"company|companies|contractors?|equipment|procurement|capabilit\w+|research institute|and security|"
                         r"policy|ministry|logistics|facilities|secrecy|products?|programmes?|programs?)\b", re.I)


def academic(text, m):
    before, after = text[max(0, m.start() - 60):m.start()], text[m.end():m.end() + 60]
    if SECTOR_NEXT.search(after):                    # "PhD in defense industry", "defense systems": the sector, not the thesis
        return ""
    if BEFORE_RX.search(before) or AFTER_RX.search(after):
        return "A"
    if NEAR_RX.search(before + " " + after):
        return "B"
    return ""


def classify(text):
    """('all', snippet, rules) if every occurrence of the term is academic; ('some'|'none', ...) otherwise."""
    ms = list(DEF_RX.finditer(text))
    if not ms:
        return "none", "", ""
    rules = [academic(text, m) for m in ms]
    snip = re.sub(r"\s+", " ", text[max(0, ms[0].start() - 90):ms[0].end() + 90])
    return ("all" if all(rules) else "some"), snip, "".join(sorted(set(r for r in rules if r)))


def read_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--flagged", required=True)
    ap.add_argument("--tags", required=True)
    ap.add_argument("--review", default="phd_defense_review.csv")
    ap.add_argument("--keep-changed", action="store_true")
    a = ap.parse_args()

    fp, tp = Path(a.flagged), Path(a.tags)
    for p in (fp, tp):
        b = p.with_name(p.name + ".before_phd")
        if not b.exists():
            shutil.copy(p, b)
            print("backup:", b)

    flagged = read_jsonl(fp)
    want = {str(r["posting_id"]) for r in flagged if TERM in r["terms"]}
    text_of, title_of = {}, {}
    for p in a.corpus:
        rows, _ = load_corpus(Path(p))
        for r in rows:
            pid = str(r["item"]["id"])
            if pid in want and pid not in text_of:
                text_of[pid] = posting_text(r["item"], SEARCH_CHARS)
                title_of[pid] = (r["item"].get("title") or "").strip()
    missing = len(want - set(text_of))

    status, review = {}, []
    new_flagged = []
    for r in flagged:
        pid = str(r["posting_id"])
        if pid in text_of and TERM in r["terms"]:
            k, snip, rules = classify(text_of[pid])
            if k == "all":
                t = [x for x in r["terms"] if x != TERM]
                status[pid] = "dropped" if not t else "changed"
                review.append({"posting_id": pid, "title": title_of[pid], "result": status[pid], "rule": rules,
                               "other_terms": "; ".join(t), "snippet": snip})
                if t:
                    new_flagged.append({**r, "terms": t})
                continue
        new_flagged.append(r)
    with open(fp, "w", encoding="utf-8") as f:
        for r in new_flagged:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(a.review, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["posting_id", "title", "result", "rule", "other_terms", "snippet"])
        w.writeheader()
        w.writerows(review)

    tags = read_jsonl(tp)
    out, n_drop, n_retag, by_ch = [], 0, 0, {}
    for t in tags:
        s = status.get(str(t["posting_id"]))
        if s == "dropped":
            n_drop += 1
            by_ch[t.get("channel")] = by_ch.get(t.get("channel"), 0) + 1
        elif s == "changed" and not a.keep_changed:
            n_retag += 1
        else:
            if s == "changed":
                t = {**t, "terms": [x for x in t["terms"] if x != TERM]}
            out.append(t)
    with open(tp, "w", encoding="utf-8") as f:
        for t in out:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")

    nd, nc = sum(v == "dropped" for v in status.values()), sum(v == "changed" for v in status.values())
    print(f"flagged postings with the term '{TERM}': {len(want):,} ({missing} not found in the corpus)")
    print(f"flagged: {len(flagged):,} -> {len(new_flagged):,} ({nd:,} no longer flagged, {nc:,} lose the term)")
    print(f"tags: {len(tags):,} -> {len(out):,}; dropped with their posting: {n_drop:,} {by_ch}; to tag again: {n_retag:,}")
    print("review file:", a.review, "(read about 30 rows before accepting the rule)")


if __name__ == "__main__":
    main()
