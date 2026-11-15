"""
Month 4, supervisor question 4: are larger boards (markets) more or less like smaller boards in the composition and
concentration of their skill sets? One run covers all boards; nothing is merged, each board is weighted on its own.

Per board (day weights of script 52, duplicates removed as everywhere else):
  Concentration (HHI = sum of squared weighted shares; effective number = 1/HHI; top-10 share)
    skills      over the skills named in the postings (labels as the platform gives them)
    sectors     over the sector field
    clusters    over the title clusters of script 92 (noise left out)
    regions     over NUTS-2 regions (placed postings only)
    employers   over the organisation field (only where the board records it; share of postings with a name is reported)
  Each HHI is given twice: on the whole board, and on equal-size subsamples. HHI falls as a sample grows, so a big board
  looks less concentrated for no real reason. The subsample is --m postings (default: the smallest board's taken
  postings), drawn with probability proportional to the weight, repeated --reps times; median and 95% range reported.
  The fair comparison between boards is the subsample one.
  Composition
    Jensen-Shannon similarity (1 = identical, 0 = nothing shared) between the skill-share vectors and the sector-share
    vectors of every pair of boards, on the labels they share. If two boards use different vocabularies the similarity is
    low for that reason alone; the number of shared labels and the share of weight they cover are reported next to it.
  By period: skill and cluster HHI per quarter, so a size effect and a time effect can be told apart.

Output: docs/boards_concentration.md, data/cluster/boards_concentration.csv

Run (project root, venv active):
    python -m diagnostics.104_board_concentration --boards jobbland.se:jobbland:A lesjeudis.com:lesjeudis:A jobs.de:jobsde:A
Each board is domain:name:input. Corpus files are data/raw/corpus_<domain>_*.jsonl, labels data/cluster/labels_<name>_<input>.jsonl,
regions data/tagged/nuts2_<name>.jsonl. Options: --corpus-dir, --reps, --m.
"""

import argparse
import csv
import json
import tempfile
from collections import defaultdict
from glob import glob
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus


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


def labels_of(v):
    if not v:
        return []
    if isinstance(v, str):
        return [v.strip().lower()]
    out = []
    for x in v:
        if isinstance(x, dict):
            x = x.get("label") or x.get("name") or x.get("preferred_label") or x.get("id") or x.get("uri")
        if x:
            out.append(str(x).strip().lower())
    return out


def hhi(vec):
    t = vec.sum()
    return float(((vec / t) ** 2).sum()) if t > 0 else float("nan")


def top10(vec):
    t = vec.sum()
    return float(np.sort(vec)[::-1][:10].sum() / t) if t > 0 else float("nan")


def js_sim(p, q):
    p, q = p / p.sum(), q / q.sum()
    m = (p + q) / 2

    def kl(x, y):
        k = x > 0
        return float((x[k] * np.log2(x[k] / y[k])).sum())
    return 1 - (kl(p, m) + kl(q, m)) / 2


def counts(idx, w, keys):
    c = defaultdict(float)
    for j in idx:
        for k in set(keys[j]):
            c[k] += w[j]
    return c


