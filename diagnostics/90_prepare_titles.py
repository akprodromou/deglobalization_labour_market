"""
Month 4, step 2: clean the posting titles (input A of the occupation clustering) for ONE board.

What is removed, and nothing else:
  * gender markers: (m/f/d), (m/w/d), (H/F), (F/H), M/F, F/M ...
  * a leading reference code that contains a digit and a hyphen (e.g. "RA-d2m-122 Innovation Coordinator")
  * a trailing reference code (IRC207099, 2024-112135, HT2025PM0103) and single (m)/(w) markers
  * trailing segments after a spaced separator (" - ", " | ", en dash) that look like an employer or a place:
      - the segment ends with a company-form word (AB, GmbH, AG, SAS, SARL, SA, Oy, AS, Inc, Ltd, LLC, KG, SE)
      - or contains municipality, kommun, region, county, university, universitet, hospital, group, groupe
      - or contains a comma (a place list such as "Fontenay-Sous-Bois, Ile de France, France")
      - or equals a word of the posting's own location field
    * or is a last segment that ends >= 25 titles of the same board (employers without a legal form, e.g. GlobalLogic)
    A segment starting with a digit ("75 - 100%") is never dropped.
    The first segment is always kept, and a segment that matches none of these is kept (so "GenAi - Manager / Consultant
    Senior" keeps its content). Hyphens inside words are never touched (only SPACED separators split).
Titles are NOT translated: the next step uses multilingual-e5, which reads Swedish, German and French titles.

Output: data/tagged/titles_<label>.jsonl, one line per posting (duplicates removed as in the tagger):
  {"id", "day", "title", "title_clean", "has_title", "desc_start"}   desc_start = first 150 characters of the description,
used only as a fallback text for postings without a title.
The report lists the share of titles that changed and 25 random before/after pairs to check by eye.

Run (project root, one board per run):
    python -m diagnostics.90_prepare_titles --corpus <the board's corpus files> --label jobbland
Writes data/tagged/titles_<label>.jsonl and docs/titles_<label>.md
"""

import argparse
import json
import random
import re
import tempfile
import unicodedata
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

G = r"[mwfhdx]"
GENDER_RX = re.compile(rf"\(?\s*(?<![A-Za-z]){G}\s*[/|]\s*{G}(?:\s*[/|]\s*{G})?(?![A-Za-z])\s*\)?", re.I)
SINGLE_G_RX = re.compile(r"\(\s*[mwfd]\s*\)", re.I)
TRAIL_CODE_RX = re.compile(r"\s*\(?\b(?:[A-Z]{2,4}\d{5,}|[A-Z]{1,3}\d{4}[A-Z]{1,3}\d{3,}|\d{4}-\d{4,})\b\)?\s*$")
REF_RX = re.compile(r"^\s*(?=\S*\d)[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+\s+")
SEP_RX = re.compile(r"\s+[-–—|]\s+")
FORM_RX = re.compile(r"\b(ab|aktiebolag|gmbh|ag|sas|sarl|sa|oy|as|inc|ltd|llc|kg|se)\.?$", re.I)
WORD_RX = re.compile(r"\b(municipality|kommun|region|county|university|universitet|hospital|group|groupe)\b", re.I)


def clean_title(title, location="", employers=frozenset()):
    t = unicodedata.normalize("NFKC", title or "")
    t = re.sub(r"\s+", " ", t).strip()
    if not t:
        return ""
    t = GENDER_RX.sub(" ", t)
    t = SINGLE_G_RX.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip(" -–—|,;:")
    t = REF_RX.sub("", t)
    loc_words = {w.lower() for w in re.findall(r"[^\W\d_]{4,}", location or "")}
    segs = SEP_RX.split(t)
    keep = [segs[0]]
    for s in segs[1:]:
        s = s.strip()
        if s[:1].isdigit():  # "75 - 100%, ..." : a percentage range, not an employer
            keep.append(s)
            continue
        drop = (s.lower() in employers or FORM_RX.search(s) or WORD_RX.search(s) or "," in s or s.lower() in loc_words
                or (loc_words and {w.lower() for w in re.findall(r"[^\W\d_]{4,}", s)} and
                    {w.lower() for w in re.findall(r"[^\W\d_]{4,}", s)} <= loc_words))
        if not drop:
            keep.append(s)
    out = " - ".join(keep)
    out = TRAIL_CODE_RX.sub("", out)
    out = re.sub(r"\s+", " ", out).strip(" -–—|,;:").rstrip(" .")
    return out or re.sub(r"\s+", " ", title or "").strip()


def frequent_suffixes(titles, min_count=25):
    """Last spaced segments that end >= min_count titles of the board: employers without a legal-form word
    (GlobalLogic, Omegapoint ...), and place names. Data-driven, so no employer list is needed."""
    from collections import Counter
    c = Counter()
    for t in titles:
        segs = SEP_RX.split(re.sub(r"\s+", " ", t or "").strip())
        if len(segs) > 1 and not segs[-1][:1].isdigit():
            c[segs[-1].strip().lower()] += 1
    return frozenset(k for k, v in c.items() if v >= min_count and len(k) > 1)


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
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    rows, dup = load_all(args.corpus)
    out = Path(f"data/tagged/titles_{args.label}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    employers = frequent_suffixes([(r["item"].get("title") or "") for r in rows])
    recs = []
    for r in rows:
        it = r["item"]
        t = (it.get("title") or "").strip()
        c = clean_title(t, it.get("location") or "", employers)
        recs.append({"id": str(it["id"]), "day": r["day"], "title": t, "title_clean": c, "has_title": bool(t),
                     "desc_start": re.sub(r"\s+", " ", (it.get("description") or ""))[:150].strip()})
    with open(out, "w", encoding="utf-8") as f:
        for x in recs:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    n = len(recs)
    titled = [x for x in recs if x["has_title"]]
    changed = [x for x in titled if x["title_clean"] != re.sub(r"\s+", " ", x["title"]).strip()]
    random.seed(args.seed)
    sample = random.sample(changed, min(25, len(changed)))
    md = [f"# Title cleaning: {args.label}", "",
          f"{n:,} postings after removing {dup:,} duplicates; {n-len(titled):,} without a title; "
          f"{len(changed):,} titles changed ({len(changed)/max(1,len(titled)):.1%} of the titled ones).", "",
          "## 25 random before / after pairs (changed titles only)", ""]
    md += [f"- `{x['title']}`  ->  `{x['title_clean']}`" for x in sample]
    md += ["", f"## {len(employers)} frequent trailing segments removed as employers/places (>= 25 titles)", ""]
    md += [f"- {e}" for e in sorted(employers)[:60]]
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/titles_{args.label}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{n:,} postings ({dup:,} duplicates removed); {n-len(titled):,} without a title; "
          f"{len(changed):,} titles changed -> {out}, docs/titles_{args.label}.md")


if __name__ == "__main__":
    main()
