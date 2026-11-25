from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent            # project folder (the parent of deliverables)
CSV = ROOT / "data" / "cluster" / "df_items_lesjeudis_esco.csv"   # written by script 125
N_POSTINGS = 18_625                                       # all postings of lesjeudis
MIN_COUNT = 1                                             # no minimum: all skills of the board (script 92 --min-items 1, script 125 --min-count 1)


def make_tukey_fence_plot():
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.color"] = "#dddddd"
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "Helvetica Neue", "DejaVu Sans"]
    palette = ["#40798C", "#a170a9", "#798c40", "#70A9A1", "#a98570"]
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

    # 1. Real shares: postings with the skill / all postings, for all skills (MIN_COUNT = 1)
    df = pd.read_csv(CSV)
    df = df[df["postings"] >= MIN_COUNT]
    shares = df["postings"].to_numpy() / N_POSTINGS * 100          # in %

    # 2. Upper Tukey fence on the logarithm of the shares (same rule as scripts 92 and 125)
    log_shares = np.log10(shares)
    q1, q3 = np.percentile(log_shares, [25, 75])
    fence_pct = 10 ** (q3 + 1.5 * (q3 - q1))
    n_removed = int((shares > fence_pct).sum())

    # 3. Figure
    fig, ax = plt.subplots(figsize=(5, 4), dpi=150)
    ax.hist(shares, bins=45, color=palette[0], edgecolor="white", alpha=0.9)
    ax.axvline(fence_pct, color=palette[1], linestyle="--", linewidth=1.8,
               label=f"Upper Tukey fence ({fence_pct:.2f}%)")
    ax.axvspan(fence_pct, shares.max() * 1.02, color=palette[1], alpha=0.18,
               label=f"Removed skills ({n_removed})")
    ax.set_title(f"Share of postings per ESCO skill (lesjeudis board)", fontsize=8)
    ax.set_xlabel("Share of postings, %", fontsize=8)
    ax.set_ylabel("Number of ESCO skills", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.5)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    # print(f"skills: {len(shares)}, median share {np.median(shares):.3f}%, fence {fence_pct:.3f}%, removed {n_removed}")
    return fig


if __name__ == "__main__":
    fig = make_tukey_fence_plot()
    fig.savefig("tukey_fence_lesjeudis.png")