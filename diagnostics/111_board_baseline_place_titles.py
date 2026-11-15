"""
Two checks for the report (items 27 and 28).
(1) Baseline: the board-wide regional mix (top NUTS-2 regions by weighted share of placed postings) in a window, to read next to the regional table of script 110.
(2) Place words in titles, by quarter: share of titles that contain the word Sweden/Swedish/Sverige/svensk(a) or the name of a large Swedish city,
    for the whole board and for the given cluster(s). Tests whether jobbland cluster 283 measures the change of the location text.

Output: docs/baseline_place_titles_<board>.md

Run (project root, venv active):
    python -m diagnostics.111_board_baseline_place_titles --board jobbland --clusters 283 350 --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl
"""
import argparse
import json
import re
import tempfile
from collections import defaultdict
from pathlib import Path

WORDS = re.compile(r"\b(sweden|swedish|sverige|svensk\w*|stockholm|g[oö]teborg|gothenburg|malm[oö]|uppsala|link[oö]ping|v[aä]ster[aå]s|[oö]rebro|helsingborg|norrk[oö]ping|j[oö]nk[oö]ping|ume[aå]|lund)\b", re.I)


def quarter(day):
    return f"{day[:4]}-Q{(int(day[5:7]) - 1) // 3 + 1}"


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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--clusters", type=int, nargs="+", default=[])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--from", dest="d_from", default="0000-00-00")
    ap.add_argument("--to", dest="d_to", default="9999-99-99")
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    lab = {}
    for l in open(f"data/cluster/labels_{a.board}_{a.input}.jsonl", encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            lab[str(r["id"])] = int(r["cluster"])
    reg = {}
    for l in open(f"data/tagged/nuts2_{a.board}.jsonl", encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            reg[str(r["id"])] = r.get("nuts2")
    rows, _ = load_all(a.corpus)
    mix = defaultdict(float)
    tot = defaultdict(lambda: [0.0, 0.0])      # key -> [weight with place word, weight all]
    n_title = 0
    for r in rows:
        it = r["item"]
        pid = str(it["id"])
        q = quarter(r["day"])
        title = (it.get("title_clean") or it.get("title") or "").strip()
        n_title += bool(title)
        hit = bool(WORDS.search(title))
        if a.d_from <= r["day"] <= a.d_to and reg.get(pid):
            mix[reg[pid]] += r["w"]
        for key in [("board", q)] + [(c, q) for c in a.clusters if lab.get(pid) == c]:
            tot[key][1] += r["w"]
            tot[key][0] += r["w"] * hit
    md = [f"# Baseline and place words in titles: {a.board}", "",
          f"## Board-wide regional mix, window {a.d_from} to {a.d_to}", "", "| region | weighted share of placed postings |", "|---|---|"]
    s = sum(mix.values())
    for k, v in sorted(mix.items(), key=lambda kv: -kv[1])[: a.top]:
        md.append(f"| {k} | {100 * v / s:.1f}% |")
    qs = sorted({k[1] for k in tot})
    keys = ["board"] + a.clusters
    md += ["", "## Share of titles with a place word (Sweden, Swedish, Sverige, svensk, or a large Swedish city), weighted, by quarter", "",
           "| quarter | " + " | ".join("board" if k == "board" else f"cluster {k}" for k in keys) + " |", "|---|" + "---|" * len(keys)]
    for q in qs:
        cells = []
        for k in keys:
            h, n = tot.get((k, q), [0.0, 0.0])
            cells.append(f"{100 * h / n:.1f}%" if n else "")
        md.append(f"| {q} | " + " | ".join(cells) + " |")
    md += ["", f"Postings with a non-empty title field: {n_title} of {len(rows)}. If this is 0, the title field name differs in the corpus and the second table is empty."]
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/baseline_place_titles_{a.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
