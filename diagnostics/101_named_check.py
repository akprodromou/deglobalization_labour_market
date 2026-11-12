"""
Month 4: check the seven named emerging occupations directly (found or not, never forced).

The cluster reports of script 92 only say in which clusters a regex match falls. This script lists every matching posting, so two things
can be judged by eye: (1) is the regex precise (is the match really that occupation), (2) where did the postings go (own cluster, a sibling
cluster, noise) and when were they posted. A cluster needs at least --min-cluster-size (40) postings, so an occupation with 17 postings cannot
form a cluster by construction; it is reported here as a count by quarter instead.

Run (project root, venv active), one line per board:
    python -m diagnostics.101_named_check --board jobbland --titles data/tagged/titles_jobbland_inf.jsonl
    python -m diagnostics.101_named_check --board lesjeudis
    python -m diagnostics.101_named_check --board jobsde

Output: docs/named_check_<board>.md
"""

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path


def load(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def named_rx():
    try:
        from diagnostics.cluster_named import NAMED_RX
        return NAMED_RX
    except ImportError:
        sp = importlib.util.spec_from_file_location("c92", str(Path(__file__).with_name("92_cluster_postings.py")))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m.NAMED_RX


def quarter(day):
    return f"{day[:4]}-Q{(int(day[5:7]) - 1) // 3 + 1}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--titles", help="the titles file used for the clustering (jobbland: titles_jobbland_inf.jsonl)")
    ap.add_argument("--labels")
    ap.add_argument("--show", type=int, default=40)
    a = ap.parse_args()
    titles = load(a.titles or f"data/tagged/titles_{a.board}.jsonl")
    labels = {str(r["id"]): r for r in load(a.labels or f"data/cluster/labels_{a.board}_{a.input}.jsonl")}
    size = Counter(r["cluster"] for r in labels.values())
    rx = named_rx()
    L = [f"# Named occupations, direct check: {a.board}, input {a.input}", "",
         f"{len(titles):,} postings; {sum(1 for c in size if c >= 0)} clusters. A cluster needs at least 40 postings, so a count below 40 cannot form one.", ""]
    for name, r in rx.items():
        hits = [t for t in titles if t.get("title_clean") and r.search(t["title_clean"])]
        inc = [t for t in hits if labels.get(str(t["id"]), {}).get("cluster", -1) >= 0]
        L += [f"## {name}", "", f"{len(hits)} matching titles; {len(inc)} in a cluster, {len(hits) - len(inc)} in noise. "
              + "By quarter: " + (", ".join(f"{q} {n}" for q, n in sorted(Counter(quarter(t["day"]) for t in hits).items())) or "none") + ".", ""]
        if hits:
            L += ["| day | cleaned title | cluster (size) |", "|---|---|---|"]
            for t in sorted(hits, key=lambda x: x["day"])[:a.show]:
                c = labels.get(str(t["id"]), {}).get("cluster", -1)
                L.append(f"| {t['day']} | {t['title_clean'][:110]} | {'noise' if c < 0 else f'C{c} ({size[c]})'} |")
            if len(hits) > a.show:
                L.append(f"| ... | {len(hits) - a.show} more | |")
            L.append("")
    Path("docs").mkdir(exist_ok=True)
    out = Path(f"docs/named_check_{a.board}.md")
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{out} written")


if __name__ == "__main__":
    main()
