"""
Month 4 deliverables for the selected clusters of one board: (1) the regional table (top NUTS-2 regions, weighted share of the cluster's
placed postings, with the number of placed postings and the unplaced share), (2) three figures: quarterly share of each selected cluster
with interval C, regional HHI per cluster next to its unplaced share, and the Occupation Emergence Rate per quarter.

Reads (project root): data/cluster/labels_<board>_<input>.jsonl (script 92), data/tagged/nuts2_<board>.jsonl (script 96),
data/cluster/series_<board>_<input>.csv and hhi_<board>_<input>.csv (script 93), docs/emergence_<board>_<input>.md (script 93) and the
corpus for the day weights. Restrict the regional table to a window with --from and --to (jobbland: the windows with a stable location
text are 2024-04-01 to 2025-06-30 and 2026-04-01 to 2026-09-30).
Output: docs/final_clusters_<board>.md and docs/fig/<board>_series.png, <board>_hhi.png, <board>_oer.png

Run (project root, venv active), lesjeudis:
    python -m diagnostics.110_final_clusters --board lesjeudis --clusters 33 68 137 130 139 --corpus data/raw/corpus_lesjeudis.com_2024-08_2025-04.jsonl data/raw/corpus_lesjeudis.com_2025-05_2025-09.jsonl
"""
import argparse
import csv
import json
import re
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


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def oer_table(md_path):
    """The Occupation Emergence Rate table of the emergence report: quarter -> (newly crossing, clearly new, returning)."""
    if not Path(md_path).exists():
        return {}
    s = open(md_path, encoding="utf-8").read()
    m = re.search(r"## Occupation Emergence Rate\s*\n\n\|.*?\n\|[-| ]+\n(.*?)\n\n", s, re.S)
    out = {}
    if m:
        for line in m.group(1).split("\n"):
            c = [x.strip() for x in line.strip("|").split("|")]
            if len(c) >= 8:
                out[c[0]] = (int(c[2]), int(c[6]), int(c[7]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--clusters", type=int, nargs="+", required=True)
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--from", dest="d_from", default="0000-00-00")
    ap.add_argument("--to", dest="d_to", default="9999-99-99")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--min-days", type=int, default=20)
    a = ap.parse_args()
    tag = f"{a.board}_{a.input}"
    lab = {}
    for l in open(f"data/cluster/labels_{tag}.jsonl", encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            lab[str(r["id"])] = int(r["cluster"])
    reg = {}
    for l in open(f"data/tagged/nuts2_{a.board}.jsonl", encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            reg[str(r["id"])] = r.get("nuts2")
    rows, _ = load_all(a.corpus)
    wt = defaultdict(lambda: defaultdict(float))
    placed_n = Counter()
    all_n = Counter()
    unpl_w = defaultdict(float)
    tot_w = defaultdict(float)
    for r in rows:
        if not (a.d_from <= r["day"] <= a.d_to):
            continue
        pid = str(r["item"]["id"])
        c = lab.get(pid)
        if c not in a.clusters:
            continue
        all_n[c] += 1
        tot_w[c] += r["w"]
        code = reg.get(pid)
        if code:
            wt[c][code] += r["w"]
            placed_n[c] += 1
        else:
            unpl_w[c] += r["w"]
    md = [f"# Regional table of the selected clusters: {a.board}, input {a.input}", "",
          f"Weighted share of the cluster's placed postings by NUTS-2 region (top {a.top}); window {a.d_from} to {a.d_to}. Postings without a region are left out and their weighted share is shown.", "",
          "| cluster | postings in window | placed | unplaced (weighted) | " + " | ".join(f"region {i + 1}" for i in range(a.top)) + " |",
          "|---|---|---|---|" + "---|" * a.top]
    for c in a.clusters:
        pw = sum(wt[c].values())
        top = sorted(wt[c].items(), key=lambda kv: -kv[1])[: a.top]
        cells = [f"{k} {100 * v / pw:.0f}%" for k, v in top] + [""] * (a.top - len(top)) if pw else [""] * a.top
        un = unpl_w[c] / tot_w[c] if tot_w[c] else float("nan")
        md.append(f"| {c} | {all_n[c]} | {placed_n[c]} | {un:.0%} | " + " | ".join(cells) + " |")
    Path("docs/fig").mkdir(parents=True, exist_ok=True)
    Path(f"docs/final_clusters_{a.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    try:
        import seaborn as sns
        sns.set_theme(style="whitegrid")
    except ImportError:
        plt.rcParams["axes.grid"] = True
        plt.rcParams["grid.color"] = "#dddddd"
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "Helvetica Neue", "DejaVu Sans"]
    palette = ["#40798C", "#a170a9", "#798c40", "#70A9A1", "#a98570"]
    plt.rcParams["axes.prop_cycle"] = plt.cycler(color=palette)
    plt.rcParams["axes.spines.left"] = True
    plt.rcParams["axes.spines.bottom"] = True
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    # (1) quarterly shares
    ser = defaultdict(list)
    sp = f"data/cluster/series_{tag}.csv"
    for r in csv.DictReader(open(sp, encoding="utf-8")):
        c = int(r["cluster"])
        if c in a.clusters and int(r["days"]) >= a.min_days:
            ser[c].append((r["quarter"], 100 * fnum(r["share"]), 100 * fnum(r["share_lo_C"]), 100 * fnum(r["share_hi_C"])))
    qs = sorted({q for v in ser.values() for q, *_ in v})
    n = len(a.clusters)
    cols = min(3, n)
    nr = (n + cols - 1) // cols
    fig, axs = plt.subplots(nr, cols, figsize=(4.2 * cols, 2.8 * nr), squeeze=False)
    for ax, c in zip(axs.ravel(), a.clusters):
        v = sorted(ser.get(c, []))
        x = [qs.index(q) for q, *_ in v]
        ax.fill_between(x, [t[2] for t in v], [t[3] for t in v], alpha=0.25, color=palette[0], linewidth=0)
        ax.plot(x, [t[1] for t in v], marker="o", ms=3, color=palette[0])
        ax.set_title(f"cluster {c}", fontsize=10)
        ax.set_xticks(range(len(qs)))
        ax.set_xticklabels(qs, rotation=90, fontsize=7)
        ax.set_ylabel("share of board, %", fontsize=8)
        ax.set_ylim(bottom=0)
        ax.grid(alpha=0.5)
    for ax in axs.ravel()[n:]:
        ax.axis("off")
    fig.suptitle(f"{a.board}: quarterly share of the selected clusters (interval C; quarters with at least {a.min_days} sampled days)", fontsize=10)
    fig.tight_layout()
    fig.savefig(f"docs/fig/{a.board}_series.png", dpi=200)
    plt.close(fig)

    # (2) HHI whole period with unplaced share
    hh = {}
    for r in csv.DictReader(open(f"data/cluster/hhi_{tag}.csv", encoding="utf-8")):
        if r["quarter"] == "all" and r["cluster"].lstrip("-").isdigit() and int(r["cluster"]) in a.clusters:
            hh[int(r["cluster"])] = (fnum(r["hhi_norm"]), fnum(r["unplaced_share"]), int(r["placed_taken"]))
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    xs = [c for c in a.clusters if c in hh]
    ax.bar(range(len(xs)), [hh[c][0] for c in xs], color=palette[0])
    for i, c in enumerate(xs):
        ax.text(i, hh[c][0] + 0.01, f"unplaced {max(hh[c][1], 0):.0%}\nn={hh[c][2]}", ha="center", fontsize=7)
    ax.set_xticks(range(len(xs)))
    ax.set_xticklabels([str(c) for c in xs])
    ax.set_xlabel("cluster")
    ax.set_ylabel("normalised HHI over NUTS-2 regions")
    ax.set_ylim(0, max([hh[c][0] for c in xs] + [0.1]) * 1.3)
    ax.set_title(f"{a.board}: regional concentration of the selected clusters, whole period", fontsize=10)
    fig.tight_layout()
    fig.savefig(f"docs/fig/{a.board}_hhi.png", dpi=200)
    plt.close(fig)

    # (3) Occupation Emergence Rate from the report of script 93
    oer = oer_table(f"docs/emergence_{tag}.md")
    if oer:
        q2 = sorted(oer)
        fig, ax = plt.subplots(figsize=(7, 3.2))
        w = 0.4
        ax.bar([i - w / 2 for i in range(len(q2))], [oer[q][0] for q in q2], w, label="newly crossing the threshold", color=palette[0])
        ax.bar([i + w / 2 for i in range(len(q2))], [oer[q][1] for q in q2], w, label="clearly new (stricter rule)", color=palette[1])
        ax.set_xticks(range(len(q2)))
        ax.set_xticklabels(q2, rotation=90, fontsize=8)
        ax.set_ylabel("clusters")
        ax.legend(fontsize=8)
        ax.set_title(f"{a.board}: Occupation Emergence Rate per quarter", fontsize=10)
        fig.tight_layout()
        fig.savefig(f"docs/fig/{a.board}_oer.png", dpi=200)
        plt.close(fig)
    print("\n".join(md))
    print(f"docs/final_clusters_{a.board}.md and docs/fig/{a.board}_*.png written")


if __name__ == "__main__":
    main()
