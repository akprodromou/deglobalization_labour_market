"""
Open item 20: how close is each cluster to an existing ESCO occupation? For every cluster, the ESCO skills found in its postings (script 69b) are
compared with the skill set of every ESCO occupation. A cluster whose best match is weak is a candidate for something that ESCO does not describe;
a cluster with a strong match is a known occupation (after Giabelli et al. 2021, where "new" is relative to the taxonomy).

Cluster vector  = for each ESCO skill, the share of the cluster's postings that mention it, times an idf weight (log of board postings / board postings with the skill),
                  so that skills present everywhere (English, teamwork) count little.
Occupation vector = the same idf weight for each essential skill, half of it for each optional skill.
Score = cosine similarity of the two vectors (0 = nothing in common, 1 = identical).
The scores of the selected clusters are shown next to the distribution over all clusters of the board (percentile of the best score).

Reads (project root): data/cluster/labels_<board>_A.jsonl, data/tagged/skills_local_full_<board>_t0.60.jsonl, data/tagged/titles_<board>.jsonl (for the top titles),
                      data/esco_dataset/occupations_en.csv, occupationSkillRelations_en.csv, skills_en.csv
Writes: docs/esco_overlap_<board>.md and data/cluster/esco_overlap_<board>.csv

Run (project root, venv active):
    python -m diagnostics.115_esco_overlap --board lesjeudis --clusters 33 68 137 130 139
"""
import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import sparse


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--clusters", type=int, nargs="*", default=[], help="clusters shown in the table (the rest only fix the distribution)")
    ap.add_argument("--esco-dir", default="data/esco_dataset")
    ap.add_argument("--skills")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--min-postings", type=int, default=20, help="clusters with fewer postings that have skills are skipped")
    a = ap.parse_args()
    lab = {str(r["id"]): int(r["cluster"]) for r in jl(f"data/cluster/labels_{a.board}_{a.input}.jsonl")}
    sk = {str(r["id"]): r["skills"] for r in jl(a.skills or f"data/tagged/skills_local_full_{a.board}_t0.60.jsonl")}
    tp = Path(f"data/tagged/titles_{a.board}.jsonl")
    title = {str(r["id"]): (r.get("title_clean") or r.get("title") or "") for r in jl(tp)} if tp.exists() else {}
    occ_label, occ_isco = {}, {}
    with open(f"{a.esco_dir}/occupations_en.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            occ_label[r["conceptUri"]] = r["preferredLabel"]
            occ_isco[r["conceptUri"]] = r.get("iscoGroup", "")
    skill_label = {}
    with open(f"{a.esco_dir}/skills_en.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            skill_label[r["conceptUri"]] = r["preferredLabel"]
    rel = defaultdict(dict)
    with open(f"{a.esco_dir}/occupationSkillRelations_en.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rel[r["occupationUri"]][r["skillUri"]] = 1.0 if r["relationType"] == "essential" else 0.5
    ids_with = [i for i in lab if sk.get(i)]
    n_board = len(ids_with)
    df = Counter(u for i in ids_with for u in set(sk[i]))
    uris = sorted(df)
    col = {u: j for j, u in enumerate(uris)}
    idf = np.array([math.log(n_board / df[u]) for u in uris])
    occs = sorted(rel)
    rows_o, cols_o, vals_o = [], [], []
    for k, o in enumerate(occs):
        for u, w in rel[o].items():
            if u in col:
                rows_o.append(k); cols_o.append(col[u]); vals_o.append(w * idf[col[u]])
    O = sparse.csr_matrix((vals_o, (rows_o, cols_o)), shape=(len(occs), len(uris)))
    on = np.sqrt(O.multiply(O).sum(axis=1)).A1
    on[on == 0] = 1
    O = sparse.diags(1 / on) @ O
    members = defaultdict(list)
    for i, c in lab.items():
        if c >= 0:
            members[c].append(i)
    out, keep = [], []
    for c, ids in members.items():
        w = [i for i in ids if sk.get(i)]
        if len(w) < a.min_postings:
            continue
        cnt = Counter(u for i in w for u in set(sk[i]) if u in col)
        r_, c_, v_ = zip(*[(0, col[u], n / len(w) * idf[col[u]]) for u, n in cnt.items()]) if cnt else ((), (), ())
        v = sparse.csr_matrix((v_, (r_, c_)), shape=(1, len(uris)))
        nv = math.sqrt(v.multiply(v).sum())
        if nv == 0:
            continue
        sc = (O @ (v / nv).T).toarray().ravel()
        top = np.argsort(-sc)[: a.top]
        topsk = [skill_label.get(u, u.rsplit("/", 1)[-1]) for u, _ in sorted(cnt.items(), key=lambda kv: -kv[1] * idf[col[kv[0]]])[:5]]
        tt = Counter(title.get(i, "") for i in ids).most_common(3)
        out.append({"cluster": c, "postings": len(ids), "with_skills": len(w), "best": float(sc[top[0]]),
                    "matches": [(occ_label[occs[j]], occ_isco.get(occs[j], ""), float(sc[j])) for j in top], "skills": topsk, "titles": tt})
    best = np.array([o["best"] for o in out])
    for o in out:
        o["pct"] = float((best < o["best"]).mean())
    show = [o for o in out if o["cluster"] in set(a.clusters)] or out
    md = [f"# ESCO overlap of the clusters: {a.board}, input {a.input}", "",
          f"{len(out)} clusters with at least {a.min_postings} postings that carry skills; {n_board:,} board postings carry skills ({n_board / len(lab):.0%} of {len(lab):,}).",
          f"Score = cosine similarity between the idf-weighted skill profile of the cluster and of an ESCO occupation (essential skills 1, optional 0.5). Over all clusters of the board the best score has median {np.median(best):.2f} "
          f"(quartiles {np.percentile(best, 25):.2f} and {np.percentile(best, 75):.2f}, minimum {best.min():.2f}, maximum {best.max():.2f}). Percentile = share of the board's clusters with a lower best score.", "",
          "| cluster | postings (with skills) | best ESCO occupation (ISCO group, score) | next two | percentile | top skills of the cluster | top titles |", "|---|---|---|---|---|---|---|"]
    for o in sorted(show, key=lambda o: o["best"]):
        m = o["matches"]
        md.append(f"| {o['cluster']} | {o['postings']} ({o['with_skills']}) | {m[0][0]} ({m[0][1]}, {m[0][2]:.2f}) | " + "; ".join(f"{x[0]} ({x[2]:.2f})" for x in m[1:]) +
                  f" | {o['pct']:.0%} | {'; '.join(o['skills'])} | " + "; ".join(f"{t} ({n})" for t, n in o["titles"] if t) + " |")
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/esco_overlap_{a.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    with open(f"data/cluster/esco_overlap_{a.board}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["cluster", "postings", "with_skills", "best_score", "best_occupation", "best_isco", "percentile"])
        for o in out:
            w.writerow([o["cluster"], o["postings"], o["with_skills"], f"{o['best']:.4f}", o["matches"][0][0], o["matches"][0][1], f"{o['pct']:.3f}"])
    print("\n".join(md))


if __name__ == "__main__":
    main()
