"""
Month 3, step 6: what lies behind the December 2025 defense peak?

Weighted posting counts jump from 3,618 (Nov 2025) to 28,639 (Dec 2025) and to 48,511 (Jan 2026),
after a year of low volume, and the defense-tagged share reaches 6.4% in December 2025 (3.4% in
December 2024, which also rose from November). Before a peak is read as an effect of EDIP, three
things are checked here, for BOTH winters (Nov 2024 to Jan 2025 and Nov 2025 to Jan 2026):

  1. Volume by week: postings in the population (day weights), postings taken, flagged share,
     defense-tagged share. A step in volume at the same week as a step in the defense share points to
     a change in what the corpus ingests, not in demand.
  2. Employers: the employer is the text after the last " - " in the posting's title (the Tracker's titles
     end with the employer's name). For December 2024 and December 2025 the report lists the employers
     with most defense-tagged postings (weighted), how concentrated the defense postings are (top 1,
     top 5, number of employers), and the employers with most postings of any kind.
  3. Sensitivity: the December defense share again after leaving out the postings of the top 1, 3 and 5
     defense employers of that December. If the peak vanishes, it is a few employers' hiring wave
     (which may still be real, but is not the whole labour market).

Postings are those of the day-stratified corpus with the day weights of corpus_io (duplicates removed,
all files read as one corpus). "Defense-tagged" = tagged with the defense channel by the model; the
lexicon-only reading (a defense-channel term found) is shown beside it.

Run (project root, venv active; same corpus files as script 64):
    python -m diagnostics.66_december_diagnostics \\
        --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl \\
                 data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl \\
        --flagged data/tagged/flagged_corpus_jobbland.se_2024-01_2026-09.jsonl \\
        --tags data/tagged/tags_qwen2.5_7b_tagging_v8.jsonl
Writes docs/december_diagnostics.md (employer names of public and private bodies, no personal data) and
data/tagged/daily_volume_winters.csv.
"""

import argparse
import csv
import json
import tempfile
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

WINTERS = [("2024-11-01", "2025-01-31"), ("2025-11-01", "2026-01-31")]
DECEMBERS = ["2024-12", "2025-12"]


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


def employer(title):
    t = (title or "").strip()
    return t.rsplit(" - ", 1)[-1].strip() if " - " in t else "(no employer in title)"


