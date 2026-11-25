"""
Month 4 appendix table: Laplacian Score of the ESCO skills of one board, the 15 lowest and the 15 highest scores.

Uses exactly the functions of script 92 (knn_graph, laplacian_filter): same graph (k = 5, title embeddings, cosine), same
minimum of 20 postings, same score. A LOW score means the postings that carry the skill are neighbours in the title
embedding space (the skill is specific to a role); a score near 1 means the postings are scattered (generic skill).

For every skill the table also gives the most common cleaned title among the postings that carry it, and how large a
share of those postings has that title, so the reader can see why the score is low or high.

Reads (as script 92):  data/tagged/titles_<board>.jsonl, data/tagged/skills_local_full_<board>_t0.60.jsonl,
                       data/cluster/emb_<board>.npy (cache of script 92),
                       skill names: data/esco_dataset/skills_en.csv (preferredLabel; as script 115), else lexicon/skills.csv
Writes:                docs/ls_table_<board>.md          the two tables (Markdown, can be pasted into the appendix)
                       data/cluster/ls_scores_<board>.csv  every scored skill (skill id, label, postings, share, score, kept)

Run (project root, venv active; the embeddings are loaded from the cache, nothing is re-embedded):
    python -m diagnostics.126_ls_top_bottom --board jobbland
Variants:  --tukey     apply the Tukey frequency cut first (the D v3 input); default = no cut (the D v2 input)
           --top 15    rows per table;  --threshold 0.8 the keep threshold used in the "decision" column
"""

import argparse
import csv
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