RN = {"SE": 8, "FR": 22, "DE": 38}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--boards", nargs="+", required=True, help="domain:name:input, e.g. jobbland.se:jobbland:A")
    ap.add_argument("--corpus-dir", default="data/raw")
    ap.add_argument("--m", type=int, default=None, help="subsample size, default the smallest board's taken postings")
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--skills-source", choices=["api", "escox"], default="escox", help="escox = skills extracted from the full text by script 69b (default, same method for every board and month); api = the tracker's own tags in the corpus")
    ap.add_argument("--from", dest="d_from", default="0000-00-00", help="first day used; use a window common to all boards for a fair comparison")
    ap.add_argument("--to", dest="d_to", default="9999-99-99", help="last day used")
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)

    B = {}
    for spec in a.boards:
        parts = spec.split(":")
        dom, name, inp = parts[:3]
        country = parts[3].upper() if len(parts) > 3 else ""
        files = sorted(glob(f"{a.corpus_dir}/corpus_{dom}_*.jsonl"))
        if not files:
            raise SystemExit(f"no corpus files for {dom} in {a.corpus_dir}")
        rows, _ = load_all(files)
        rows = [r for r in rows if a.d_from <= r["day"] <= a.d_to]
        lab = {}
        p = f"data/cluster/labels_{name}_{inp}.jsonl"
        if Path(p).exists():
            for l in open(p, encoding="utf-8"):
                if l.strip():
                    r = json.loads(l)
                    lab[str(r["id"])] = int(r["cluster"])
        else:
            print(f"NOTE: {p} not found, cluster dimension empty for {name}")
        reg = {}
        p = f"data/tagged/nuts2_{name}.jsonl"
        if Path(p).exists():
            for l in open(p, encoding="utf-8"):
                if l.strip():
                    r = json.loads(l)
                    reg[str(r["id"])] = r["nuts2"]
        else:
            print(f"NOTE: {p} not found, region dimension empty for {name}")
        ids = [str(r["item"]["id"]) for r in rows]
        esc = None
        if a.skills_source == "escox":
            p = f"data/tagged/skills_local_full_{name}_t0.60.jsonl"
            if not Path(p).exists():
                raise SystemExit(f"{p} not found: run script 69b for this board, or use --skills-source api")
            esc = {}
            for l in open(p, encoding="utf-8"):
                if l.strip():
                    r = json.loads(l)
                    esc[str(r["id"])] = [str(x).strip().lower() for x in r.get("skills") or []]
        w = np.array([r["w"] for r in rows])
        B[name] = {
            "country": country, "n": len(rows), "w": w, "day": [r["day"] for r in rows],
            "skills": [esc.get(i, []) for i in ids] if esc is not None else [labels_of(r["item"].get("skills")) for r in rows],
            "sectors": [labels_of(r["item"].get("sectors")) for r in rows],
            "cluster": [[str(lab[i])] if i in lab and lab[i] >= 0 else [] for i in ids],
            "region": [[reg[i]] if reg.get(i) else [] for i in ids],
            "occupations": [labels_of(r["item"].get("occupations")) for r in rows],
            "employer": [[str(r["item"]["organization"]).strip().lower()] if r["item"].get("organization") else [] for r in rows],
        }
        print(f"{name}: {len(rows)} postings, weighted {w.sum():,.0f}")

    WT = ("" if a.skills_source == "escox" else "_api") + ("" if a.d_from == "0000-00-00" and a.d_to == "9999-99-99" else f"_{a.d_from}_{a.d_to}")
    m = a.m or min(b["n"] for b in B.values())
    dims = ["skills", "sectors", "cluster", "region", "employer"]
    out_rows, vec_full = [], {}
    for name, b in B.items():
        n = b["n"]
        pr = b["w"] / b["w"].sum()
        draws = [rng.choice(n, size=min(m, n), replace=True, p=pr) for _ in range(a.reps)]
        for d in dims:
            keys = b[d]
            has = np.array([len(k) > 0 for k in keys])
            if not has.any():
                out_rows.append({"board": name, "dimension": d, "coverage": 0.0})
                continue
            c = counts(range(n), b["w"], keys)
            if len(c) < 2:
                out_rows.append({"board": name, "dimension": d, "coverage": float(b["w"][has].sum() / b["w"].sum()), "labels": len(c), "note": "field not recorded"})
                continue
            v = np.array(list(c.values()))
            vec_full[(name, d)] = c
            hs, ts, es = [], [], []
            for s in draws:
                cs = defaultdict(float)
                for j in s:
                    for k in set(keys[j]):
                        cs[k] += 1
                vv = np.array(list(cs.values()))
                h = hhi(vv)
                hs.append(h); ts.append(top10(vv)); es.append(1 / h)
            out_rows.append({
                "board": name, "dimension": d, "coverage": float(b["w"][has].sum() / b["w"].sum()), "labels": len(c),
                "hhi_full": hhi(v), "eff_full": 1 / hhi(v), "top10_full": top10(v),
                "hhi_sub": float(np.median(hs)), "hhi_sub_lo": float(np.percentile(hs, 2.5)), "hhi_sub_hi": float(np.percentile(hs, 97.5)),
                "eff_sub": float(np.median(es)), "top10_sub": float(np.median(ts)), "m": min(m, n),
                "hhi_norm": ((hhi(v) - 1 / RN[b["country"]]) / (1 - 1 / RN[b["country"]])) if d == "region" and b["country"] in RN else None})

    Path("data/cluster").mkdir(parents=True, exist_ok=True)
    Path("docs").mkdir(exist_ok=True)
    cols = ["board", "dimension", "coverage", "labels", "hhi_full", "eff_full", "top10_full", "hhi_sub", "hhi_sub_lo", "hhi_sub_hi", "eff_sub", "top10_sub", "m", "hhi_norm"]
    with open(f"data/cluster/boards_concentration{WT}.csv", "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        wr.writeheader()
        wr.writerows(out_rows)

    names = list(B)
    sim = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            for d in ("skills", "sectors"):
                ci, cj = vec_full.get((names[i], d)), vec_full.get((names[j], d))
                if not ci or not cj:
                    continue
                shared = sorted(set(ci) & set(cj))
                if not shared:
                    sim.append((names[i], names[j], d, 0, 0.0, 0.0))
                    continue
                pi = np.array([ci[k] for k in shared]); pj = np.array([cj[k] for k in shared])
                cover = min(pi.sum() / sum(ci.values()), pj.sum() / sum(cj.values()))
                sim.append((names[i], names[j], d, len(shared), js_sim(pi, pj), cover))

    def quarter(day):
        y, mo, _ = day.split("-")
        return f"{y}-Q{(int(mo) - 1) // 3 + 1}"
    qrows = []
    for name, b in B.items():
        qd = np.array([quarter(d) for d in b["day"]])
        for q in sorted(set(qd)):
            ix = np.where(qd == q)[0]
            if len(ix) < 300:
                continue
            row = {"board": name, "quarter": q, "taken": len(ix)}
            for d in ("skills", "cluster"):
                c = counts(ix, b["w"], b[d])
                row[d] = hhi(np.array(list(c.values()))) if c else float("nan")
            hs_ = np.array([len(b["skills"][j]) > 0 for j in ix])
            row["skill_cov"] = float(b["w"][ix][hs_].sum() / b["w"][ix].sum())
            row["skills_per"] = float(np.mean([len(b["skills"][j]) for j in ix if b["skills"][j]])) if hs_.any() else float("nan")
            c = counts(ix, b["w"], b["skills"])
            row["top_skill"] = max(c, key=c.get) if c else ""
            row["top_skill_share"] = (max(c.values()) / b["w"][ix][hs_].sum()) if c else float("nan")
            qrows.append(row)

    def f(x, p=3):
        return "" if x is None or x != x else f"{x:.{p}f}"
    md = ["# Boards compared: composition and concentration", "",
          f"Equal-size comparison uses subsamples of {m:,} postings drawn by weight, {a.reps} repetitions. "
          "HHI on the whole board depends on the board's size and should not be compared across boards; use the equal-size columns.", ""]
    for d in dims:
        rs = [r for r in out_rows if r["dimension"] == d]
        md += [f"## {d}", "",
               "| board | postings with the field | labels | HHI whole board | effective number whole | top-10 share whole | HHI equal size (median) | 95% range | effective number equal size | top-10 share equal size |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        for r in rs:
            if r.get("note"):
                md.append(f"| {r['board']} | {r['coverage']:.1%} | {r['labels']} | field not recorded | | | | | | |")
            elif r.get("labels"):
                md.append(f"| {r['board']} | {r['coverage']:.1%} | {r['labels']} | {f(r['hhi_full'], 4)} | {r['eff_full']:.1f} | {r['top10_full']:.1%} | {f(r['hhi_sub'], 4)} | {f(r['hhi_sub_lo'], 4)} to {f(r['hhi_sub_hi'], 4)} | {r['eff_sub']:.1f} | {r['top10_sub']:.1%} |")
            else:
                md.append(f"| {r['board']} | 0.0% | 0 | | | | | | | |")
        md.append("")
    rn = [r for r in out_rows if r["dimension"] == "region" and r.get("hhi_norm") is not None]
    if rn:
        md += ["## Regions: HHI corrected for the number of regions", "",
               "A country with 38 regions has a low HHI even if one region dominates, so the HHI is rescaled to (HHI - 1/R) / (1 - 1/R), 0 = postings spread evenly over the R regions, 1 = all in one.", "",
               "| board | regions seen | HHI | normalised HHI |", "|---|---|---|---|"]
        for r in rn:
            md.append(f"| {r['board']} | {r['labels']} | {f(r['hhi_full'], 4)} | {f(r['hhi_norm'], 3)} |")
        md.append("")
    md += ["## Composition similarity between boards (Jensen-Shannon, 1 = identical)", "",
           "| board A | board B | dimension | shared labels | similarity | weight covered by shared labels (smaller side) |", "|---|---|---|---|---|---|"]
    for x in sim:
        md.append(f"| {x[0]} | {x[1]} | {x[2]} | {x[3]} | {x[4]:.3f} | {x[5]:.1%} |")
    md += ["", "## HHI by quarter (quarters with at least 300 taken postings)", "",
           "| board | quarter | taken | skills HHI | postings with skills | skills per posting | most common skill | its share of postings with skills | cluster HHI |", "|---|---|---|---|---|---|---|---|---|"]
    for r in qrows:
        md.append(f"| {r['board']} | {r['quarter']} | {r['taken']} | {f(r['skills'], 4)} | {r['skill_cov']:.1%} | {f(r['skills_per'], 1)} | {r['top_skill']} | {r['top_skill_share']:.1%} | {f(r['cluster'], 4)} |")
    md += ["", "## Field coverage by month (share of weighted postings with the field filled)", "",
           "| board | month | taken | skills | sectors | occupations |", "|---|---|---|---|---|---|"]
    for name, b in B.items():
        mo = np.array([d[:7] for d in b["day"]])
        for q in sorted(set(mo)):
            ix = np.where(mo == q)[0]
            tot = b["w"][ix].sum()
            cv = [float(b["w"][ix][np.array([len(b[d][j]) > 0 for j in ix])].sum() / tot) for d in ("skills", "sectors", "occupations")]
            md.append(f"| {name} | {q} | {len(ix)} | {cv[0]:.1%} | {cv[1]:.1%} | {cv[2]:.1%} |")
    Path(f"docs/boards_concentration{WT}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"docs/boards_concentration{WT}.md written")


if __name__ == "__main__":
    main()
