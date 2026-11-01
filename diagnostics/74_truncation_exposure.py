"""
Month 3: which annotated postings may have been labelled without seeing the text that made the lexicon flag them?

The annotation sheets (script 59) show the first 1,800 characters of the description; the tagger reads the first 3,000
characters plus passages around matched terms that lie further in. A human label can therefore miss a defense (or other)
reference that stands late in the ad. This script finds those rows and lets you check them against the full text.

  Step 1  list:   python -m diagnostics.74_truncation_exposure list --sheet <filled sheet> --corpus <corpus files> --out exposure.csv
          For every labelled row it looks for the sheet's `terms_found` in the full description and writes the rows where
          NONE of the terms is inside the visible 1,800 characters (class "hidden") or only some are ("partly"), with the
          late passages. Columns `channel_full` and `intensity_full` are empty: fill them for the rows you want to relabel
          after reading the full text (leave empty to keep the old label).
  Step 2  apply:  python -m diagnostics.74_truncation_exposure apply --sheet <filled sheet> --exposure exposure.csv [more files]
          Writes <sheet>_full.csv (your new labels where you gave one) and <sheet>_visible_only.csv (hidden and partly rows
          unlabelled, so script 60 leaves them out). Score each with script 60 and compare with the original.

The counts printed by `list` answer the question: how many of the labelled rows could have been affected.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
    from diagnostics.lexicon_io import term_regex
except ImportError:
    from corpus_io import load_corpus
    from lexicon_io import term_regex

VISIBLE = 1800


def norm(desc):
    return re.sub(r"\s+", " ", desc or "")


def first_pos(term, text):
    m = re.search(term_regex(term, "en"), text, re.I)
    return m.start() if m else None


def passage(text, pos, w=220):
    return text[max(0, pos - w):pos + w].strip()


def cmd_list(a):
    desc = {}
    for p in a.corpus:
        rows, _ = load_corpus(Path(p))
        for r in rows:
            desc[str(r["item"]["id"])] = norm(r["item"].get("description"))
    rows = list(csv.DictReader(open(a.sheet, encoding="utf-8-sig")))
    lab = [r for r in rows if (r.get("channel") or "").strip()]
    skip = set()
    for sk in a.skip:                               # rows already listed (and possibly filled) in an earlier exposure file
        skip |= {r["posting_id"] for r in csv.DictReader(open(sk, encoding="utf-8-sig"))}
    if skip:
        print(f"{len(skip)} rows from --skip files are left out of this list")
    out, n_long, missing = [], 0, 0
    for r in lab:
        d = desc.get(r["posting_id"])
        if r["posting_id"] in skip:
            continue
        if d is None:
            missing += 1
            continue
        n_long += len(d) > VISIBLE
        terms = [t.strip() for t in r["terms_found"].split(";") if t.strip()]
        pos = {t: first_pos(t, d) for t in terms}
        vis = [t for t, p in pos.items() if p is not None and p < VISIBLE]
        late = [t for t, p in pos.items() if p is not None and p >= VISIBLE]
        if not late:
            continue
        cls = "partly" if vis else "hidden"
        out.append({"item": r["item"], "posting_id": r["posting_id"], "title": r["title"], "class": cls,
                    "label_now": f'{r["channel"].strip()} / {(r.get("intensity") or "").strip()}',
                    "terms_visible": "; ".join(vis), "terms_only_late": "; ".join(late),
                    "late_passages": "  [...]  ".join(passage(d, pos[t]) for t in late[:3]),
                    "length": len(d), "channel_full": "", "intensity_full": ""})
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()) if out else ["item"])
        w.writeheader()
        w.writerows(out)
    h = sum(o["class"] == "hidden" for o in out)
    print(f"labelled rows: {len(lab)} ({missing} not found in the corpus); description longer than {VISIBLE} characters: {n_long}")
    print(f"rows with a matched term only after character {VISIBLE}: hidden {h} (no matched term visible), partly {len(out) - h}")
    print("written:", a.out)


def cmd_apply(a):
    rows = list(csv.DictReader(open(a.sheet, encoding="utf-8-sig")))
    ex = {}
    for path in a.exposure:
        for r in csv.DictReader(open(path, encoding="utf-8-sig")):
            ex[r["posting_id"]] = r
    fields = list(rows[0].keys())
    full, vis = [], []
    n_rel = 0
    for r in rows:
        e = ex.get(r["posting_id"])
        f_, v_ = dict(r), dict(r)
        if e:
            v_["channel"] = v_["intensity"] = ""
            if (e.get("channel_full") or "").strip():
                f_["channel"] = e["channel_full"].strip()
                f_["intensity"] = (e.get("intensity_full") or "").strip() or f_["intensity"]
                n_rel += 1
        full.append(f_)
        vis.append(v_)
    stem = Path(a.sheet)
    for name, data in (("_full", full), ("_visible_only", vis)):
        p = stem.with_name(stem.stem + name + ".csv")
        with open(p, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(data)
        print("written:", p)
    print(f"relabelled rows: {n_rel}; rows left out of the visible-only sheet: {len(ex)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument("--sheet", required=True)
    l.add_argument("--corpus", nargs="+", required=True)
    l.add_argument("--out", default="exposure.csv")
    l.add_argument("--skip", nargs="*", default=[], help="earlier exposure file(s): their rows are not listed again")
    p = sub.add_parser("apply")
    p.add_argument("--sheet", required=True)
    p.add_argument("--exposure", nargs="+", required=True, help="one or more filled exposure files")
    a = ap.parse_args()
    {"list": cmd_list, "apply": cmd_apply}[a.cmd](a)


if __name__ == "__main__":
    main()