def monday(day):
    d = date.fromisoformat(day)
    return (d - timedelta(days=d.weekday())).isoformat()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--flagged", required=True)
    ap.add_argument("--lexicon", default="lexicon/lexicon.csv")
    ap.add_argument("--tags", required=True)
    ap.add_argument("--out-md", default="docs/december_diagnostics.md")
    ap.add_argument("--out-csv", default="data/tagged/daily_volume_winters.csv")
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()

    rows, dup = load_all(args.corpus)
    chan_of = {r["term"]: r["channel"] for r in csv.DictReader(open(args.lexicon, encoding="utf-8-sig"))}
    flagged = {}
    for line in open(args.flagged, encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            flagged[str(r["posting_id"])] = r["terms"]
    tag = {}
    for line in open(args.tags, encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            tag[str(r["posting_id"])] = r["channel"] if r.get("ok") else None

    n_day = Counter(r["day"] for r in rows)
    recs = []
    for r in rows:
        pid = str(r["item"]["id"])
        terms = flagged.get(pid, [])
        recs.append({
            "day": r["day"], "w": r["w"], "emp": employer(r["item"].get("title")),
            "flag": bool(terms),
            "lex_def": any(chan_of.get(t) == "defense" for t in terms),
            "tag_def": tag.get(pid) == "defense",
        })
    print(f"{len(recs):,} postings after removing {dup:,} duplicates")

    def share(sel, key):
        pop = sum(x["w"] for x in sel)
        return (sum(x["w"] for x in sel if x[key]) / pop) if pop else float("nan")

    L = ["# December 2025 defense peak: volume and employers", "",
         "Weights are the day weights of the corpus. Employer = text after the last ' - ' in the title. "
         "Defense-tagged = tagged defense by the model; lexicon = a defense-channel term was found.", ""]

    # 1. volume by week and daily csv
    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["day", "postings_taken", "population", "flagged_share", "defense_tagged_share"])
        for a, b in WINTERS:
            for d in sorted({x["day"] for x in recs if a <= x["day"] <= b}):
                sel = [x for x in recs if x["day"] == d]
                wr.writerow([d, len(sel), round(sum(x["w"] for x in sel)),
                             round(share(sel, "flag"), 5), round(share(sel, "tag_def"), 5)])
    for a, b in WINTERS:
        L += [f"## Volume by week, {a} to {b}", "",
              "| Week starting | Postings taken | Population | Flagged share (%) | Defense-tagged share (%) | Defense, lexicon only (%) |",
              "|---|---:|---:|---:|---:|---:|"]
        weeks = defaultdict(list)
        for x in recs:
            if a <= x["day"] <= b:
                weeks[monday(x["day"])].append(x)
        for wk in sorted(weeks):
            s = weeks[wk]
            L.append(f"| {wk} | {len(s):,} | {sum(x['w'] for x in s):,.0f} | {100*share(s,'flag'):.1f} | "
                     f"{100*share(s,'tag_def'):.1f} | {100*share(s,'lex_def'):.1f} |")
        L.append("")

    # 2 and 3. employers in each December
    for ym in DECEMBERS:
        sel = [x for x in recs if x["day"][:7] == ym]
        pop = sum(x["w"] for x in sel)
        dsel = [x for x in sel if x["tag_def"]]
        dpop = sum(x["w"] for x in dsel)
        by_emp = Counter()
        n_emp = Counter()
        for x in dsel:
            by_emp[x["emp"]] += x["w"]
            n_emp[x["emp"]] += 1
        ranked = by_emp.most_common()
        top = lambda k: sum(w for _, w in ranked[:k]) / dpop if dpop else float("nan")
        L += [f"## {ym}: defense-tagged postings and their employers", "",
              f"Postings taken {len(sel):,}, population about {pop:,.0f}; defense-tagged: {len(dsel)} taken, about {dpop:,.0f} in the population "
              f"({100*dpop/pop:.2f}% of all postings); {len(ranked)} distinct employers. Top employer holds {100*top(1):.0f}% of the weighted "
              f"defense postings, the top 5 hold {100*top(5):.0f}%.", "",
              "| Employer | Defense-tagged taken | Weighted share of defense postings (%) |", "|---|---:|---:|"]
        for e, w in ranked[:args.top]:
            L.append(f"| {e} | {n_emp[e]} | {100*w/dpop:.1f} |")
        L += ["", f"Sensitivity: the December defense-tagged share (% of all postings) without the postings of the top 1, 3 and 5 defense employers:", "",
              "| Left out | Defense-tagged share (%) |", "|---|---:|", f"| nobody | {100*dpop/pop:.2f} |"]
        for k in (1, 3, 5):
            drop = {e for e, _ in ranked[:k]}
            keep = [x for x in sel if x["emp"] not in drop]
            L.append(f"| top {k} | {100*share(keep, 'tag_def'):.2f} |")
        allemp = Counter()
        for x in sel:
            allemp[x["emp"]] += x["w"]
        L += ["", f"Employers with the most postings of any kind in {ym} (weighted share of all postings):", "",
              "| Employer | Share of all postings (%) |", "|---|---:|"]
        for e, w in allemp.most_common(args.top):
            L.append(f"| {e} | {100*w/pop:.1f} |")
        L.append("")

    # employers that grew most between the two Decembers (defense-tagged)
    def dweights(ym):
        c = Counter()
        sel = [x for x in recs if x["day"][:7] == ym]
        pop = sum(x["w"] for x in sel)
        for x in sel:
            if x["tag_def"]:
                c[x["emp"]] += x["w"] / pop
        return c
    a, b = dweights(DECEMBERS[0]), dweights(DECEMBERS[1])
    diff = sorted(((b[e] - a[e], e) for e in set(a) | set(b)), reverse=True)
    L += ["## Employers behind the change in the defense-tagged share, December 2024 to December 2025", "",
          "Contribution to the change, in percentage points of all postings (sums to the total change).", "",
          "| Employer | Dec 2024 (%) | Dec 2025 (%) | Contribution (points) |", "|---|---:|---:|---:|"]
    for d, e in diff[:args.top]:
        L.append(f"| {e} | {100*a[e]:.2f} | {100*b[e]:.2f} | {100*d:+.2f} |")
    L.append(f"| all employers | {100*sum(a.values()):.2f} | {100*sum(b.values()):.2f} | {100*(sum(b.values())-sum(a.values())):+.2f} |")
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text("\n".join(L), encoding="utf-8")
    print(f"Wrote {args.out_md} and {args.out_csv}")


if __name__ == "__main__":
    main()
