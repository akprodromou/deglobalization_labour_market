"""
Month 4: what exactly changes in the mix of postings around one jump of the day total? (companion to script 97)

For one date (the first day after the jump) the --span-days sampled days before and from that date are compared. Per cluster:
how many postings were taken on each side, the share of the postings taken (unweighted: the composition of the pages), the weighted share
(the share the thesis uses), the change, the most frequent titles of the cluster, and how concentrated its postings after the jump are in
ONE template (the first 80 normalised description characters), which separates a broad shift in the kinds of job from one employer's or
one feed's batch. The same table is made for the same-length stretch just before the "before" window as a reference for an ordinary
change, and the share of Month 3 flagged postings on each side is printed.

A large share change in a cluster with a high template concentration is a batch: one source began (or stopped) delivering a block of
similar postings. A large change spread over many templates means the kinds of job in the database changed.

Run (project root, venv active), jobbland, jump of 2025-12-09:
    python -m diagnostics.97b_jump_example --board jobbland --input A --date 2025-12-09 --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl --tags data/tagged/tags_v12_jobbland.final.post.jsonl

Output: docs/jump_example_<board>_<date>.md
"""

import argparse
import json
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus, norm
except ImportError:
    from corpus_io import load_corpus, norm

CH = ["reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"]


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
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--date", required=True, help="first day after the jump, YYYY-MM-DD")
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--labels")
    ap.add_argument("--tags", nargs="+")
    ap.add_argument("--span-days", type=int, default=14)
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--min-after", type=int, default=0, help="only clusters with at least this many postings on one of the two sides")
    a, _ignored = ap.parse_known_args()
    labels_p = a.labels or f"data/cluster/labels_{a.board}_{a.input}.jsonl"
    if not Path(labels_p).exists():
        raise SystemExit(f"labels file not found: {labels_p}")
    lab = {}
    for l in open(labels_p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            lab[str(r["id"])] = int(r["cluster"])
    flag = {}
    for p in a.tags or []:
        if not Path(p).exists():
            raise SystemExit(f"tags file not found: {p}")
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                if r.get("ok") and r.get("channel") in CH:
                    flag[str(r["posting_id"])] = r["channel"]

    rows, dup = load_all(a.corpus)
    days = sorted({r["day"] for r in rows})
    if a.date not in days:
        later = [d for d in days if d >= a.date]
        if not later:
            raise SystemExit("date is after the last sampled day")
        a.date = later[0]
    i = days.index(a.date)
    S = a.span_days
    if i < 2 * S:
        raise SystemExit("not enough sampled days before the date for the window and its reference")
    win = {"before": set(days[i - S:i]), "after": set(days[i:i + S]), "ref": set(days[i - 2 * S:i - S])}

    def side(name):
        return [r for r in rows if r["day"] in win[name]]

    def table(left, right, lname, rname):
        L_, R_ = side(left), side(right)
        nl, nr = len(L_), len(R_)
        wl, wr = sum(r["w"] for r in L_), sum(r["w"] for r in R_)
        cl, cr, wcl, wcr = Counter(), Counter(), Counter(), Counter()
        titles, tmpl = {}, {}
        for r in L_:
            c = lab.get(str(r["item"]["id"]), -2)
            cl[c] += 1
            wcl[c] += r["w"]
        for r in R_:
            c = lab.get(str(r["item"]["id"]), -2)
            cr[c] += 1
            wcr[c] += r["w"]
            titles.setdefault(c, Counter())[norm(r["item"].get("title") or "")[:60]] += 1
            tmpl.setdefault(c, Counter())[norm(r["item"].get("description") or "")[:80]] += 1
        for r in L_:
            c = lab.get(str(r["item"]["id"]), -2)
            titles.setdefault(c, Counter())[norm(r["item"].get("title") or "")[:60]] += 1
        out = []
        for c in set(cl) | set(cr):
            if max(cl[c], cr[c]) < a.min_after:
                continue
            sl, sr = cl[c] / nl, cr[c] / nr
            out.append((abs(sr - sl), c, cl[c], cr[c], sl, sr, wcl[c] / wl if wl else 0, wcr[c] / wr if wr else 0,
                        titles.get(c, Counter()).most_common(3), (max(tmpl[c].values()) / cr[c]) if cr[c] else 0))
        out.sort(reverse=True)
        fl = lambda rs: np.mean([str(r["item"]["id"]) in flag for r in rs]) if rs else 0
        nt = lambda rs: np.mean([not (r["item"].get("title") or "").strip() for r in rs]) if rs else 0
        lines = [f"{lname}: {len(win[left])} sampled days, {nl:,} postings taken, weighted {wl:,.0f}, mean day total {wl / len(win[left]):,.0f}, flagged {fl(L_):.1%} of taken, without title {nt(L_):.1%} of taken.",
                 f"{rname}: {len(win[right])} sampled days, {nr:,} postings taken, weighted {wr:,.0f}, mean day total {wr / len(win[right]):,.0f}, flagged {fl(R_):.1%} of taken, without title {nt(R_):.1%} of taken.\n",
                 f"| cluster | taken {lname} | taken {rname} | share of taken {lname} | share of taken {rname} | change | weighted share {lname} | weighted share {rname} | top titles | largest template group after |",
                 "|---|---|---|---|---|---|---|---|---|---|"]
        for d_, c, nl_, nr_, sl, sr, wsl, wsr, tt, ts in out[:a.top]:
            lines.append(f"| {c} | {nl_} | {nr_} | {sl:.1%} | {sr:.1%} | {sr - sl:+.1%} | {wsl:.1%} | {wsr:.1%} | "
                         f"{'; '.join(f'{t} ({n})' for t, n in tt)} | {ts:.0%} |")
        tv = 0.5 * sum(abs(cl[c] / nl - cr[c] / nr) for c in set(cl) | set(cr))
        lines.append(f"\nTotal share of postings that would have to change cluster to equalise the two mixes (half the sum of absolute differences): {tv:.1%}.")
        return lines

    M = [f"# What changes at {a.date}: {a.board} input {a.input}\n",
         f"Windows of {S} sampled days. Before = {min(win['before'])} to {max(win['before'])}; after = {min(win['after'])} to {max(win['after'])}; "
         f"reference = {min(win['ref'])} to {max(win['ref'])}. Postings are the postings taken (duplicates removed: {dup}).\n",
         "## The jump: before against after\n"] + table("before", "after", "before", "after") + \
        ["\n## Reference: the stretch before that against the 'before' window (an ordinary change at similar volume, if the volume was stable)\n"] + \
        table("ref", "before", "ref", "before") + \
        ["\n## Reading notes\n",
         "- The share change of a cluster is read against the reference table: an ordinary stretch shows how large changes are without a jump.",
         "- A large change with a template group above about 30% means one batch; spread over many templates means different kinds of job.",
         "- Cluster numbers have no meaning; the top titles are the clusters' names. Titles are counted over both sides."]
    Path("docs").mkdir(exist_ok=True)
    out_p = f"docs/jump_example_{a.board}_{a.date}.md"
    Path(out_p).write_text("\n".join(M) + "\n", encoding="utf-8")
    print(out_p + " written")


if __name__ == "__main__":
    main()
