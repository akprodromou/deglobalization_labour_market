"""
Month 4, supervisor request 3a: compare 3 to 4 clustering algorithms by silhouette BEFORE the clustering setup is fixed
(runs on Colab, same environment as script 92; it imports 92's embedding, skill blocks and UMAP + HDBSCAN, so inputs A and D
are built exactly as there). One board per run.

Algorithms, all on the same 10-dimensional UMAP space of the input (cosine UMAP, min_dist 0, as in script 92):
  hdbscan_eom   HDBSCAN, excess-of-mass selection (the script 92 setting)
  hdbscan_leaf  HDBSCAN, leaf selection (smaller, finer clusters: the ones most likely to hold a new narrow occupation)
  kmeans        k-means with the same k as hdbscan_eom (no noise: every posting is placed)
  ward          agglomerative clustering, Ward linkage on a nearest-neighbour graph (--ward-neighbors), same k (no noise)
Also a k scan for k-means (--kscan), to see how silhouette changes with the number of clusters.

Measures per algorithm
  clusters, noise share (HDBSCAN only), share of postings in the largest cluster, median cluster size
  silhouette (UMAP space, Euclidean) and silhouette (input space, cosine) of the postings that were clustered, on a random
  sample of --sample postings (silhouette needs all pairwise distances). The silhouette of a posting is
  (distance to the nearest other cluster - distance to its own cluster) / the larger of the two: 1 = well inside its cluster,
  0 = on a boundary, negative = nearer to another cluster.
HDBSCAN leaves noise out of its silhouette, so an algorithm that drops 30% of the postings can look better than one that
places everyone. The table therefore always shows the noise share next to the silhouette, and --also-noise-free gives the silhouette
of the non-noise postings of hdbscan_eom for the other algorithms too (the same postings are scored for every algorithm).

Output: docs/cluster_compare_<board>_<input>.md and data/cluster/cluster_compare_<board>_<input>.csv

Run on Colab after the same setup as script 92 (pip install sentence-transformers umap-learn hdbscan scikit-learn), per board:
    python -m diagnostics.105_cluster_compare --board lesjeudis --input A D
D v2 with equal Lightcast and ESCO weights (supervisor): --w-skills 0.5 --w-lc 0.5 (the defaults of this script)
D v3 (weights 0.25 and 0.25, common items dropped): --input D --w-skills 0.25 --w-lc 0.25 --max-df 0.05 --tag v3
Test without a GPU: --mock --limit 3000
"""

import argparse
import csv
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np


