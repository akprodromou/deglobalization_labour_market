"""
Month 3: find labelled postings whose label may change under the diversification definition of prompt v10, and apply the new labels.

Prompt v10 and guide: diversification = reducing dependence on a single supplier, country or technology provider (diversified
supplier base, dual sourcing, new partners and markets, sovereign AI and cloud capacity). Supplier diversification used to be
reshoring (guide, prompt v9); cybersecurity stays none.

  list:   python -m diagnostics.78_relabel_diversification list --sheet <labelled sheet> --corpus <files> --out relabel_<name>.csv
          Searches the FULL description of every labelled posting for the phrases below and lists the matches with the
          author's current label and a snippet. Columns channel_new and intensity_new are empty: fill them where the
          label should change (leave empty to keep it).
  apply:  python -m diagnostics.78_relabel_diversification apply --sheet <labelled sheet> --relabel relabel_<name>.csv
          Writes <sheet>_v10.csv with the new labels; score it with script 60 against tags made with prompt v10.
"""
import argparse
import csv
import re
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

PHRASES = re.compile(
    r"divers\w+ (?:of )?(?:the )?(?:our )?(?:supplier|supply|sourcing|source|vendor|partner|market)\w*|"
    r"(?:supplier|supply|vendor|source|sourcing) divers\w+|dual[- ]sourc\w+|multi[- ]sourc\w+|second[- ]source\w*|"
    r"alternative (?:supplier|source)s?|(?:single|sole)[- ](?:supplier|source)\w*|"
    r"(?:reduc\w+|less|lower|limit\w*) (?:our |the )?(?:dependen\w+|reliance)\b|dependen\w+ (?:on|upon) (?:the )?(?:us|u\.s\.|china|chinese|american|non-european|foreign|third[- ]countr\w+|a single)|"
    r"sovereign\w*|digital sovereignty|strategic autonomy|gigafactor\w+|eurohpc|gaia-x|secnumcloud|"
    r"new export markets?|free trade agreements?", re.I)


def norm(t):
    return re.sub(r"\s+", " ", t or "")


def cmd_list(a):
    desc = {}
    for p in a.corpus:
        rows, _ = load_corpus(Path(p))
        for r in rows:
            desc[str(r["item"]["id"])] = norm(r["item"].get("description"))
    rows = list(csv.DictReader(open(a.sheet, encoding="utf-8-sig")))
    out = []
    for r in rows:
        ch = (r.get("channel") or "").strip()
        if not ch or ch == "unclear":
            continue
        d = desc.get(r["posting_id"], norm(r.get("text")))
        ms = list(PHRASES.finditer(d))
        if not ms:
            continue
        m = ms[0]
        out.append({"item": r["item"], "posting_id": r["posting_id"], "title": r["title"],
                    "label_now": f'{ch} / {(r.get("intensity") or "").strip()}',
                    "phrases": "; ".join(sorted({x.group(0).lower() for x in ms})[:6]),
                    "snippet": d[max(0, m.start() - 160):m.end() + 160], "channel_new": "", "intensity_new": ""})
    with open(a.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()) if out else ["item"])
        w.writeheader()
        w.writerows(out)
    print(f"{len(out)} of {len(rows)} sheet rows match; written {a.out}")


def cmd_apply(a):
    rows = list(csv.DictReader(open(a.sheet, encoding="utf-8-sig")))
    rl = {r["posting_id"]: r for r in csv.DictReader(open(a.relabel, encoding="utf-8-sig"))}
    n = 0
    for r in rows:
        e = rl.get(r["posting_id"])
        if e and (e.get("channel_new") or "").strip():
            r["channel"] = e["channel_new"].strip()
            r["intensity"] = (e.get("intensity_new") or "").strip() or r["intensity"]
            n += 1
    p = Path(a.sheet)
    q = p.with_name(p.stem + "_v10.csv")
    with open(q, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{n} labels changed; written {q}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument("--sheet", required=True)
    l.add_argument("--corpus", nargs="+", required=True)
    l.add_argument("--out", required=True)
    p = sub.add_parser("apply")
    p.add_argument("--sheet", required=True)
    p.add_argument("--relabel", required=True)
    a = ap.parse_args()
    {"list": cmd_list, "apply": cmd_apply}[a.cmd](a)


if __name__ == "__main__":
    main()
