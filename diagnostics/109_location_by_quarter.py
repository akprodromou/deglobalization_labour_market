"""
Month 4: why is the unplaced share of a board high in some quarters? Per quarter (calendar quarter of the sampled day), the postings by
the method script 96 used to place them (field, county, learned, manual, gazetteer) or the reason they were not placed (vague,
unmatched, outside, not in the nuts2 file), as counts and as weighted shares, plus the largest location strings among the unplaced
postings of the worst quarters and the share of postings with an empty location.
Reads data/tagged/nuts2_<label>.jsonl (script 96) and the corpus (day, weight, location), duplicates removed as in script 93.
Output: docs/location_by_quarter_<label>.md
Run (project root, venv active), jobbland:
    python -m diagnostics.109_location_by_quarter --label jobbland --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl
"""
import argparse
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path


def load_all(paths):
    try:
        from diagnostics.corpus_io import load_corpus
    except ImportError:
        from corpus_io import load_corpus
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


def quarter(day):
    y, m = int(day[:4]), int(day[5:7])
    return f"{y}-Q{(m - 1) // 3 + 1}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--nuts")
    ap.add_argument("--worst", type=int, default=3, help="number of quarters with the highest unplaced share whose locations are listed")
    ap.add_argument("--show", type=int, default=15)
    a = ap.parse_args()
    nuts_p = a.nuts or f"data/tagged/nuts2_{a.label}.jsonl"
    meth, code = {}, {}
    for l in open(nuts_p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            meth[str(r["id"])] = r.get("method") or "?"
            code[str(r["id"])] = r.get("nuts2")
    rows, _ = load_all(a.corpus)
    n = defaultdict(Counter)
    w = defaultdict(lambda: defaultdict(float))
    empty = defaultdict(int)
    tot = defaultdict(int)
    wtot = defaultdict(float)
    unpl_loc = defaultdict(Counter)
    for r in rows:
        pid = str(r["item"]["id"])
        q = quarter(r["day"])
        loc = (r["item"].get("location") or "").strip()
        m = meth.get(pid, "not in the nuts2 file")
        placed = bool(code.get(pid))
        label = m if placed else (m if m in ("vague", "unmatched", "outside") else "not in the nuts2 file" if pid not in meth else m + " (no code)")
        n[q][label] += 1
        w[q][label] += r["w"]
        tot[q] += 1
        wtot[q] += r["w"]
        if not loc:
            empty[q] += 1
        if not placed:
            unpl_loc[q][loc[:60] or "(empty)"] += 1
    qs = sorted(tot)
    labels = sorted({k for q in qs for k in n[q]})
    unpl_share = {q: sum(w[q][k] for k in labels if k in ("vague", "unmatched", "outside", "not in the nuts2 file") or "(no code)" in k) / wtot[q] for q in qs}
    md = [f"# Location and NUTS-2 placement by quarter: {a.label}", "",
          f"{sum(tot.values()):,} postings after duplicates. Method of script 96 per posting; 'not in the nuts2 file' means the id has no row in {nuts_p} (script 96 was run on a corpus that did not hold it).", "",
          "## Postings taken by method (counts)", "", "| quarter | taken | empty location | " + " | ".join(labels) + " |", "|---|---|---|" + "---|" * len(labels)]
    for q in qs:
        md.append(f"| {q} | {tot[q]} | {empty[q]} | " + " | ".join(str(n[q][k]) for k in labels) + " |")
    md += ["", "## Weighted share by method", "", "| quarter | unplaced (weighted) | " + " | ".join(labels) + " |", "|---|---|" + "---|" * len(labels)]
    for q in qs:
        md.append(f"| {q} | {unpl_share[q]:.0%} | " + " | ".join(f"{w[q][k] / wtot[q]:.0%}" for k in labels) + " |")
    for q in sorted(qs, key=lambda x: -unpl_share[x])[: a.worst]:
        md += ["", f"## Largest locations among the unplaced postings of {q} (unplaced share {unpl_share[q]:.0%})", "", "| location | postings |", "|---|---|"]
        md += [f"| {k} | {v} |" for k, v in unpl_loc[q].most_common(a.show)]
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/location_by_quarter_{a.label}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:40]))
    print(f"docs/location_by_quarter_{a.label}.md written")


if __name__ == "__main__":
    main()
