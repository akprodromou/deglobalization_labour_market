"""
Month 4 figure: a two-dimensional UMAP map of one board's title embeddings (input A), with the seven named occupations marked and, optionally,
the selected flagged clusters coloured. The map is for validation and illustration only (the clusters themselves come from the 10-dimensional
UMAP of script 92). A posting is marked as a named occupation when the regex of script 92 matches its cleaned title (never forced).

Reads: data/cluster/emb_<board>.npy (script 92, same order as the titles file), data/tagged/titles_<board>.jsonl,
       data/cluster/labels_<board>_A.jsonl (cluster of each posting; only needed for --clusters).
Writes: data/cluster/umap2d_<board>.npy (coordinates, so the map can be redrawn without the UMAP run), docs/fig/umap_<board>.png,
        docs/umap_named_<board>.md (named-occupation counts and the share of each that sits in one cluster).

Run (project root, venv active; on Colab from /content/work):
    python -m diagnostics.112_umap_map --board lesjeudis --clusters 33 68 137 130 139
(on Colab the script is run as: python 112_umap_map.py --board lesjeudis --clusters 33 68 137 130 139)
"""
import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path

import numpy as np


def load_92():
    here = Path(__file__).resolve().parent
    for cand in (here / "92_cluster_postings.py", Path("92_cluster_postings.py")):
        if cand.exists():
            spec = importlib.util.spec_from_file_location("cp92", cand)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    raise SystemExit("92_cluster_postings.py not found next to this script")


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--clusters", type=int, nargs="*", default=[])
    ap.add_argument("--n-neighbors", type=int, default=30)
    ap.add_argument("--min-dist", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--max-bg", type=int, default=20000, help="background points drawn (all points are in the UMAP)")
    ap.add_argument("--redraw", action="store_true", help="reuse data/cluster/umap2d_<board>.npy")
    a = ap.parse_args()
    cp = load_92()
    recs = load_jsonl(f"data/tagged/titles_{a.board}.jsonl")
    e = np.load(f"data/cluster/emb_{a.board}.npy")
    assert len(e) == len(recs), f"embeddings {len(e)} and titles {len(recs)} differ in length"
    cache = Path(f"data/cluster/umap2d_{a.board}.npy")
    if a.redraw and cache.exists():
        xy = np.load(cache)
    else:
        import umap
        xy = umap.UMAP(n_neighbors=a.n_neighbors, n_components=2, min_dist=a.min_dist, metric="cosine", random_state=a.seed).fit_transform(e)
        np.save(cache, xy.astype("float32"))
    lab = np.full(len(recs), -1)
    if a.clusters:
        by_id = {str(r["id"]): int(r["cluster"]) for r in load_jsonl(f"data/cluster/labels_{a.board}_A.jsonl")}
        lab = np.array([by_id.get(str(r["id"]), -1) for r in recs])
    texts = [cp.text_a(r) for r in recs]
    named = {k: np.array([bool(rx.search(t)) for t in texts]) for k, rx in cp.NAMED_RX.items()}

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    try:
        import seaborn as sns
        sns.set_theme(style="whitegrid")
    except ImportError:
        pass
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "Helvetica Neue", "DejaVu Sans"]
    palette = ["#40798C", "#a170a9", "#798c40", "#70A9A1", "#a98570"]
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    rng = np.random.default_rng(a.seed)
    bg = np.arange(len(xy))
    if len(bg) > a.max_bg:
        bg = rng.choice(bg, a.max_bg, replace=False)
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.scatter(xy[bg, 0], xy[bg, 1], s=2, c="#cccccc", alpha=0.5, linewidths=0, rasterized=True, label="all postings (sample)")
    for i, c in enumerate(a.clusters):
        m = lab == c
        if m.any():
            ax.scatter(xy[m, 0], xy[m, 1], s=9, c=palette[i % len(palette)], alpha=0.85, linewidths=0, label=f"cluster {c} (n={int(m.sum())})")
    markers = ["o", "s", "^", "D", "v", "P", "X"]
    md = [f"# Named occupations on the UMAP map: {a.board}", "", "| named occupation | postings with a title match | share in its largest cluster |", "|---|---|---|"]
    for j, (k, m) in enumerate(named.items()):
        n = int(m.sum())
        if n:
            ax.scatter(xy[m, 0], xy[m, 1], s=34, marker=markers[j % len(markers)], facecolors="none", edgecolors="black", linewidths=0.9, label=f"{k} (n={n})")
            cnt = Counter(lab[m].tolist()) if a.clusters else Counter()
        md.append(f"| {k} | {n} | " + (f"{max(Counter(_cluster_of(a, recs, m)).values()) / n:.0%}" if n else "") + " |")
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.set_title(f"{a.board}: two-dimensional UMAP of the title embeddings (input A)", fontsize=11)
    ax.legend(fontsize=7, markerscale=1.5, loc="best", frameon=True)
    fig.tight_layout()
    Path("docs/fig").mkdir(parents=True, exist_ok=True)
    fig.savefig(f"docs/fig/umap_{a.board}.png", dpi=200)
    Path(f"docs/umap_named_{a.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"docs/fig/umap_{a.board}.png written")


def _cluster_of(a, recs, mask):
    by_id = {str(r["id"]): int(r["cluster"]) for r in load_jsonl(f"data/cluster/labels_{a.board}_A.jsonl")}
    return [by_id.get(str(r["id"]), -1) for r, m in zip(recs, mask) if m]


if __name__ == "__main__":
    main()