def esc(s):
    return str(s).replace("|", "/").replace("\n", " ").strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True, help="jobbland | lesjeudis | jobsde")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--min-n", type=int, default=20, help="minimum postings of a skill (as in script 92)")
    ap.add_argument("--threshold", type=float, default=0.8)
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--tukey", action="store_true", help="remove the too-common skills first (D v3)")
    ap.add_argument("--show-skill", help="part of a skill name: list the most common titles of the postings that carry it")
    ap.add_argument("--show-titles", type=int, default=25, help="titles listed by --show-skill")
    ap.add_argument("--sample", type=int, default=10, help="random postings printed by --show-skill (title, start of the description, other skills)")
    ap.add_argument("--esco-csv", default="lexicon/skills.csv", help="fallback names: id,description (label + alternative labels + description)")
    ap.add_argument("--esco-dir", default="data/esco_dataset", help="folder with ESCO skills_en.csv (conceptUri, preferredLabel), as in script 115")
    ap.add_argument("--out", default="data/cluster")
    ap.add_argument("--docs", default="docs")
    a = ap.parse_args()

    cp = load_92()
    recs = cp.load_jsonl(f"data/tagged/titles_{a.board}.jsonl")
    ids = [r["id"] for r in recs]
    titles = [(cp.text_a(r) or "").strip().lower() for r in recs]
    sk = {r["id"]: r["skills"] for r in cp.load_jsonl(f"data/tagged/skills_local_full_{a.board}_t0.60.jsonl")}
    docs = [sk.get(i, []) for i in ids]
    n_post = len(docs)

    label = {}
    ec = Path(a.esco_dir) / "skills_en.csv"
    if ec.exists():                      # preferred label of the skill (short, readable)
        with open(ec, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                label[r["conceptUri"]] = r.get("preferredLabel", "")
        print(f"skill names: preferredLabel from {ec}")
    elif Path(a.esco_csv).exists():      # fallback: long text, cut in the table
        with open(a.esco_csv, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                label[r["id"]] = r.get("description", "")
        print(f"skill names: long description from {a.esco_csv} (put skills_en.csv in {a.esco_dir} for short names)")

    cut = None
    if a.tukey:
        cut = cp.tukey_cut(docs, min(5, a.min_n))   # fence base follows --min-n (1 = all items, as script 92 --min-items 1)
        cnt0 = Counter(t for x in docs for t in set(x))
        common = {t for t, c in cnt0.items() if c / n_post > cut}
        docs = [[t for t in x if t not in common] for x in docs]
        print(f"Tukey cut {cut:.3%}: {len(common)} skills removed")

    e = cp.embed_titles([cp.text_a(r) for r in recs], "intfloat/multilingual-e5-large", f"{a.out}/emb_{a.board}.npy", False)
    g = cp.knn_graph(e, a.k)
    keep, stats = cp.laplacian_filter(docs, g, a.min_n, a.threshold)
    print(f"{a.board}: {n_post:,} postings, {len(stats):,} skills scored, {len(keep):,} below {a.threshold}, t = {g['t']:.4f}")

    # most common title among the postings that carry each skill
    carrying = {t: [] for t in stats}
    for i, x in enumerate(docs):
        for t in set(x):
            if t in carrying:
                carrying[t].append(i)
    rows = []
    for t, (n, s) in stats.items():
        c = Counter(titles[i] for i in carrying[t] if titles[i])
        top_title, top_n = (c.most_common(1)[0] if c else ("", 0))
        rows.append({"id": t, "label": label.get(t, t.rsplit("/", 1)[-1]), "postings": n, "share": n / n_post, "score": s,
                     "kept": t in keep, "title": top_title, "title_share": top_n / max(1, n), "distinct": len(c)})
    rows.sort(key=lambda r: r["score"])

    Path(a.out).mkdir(parents=True, exist_ok=True)
    Path(a.docs).mkdir(parents=True, exist_ok=True)
    if a.show_skill:
        import re
        pos = {r["id"]: r for r in rows}
        hits = [r for r in rows if a.show_skill.lower() in r["label"].lower()]
        if not hits:
            print(f"no scored skill contains '{a.show_skill}'")
        for r in hits:
            c = Counter(titles[i] for i in carrying[r["id"]] if titles[i])
            out = [f"# {r['label']}", "",
                   f"{r['postings']:,} postings, {len(c):,} distinct titles, Laplacian Score {r['score']:.3f} "
                   f"({'kept' if r['kept'] else 'dropped'} at {a.threshold})", "",
                   "| title | postings | share of the skill's postings |", "|---|---|---|"]
            for t, n in c.most_common(a.show_titles):
                out.append(f"| {esc(t)[:80]} | {n:,} | {n / r['postings']:.1%} |")
            # length of the postings: script 69b stores the number of text windows (3,000 characters each) per posting
            rec = {str(x["id"]): x for x in cp.load_jsonl(f"data/tagged/skills_local_full_{a.board}_t0.60.jsonl")}
            if all("windows" in v for v in rec.values()):
                w_all = np.array([rec[str(i)].get("windows", 0) for i in ids if str(i) in rec])
                w_sk = np.array([rec[str(ids[i])].get("windows", 0) for i in carrying[r["id"]] if str(ids[i]) in rec])
                n_all = np.array([len(rec[str(i)]["skills"]) for i in ids if str(i) in rec])
                n_sk = np.array([len(rec[str(ids[i])]["skills"]) for i in carrying[r["id"]] if str(ids[i]) in rec])
                out += ["", f"Text windows per posting (median): {np.median(w_sk):.0f} for postings with this skill, {np.median(w_all):.0f} for all postings. "
                        f"ESCO skills per posting (median): {np.median(n_sk):.0f} with this skill, {np.median(n_all):.0f} for all postings."]
            if a.sample > 0:
                rng = np.random.default_rng(1)
                pick = rng.choice(carrying[r["id"]], min(a.sample, len(carrying[r["id"]])), replace=False)
                out += ["", f"{len(pick)} random postings with this skill (seed 1): title | start of the description | other ESCO skills of the posting", ""]
                for i in pick:
                    others = [label.get(t, t.rsplit("/", 1)[-1])[:30] for t in sk.get(ids[i], []) if t != r["id"]][:5]
                    out.append(f"- {esc(titles[i])[:70]} | {esc(recs[i].get('desc_start') or '')[:150]} | {'; '.join(others)}")
            txt = "\n".join(out) + "\n"
            print(txt)
            slug = re.sub(r"[^a-z0-9]+", "_", r["label"].lower()).strip("_")[:50]
            Path(f"{a.docs}/ls_skill_{slug}.md").write_text(txt, encoding="utf-8")
        return
    suffix = "_tukey" if a.tukey else ""
    with open(f"{a.out}/ls_scores_{a.board}{suffix}.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["skill_id", "label", "postings", "share", "laplacian_score", "kept", "most_common_title", "title_share", "distinct_titles"])
        for r in rows:
            w.writerow([r["id"], r["label"], r["postings"], f"{r['share']:.5f}", f"{r['score']:.4f}", int(r["kept"]),
                        r["title"], f"{r['title_share']:.3f}", r["distinct"]])

    def table(sel, start):
        out = ["| # | skill | postings | score | most common title (share of these postings) | decision |",
               "|---|---|---|---|---|---|"]
        for j, r in enumerate(sel, start):
            out.append(f"| {j} | {esc(r['label'])[:60]} | {r['postings']:,} | {r['score']:.3f} | "
                       f"{esc(r['title'])[:45]} ({r['title_share']:.0%}) | {'kept' if r['kept'] else 'dropped'} |")
        return out

    n = a.top
    sc = np.array([r["score"] for r in rows])
    md = [f"# Laplacian Score of the ESCO skills: {a.board}" + (" (after the Tukey cut)" if a.tukey else ""), "",
          f"{n_post:,} postings; {len(rows):,} skills were scored"
          + (f" (minimum {a.min_n} postings per skill); " if a.min_n > 1 else " (no minimum number of postings); ") +
          f"{len(keep):,} have a score below {a.threshold} and are kept. Score: minimum {sc.min():.3f}, median {np.median(sc):.3f}, "
          f"maximum {sc.max():.3f}. Graph: k = {a.k}, title embeddings, t = {g['t']:.4f}.", "",
          f"## The {n} lowest scores (postings of the skill are neighbours: specific skills)", ""]
    md += table(rows[:n], 1)
    md += ["", f"## The {n} highest scores (postings of the skill are scattered: generic skills)", ""]
    md += table(rows[-n:], len(rows) - n + 1)
    md += ["", f"## The {n} most frequent skills (rank by number of postings; no threshold involved)", ""]
    md += table(sorted(rows, key=lambda r: -r["postings"])[:n], 1)
    # skills by number of postings: how many are below the threshold, how concentrated on one title, how many distinct titles
    md += ["", f"## Skills by number of postings (minimum for scoring: {a.min_n})", "",
           "| postings per skill | skills | below threshold | median score | median share of the most common title | median distinct titles per posting |",
           "|---|---|---|---|---|---|"]
    for lo, hi in ((1, 2), (3, 4), (5, 9), (10, 19), (20, 49), (50, 199), (200, None)):
        sel = [r for r in rows if r["postings"] >= lo and (hi is None or r["postings"] <= hi)]
        if not sel:
            continue
        md.append(f"| {lo} to {hi} " if hi else f"| {lo} or more ")
        md[-1] += (f"| {len(sel):,} | {sum(r['kept'] for r in sel) / len(sel):.0%} | {np.median([r['score'] for r in sel]):.3f} | "
                   f"{np.median([r['title_share'] for r in sel]):.0%} | {np.median([r['distinct'] / r['postings'] for r in sel]):.2f} |")
    print("\n".join(md[-11:]))
    Path(f"{a.docs}/ls_table_{a.board}{suffix}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {a.docs}/ls_table_{a.board}{suffix}.md and {a.out}/ls_scores_{a.board}{suffix}.csv")


if __name__ == "__main__":
    main()
