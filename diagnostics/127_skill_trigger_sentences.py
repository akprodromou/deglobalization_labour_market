"""
Month 4 check: WHICH SENTENCE of a posting makes the ESCO extractor return a given skill?

Why: the Laplacian Score table shows skills such as "improve chemical processes" (on junior audit consultant postings) and
"give interviews to media" (on retail, teacher, engineer postings). To describe the skill tagging correctly we need to see
what text triggers such a skill: duties text, or employer text (recruitment, culture, boilerplate).

What it does, for ONE board and ONE skill (part of its ESCO preferred label):
  1. finds the skill's URI in <esco-dir>/skills_en.csv and the postings of the board that carry it (script 69b output),
  2. takes --n of them at random (seed 1) and rebuilds their text exactly as script 69b does (corpus_io.posting_text, whole text),
  3. checks that the skill is found again when the extractor runs on the same text windows as script 69b ("reproduced"),
  4. cuts the text into sentences and runs the extractor on every sentence alone; the sentences that return the skill
     are printed, together with the other skills that the same sentence returns.
The extractor is called through its public get_skills only. It may split the text itself, so a skill found in a window can be
missing at sentence level ("not reproduced per sentence"): then the match needs more context than one sentence, which is a result too.

Needs (project root, venv active, on the machine with the raw corpus and the package esco-skill-extractor):
  data/raw/corpus_<board>_*.jsonl (the board's corpus files, as for script 69b), data/tagged/skills_local_full_<board>_t0.60.jsonl,
  data/esco_dataset/skills_en.csv

Run:
    python -m diagnostics.127_skill_trigger_sentences --corpus <the board's corpus files> --board jobbland --skill "improve chemical processes"
Options: --n 6  --threshold 0.6  --max-sentences 300  --seed 1  --mock (test without the package)
Writes docs/skill_trigger_<skill>.md
"""

import argparse
import csv
import importlib.util
import json
import re
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import posting_text
except ImportError:
    from corpus_io import posting_text


def load_69b():
    here = Path(__file__).resolve().parent
    for cand in (here / "69b_extract_skills_full.py", Path("69b_extract_skills_full.py")):
        if cand.exists():
            spec = importlib.util.spec_from_file_location("m69b", cand)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    raise SystemExit("69b_extract_skills_full.py not found next to this script")


def sentences(text, max_n):
    parts = re.split(r"(?<=[.!?:;])\s+|\n+", text or "")
    out = [p.strip() for p in parts if len(p.strip()) >= 12]
    return [s[:1000] for s in out[:max_n]]


def esc(s):
    return str(s).replace("|", "/").replace("\n", " ").strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True, help="the board's corpus files (as for script 69b)")
    ap.add_argument("--board", required=True)
    ap.add_argument("--skill", required=True, help="part of the ESCO preferred label")
    ap.add_argument("--n", type=int, default=6, help="postings with the skill to examine")
    ap.add_argument("--threshold", type=float, default=0.6)
    ap.add_argument("--max-sentences", type=int, default=300)
    ap.add_argument("--max-chars", type=int, default=3000, help="window size, as in script 69b")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--esco-dir", default="data/esco_dataset")
    ap.add_argument("--skills", help="default data/tagged/skills_local_full_<board>_t0.60.jsonl")
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--mock", action="store_true")
    a = ap.parse_args()

    m69 = load_69b()
    label = {}
    with open(Path(a.esco_dir) / "skills_en.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            label[r["conceptUri"]] = r.get("preferredLabel", "")
    want = a.skill.lower().strip()
    exact = [u for u, l in label.items() if l.lower().strip() == want]
    hits = exact or [u for u, l in label.items() if want in l.lower()]
    if not hits:
        raise SystemExit(f"no ESCO skill with '{a.skill}' in its preferred label")
    uri = hits[0]
    print(f"skill: {label[uri]}  ({uri})" + (f"  [{len(hits)} labels contain the text, the first is used]" if len(hits) > 1 and not exact else ""))

    sk_file = a.skills or f"data/tagged/skills_local_full_{a.board}_t0.60.jsonl"
    stored = {}
    with open(sk_file, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                stored[str(r["id"])] = r
    carriers = [i for i, r in stored.items() if uri in r["skills"]]
    print(f"{len(carriers):,} postings of {a.board} carry the skill")

    rows, dup = m69.load_all(a.corpus)
    by_id = {str(r["item"]["id"]): r for r in rows}
    carriers = [i for i in carriers if i in by_id]
    print(f"{len(carriers):,} of them found in the corpus files")
    if not carriers:
        raise SystemExit("no carrier found in the corpus: check --corpus and the ids")
    rng = np.random.default_rng(a.seed)
    pick = list(rng.choice(carriers, min(a.n, len(carriers)), replace=False))

    device = "cpu"
    try:
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        pass
    ex = m69.Mock() if a.mock else m69.real_extractor(a.threshold, device)

    md = [f"# Which sentences return the skill \"{label[uri]}\"? ({a.board}, threshold {a.threshold})", "",
          f"{len(carriers):,} postings carry the skill; {len(pick)} random ones (seed {a.seed}) are examined. "
          "The extractor is run on the sentences of each posting one by one; sentences that return the skill are listed "
          "with the other skills the same sentence returns.", ""]
    n_repro = n_sent_repro = 0
    for pid in pick:
        r = by_id[pid]
        item = r["item"]
        title = str(item.get("title", ""))[:90]
        text = posting_text(item, m69.FULL)
        wins = m69.split_windows(text, a.max_chars)[:8]
        win_res = ex.get_skills(wins) if wins else []
        repro = any(uri in set(x) for x in win_res)
        sents = sentences(text, a.max_sentences)
        res = ex.get_skills(sents) if sents else []
        trig = [(s, x) for s, x in zip(sents, res) if uri in set(x)]
        n_repro += int(repro)
        n_sent_repro += int(bool(trig))
        md += [f"## {esc(title)} (id {pid}; {len(text):,} characters; {len(sents)} sentences; stored skills: {len(stored[pid]['skills'])})", "",
               f"Skill found again with the windows of script 69b: **{'yes' if repro else 'no'}**. "
               f"Sentences that return it when run alone: **{len(trig)}**."
               + ("" if trig or not repro else " The skill needs more context than one sentence."), ""]
        for s, x in trig[:5]:
            others = [label.get(u, u.rsplit("/", 1)[-1])[:35] for u in x if u != uri][:6]
            md.append(f"- \"{esc(s)[:350]}\"  \n  other skills of this sentence: {'; '.join(others) if others else 'none'}")
        md.append("")
        print(f"{esc(title)[:60]:60s} windows reproduce: {'yes' if repro else 'no ':3s} sentences with the skill: {len(trig)}")
    md += ["", f"Summary: found again with windows in {n_repro} of {len(pick)} postings; at least one single sentence returns the skill in {n_sent_repro} of {len(pick)}."]
    Path(a.docs).mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "_", label[uri].lower()).strip("_")[:50]
    out = Path(a.docs) / f"skill_trigger_{slug}.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