def load92():
    p = Path(__file__).with_name("92_cluster_postings.py")
    spec = importlib.util.spec_from_file_location("cp92", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def sizes(lab):
    v = lab[lab >= 0]
    if not len(v):
        return 0, float("nan"), float("nan")
    cnt = np.bincount(v)
    cnt = cnt[cnt > 0]
    return int(len(cnt)), float(cnt.max() / len(lab)), float(np.median(cnt))


def silh(x, lab, idx, metric):
    from sklearn.metrics import silhouette_score
    l = lab[idx]
    ok = l >= 0
    if ok.sum() < 3 or len(set(l[ok].tolist())) < 2:
        return float("nan")
    return float(silhouette_score(x[idx][ok], l[ok], metric=metric))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True, help="jobbland | lesjeudis | jobsde")
    ap.add_argument("--input", nargs="+", default=["A", "D"], choices=["A", "D"])
    ap.add_argument("--titles")
    ap.add_argument("--skills")
    ap.add_argument("--lightcast")
    ap.add_argument("--lc-terms", default="lexicon/lightcast_block_terms.csv")
    ap.add_argument("--esco-csv", default="lexicon/skills.csv")
    ap.add_argument("--model", default="intfloat/multilingual-e5-large")
    ap.add_argument("--out", default="data/cluster")
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--min-cluster-size", type=int, default=40)
    ap.add_argument("--min-samples", type=int, default=10)
    ap.add_argument("--n-neighbors", type=int, default=30)
    ap.add_argument("--dims", type=int, default=10)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--w-skills", type=float, default=0.5)
    ap.add_argument("--w-lc", type=float, default=0.5, help="equal to the ESCO weight, as the supervisor asked (script 92 default 0.3)")
    ap.add_argument("--min-lift", type=float, default=0.15)
    ap.add_argument("--max-df", type=float, default=None, help="D v3: drop skills and Lightcast terms present in more than this share of the board's postings (for example 0.05), as in script 92")
    ap.add_argument("--tag", default="", help="suffix for the output files (for example v3 gives cluster_compare_<board>_D_v3.md)")
    ap.add_argument("--no-coherence", action="store_true")
    ap.add_argument("--ward-neighbors", type=int, default=15)
    ap.add_argument("--kscan", type=int, nargs="+", default=[25, 50, 100, 200, 400])
    ap.add_argument("--sample", type=int, default=10000)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--mock", action="store_true")
    args = ap.parse_args()
    args.seeds = [args.seed]

    cp = load92()
    import hdbscan
    from sklearn.cluster import AgglomerativeClustering, KMeans
    from sklearn.neighbors import kneighbors_graph

    titles = args.titles or f"data/tagged/titles_{args.board}.jsonl"
    skills = args.skills or f"data/tagged/skills_local_full_{args.board}_t0.60.jsonl"
    lcf = args.lightcast or f"data/tagged/lightcast_block_{args.board}.jsonl"
    recs = cp.load_jsonl(titles)
    if args.limit:
        recs = recs[: args.limit]
    ids = [r["id"] for r in recs]
    Path(args.out).mkdir(parents=True, exist_ok=True)
    Path(args.docs).mkdir(parents=True, exist_ok=True)
    esco_label = {}
    if Path(args.esco_csv).exists():
        with open(args.esco_csv, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                esco_label[r["id"]] = r.get("description", "")[:40]
    cache = None if args.limit else f"{args.out}/emb_{args.board}.npy"
    e = cp.embed_titles([cp.text_a(r) for r in recs], args.model, cache, args.mock)
    rng = np.random.default_rng(args.seed)

    for name in args.input:
        if name == "A":
            x = e
        else:
            if not Path(skills).exists():
                sys.exit(f"missing {skills}")
            blocks, _ = cp.skill_blocks(ids, e, skills, lcf, args.lc_terms, args.w_skills, args.w_lc,
                                        None if args.no_coherence else args.min_lift, esco_label, args.docs, args.board,
                                        max_df=args.max_df)
            x = np.hstack([e] + blocks)
            x = x / np.linalg.norm(x, axis=1, keepdims=True)
        print(f"[{name}] UMAP + HDBSCAN (eom)")
        t0 = time.time()
        u, h = cp.run_umap_hdbscan(x, args.seed, args)
        t_umap = time.time() - t0
        n = len(u)
        idx = np.sort(rng.choice(n, min(args.sample, n), replace=False))
        res = []

        def add(algo, lab, secs):
            k, big, med = sizes(lab)
            res.append({"input": name, "algorithm": algo, "clusters": k, "noise_share": float((lab < 0).mean()),
                        "largest_share": big, "median_size": med,
                        "silhouette_umap": silh(u, lab, idx, "euclidean"), "silhouette_input": silh(x, lab, idx, "cosine"),
                        "seconds": round(secs, 1)})
            print(f"  {algo}: {k} clusters, noise {res[-1]['noise_share']:.1%}, silhouette umap {res[-1]['silhouette_umap']:.3f}, input {res[-1]['silhouette_input']:.3f}")

        lab_eom = h.labels_.copy()
        add("hdbscan_eom", lab_eom, t_umap)
        t0 = time.time()
        lab_leaf = hdbscan.HDBSCAN(min_cluster_size=args.min_cluster_size, min_samples=args.min_samples, metric="euclidean",
                                   cluster_selection_method="leaf").fit(u).labels_
        add("hdbscan_leaf", lab_leaf, time.time() - t0)
        k = max(int(lab_eom.max()) + 1, 2)
        t0 = time.time()
        lab_km = KMeans(k, n_init=3, random_state=args.seed).fit(u).labels_
        add(f"kmeans_k{k}", lab_km, time.time() - t0)
        t0 = time.time()
        g = kneighbors_graph(u, args.ward_neighbors, include_self=False)
        lab_wd = AgglomerativeClustering(n_clusters=k, linkage="ward", connectivity=g).fit_predict(u)
        add(f"ward_k{k}", lab_wd, time.time() - t0)

        # same postings scored for every algorithm: the ones HDBSCAN-eom placed in a cluster
        shared = idx[lab_eom[idx] >= 0]
        for r, lab in zip(res, (lab_eom, lab_leaf, lab_km, lab_wd)):
            l = lab.copy()
            mask = np.zeros(n, bool)
            mask[shared] = True
            l[~mask] = -1
            r["silhouette_umap_on_eom_placed"] = silh(u, l, shared, "euclidean")
            r["silhouette_input_on_eom_placed"] = silh(x, l, shared, "cosine")

        scan = []
        for kk in args.kscan:
            if kk >= n:
                continue
            lab = KMeans(kk, n_init=2, random_state=args.seed).fit(u).labels_
            scan.append({"k": kk, "silhouette_umap": silh(u, lab, idx, "euclidean"), "silhouette_input": silh(x, lab, idx, "cosine")})
            print(f"  kmeans k={kk}: silhouette umap {scan[-1]['silhouette_umap']:.3f}")

        tag = f"{args.board}_{name}" + (f"_{args.tag}" if args.tag else "")
        with open(f"{args.out}/cluster_compare_{tag}.csv", "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=list(res[0].keys()))
            wr.writeheader()
            wr.writerows(res)
        fm = lambda v, p=3: "" if v != v else f"{v:.{p}f}"
        md = [f"# Clustering algorithms compared by silhouette: {args.board}, input {name}", "",
              f"{n:,} postings, silhouette on a random sample of {len(idx):,}. UMAP space of {args.dims} dimensions, seed {args.seed}. "
              "Silhouette: 1 = well inside its cluster, 0 = on a boundary, negative = closer to another cluster; only clustered postings are scored. "
              "k-means and Ward place every posting, HDBSCAN leaves noise out, so read the noise share with the silhouette.", "",
              "| algorithm | clusters | noise | largest cluster | median size | silhouette (UMAP) | silhouette (input, cosine) | same postings for all: UMAP | same postings for all: input |",
              "|---|---|---|---|---|---|---|---|---|"]
        for r in res:
            md.append(f"| {r['algorithm']} | {r['clusters']} | {r['noise_share']:.1%} | {r['largest_share']:.1%} | {fm(r['median_size'], 0)} | "
                      f"{fm(r['silhouette_umap'])} | {fm(r['silhouette_input'])} | {fm(r['silhouette_umap_on_eom_placed'])} | {fm(r['silhouette_input_on_eom_placed'])} |")
        md += ["", "## k-means: silhouette against the number of clusters", "", "| k | silhouette (UMAP) | silhouette (input, cosine) |", "|---|---|---|"]
        for s in scan:
            md.append(f"| {s['k']} | {fm(s['silhouette_umap'])} | {fm(s['silhouette_input'])} |")
        md += ["", "Reading notes", "",
               "- Silhouette usually falls as k grows and is higher in the UMAP space (the clustering space) than in the input space; compare algorithms within one column.",
               "- The silhouette does not say which clusters are occupations. It says how separated the groups are. Check the named occupations and the cluster samples (script 98) next to it.",
               "- Columns \"same postings for all\" score the same postings (those hdbscan_eom placed) for every algorithm, which removes the advantage of dropping noise."]
        Path(f"{args.docs}/cluster_compare_{tag}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        print(f"wrote {args.docs}/cluster_compare_{tag}.md")


if __name__ == "__main__":
    main()
