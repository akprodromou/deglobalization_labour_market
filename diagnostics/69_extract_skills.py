"""
Month 3, step 9: extract ESCO skills locally for every posting, with ONE threshold for all months.

Why: the Tracker's skill tags stop for jobbland.se in autumn 2025 (script 68 showed that the text carries skills
in 98-100% of the postings of those months, so the stop is not a threshold effect). A skill measure that crosses the
outage needs the same extractor in every month. This script runs the open-source esco-skill-extractor
(github.com/KonstantinosPetrakis/esco-skill-extractor) over the whole deduplicated corpus; the Tracker's own skills
are NOT used anywhere downstream (never mix the two).

Text = title and the first --max-chars characters of the description, boilerplate removed (as the tagger sees it).
Output: one JSON line per posting {"id", "day", "skills": [ESCO URIs]} in data/tagged/skills_local_t<threshold>.jsonl,
appended in batches, so an interrupted run (a Colab disconnect) is continued by running the same command again.

Primary run: --threshold 0.6 on the whole corpus (the tool's default; script 68: it reproduces the Tracker's number of
skills per posting in the tagged months). A sensitivity run at 0.45 needs the whole corpus too, because script 70's lift
divides by the share among ALL postings; --flagged exists only to look at the flagged postings' skills quickly (shares
within a channel are valid, lifts are not).

Colab (CPU is enough; a GPU makes it several times faster):
    !pip install -q esco-skill-extractor
    !python -m diagnostics.69_extract_skills --corpus <the merged or the four corpus files> --threshold 0.6
Copy data/tagged/skills_local_t0.60.jsonl to Drive when it finishes (and every half hour in a long run).
Test the pipeline without the package: --mock --limit 200.
"""

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus, posting_text
except ImportError:
    from corpus_io import load_corpus, posting_text


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


def real_extractor(threshold, device):
    import inspect
    from esco_skill_extractor import SkillExtractor
    params = inspect.signature(SkillExtractor.__init__).parameters
    names = [n for n in params if "threshold" in n and "occup" not in n]
    if not names:
        raise SystemExit("SkillExtractor has no skill threshold argument; parameters: " + ", ".join(params))
    kw = {names[0]: threshold}
    if "device" in params:
        kw["device"] = device
    return SkillExtractor(**kw)


class Mock:
    def get_skills(self, texts):
        return [[f"mock/{w}" for w in sorted({w for w in t.lower().split() if len(w) > 7})[:6]] for t in texts]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--threshold", type=float, default=0.6)
    ap.add_argument("--flagged", default=None, help="restrict to the postings of this flagged file")
    ap.add_argument("--max-chars", type=int, default=3000)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--device", default="auto")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    out = Path(args.out or f"data/tagged/skills_local_t{args.threshold:.2f}{'_flagged' if args.flagged else ''}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    rows, dup = load_all(args.corpus)
    if args.flagged:
        keep = {str(json.loads(l)["posting_id"]) for l in open(args.flagged, encoding="utf-8") if l.strip()}
        rows = [r for r in rows if str(r["item"]["id"]) in keep]
    if args.limit:
        rows = rows[:args.limit]
    done = set()
    if out.exists():
        for l in open(out, encoding="utf-8"):
            if l.strip():
                done.add(json.loads(l)["id"])
    todo = [r for r in rows if str(r["item"]["id"]) not in done]
    print(f"{len(rows):,} postings ({dup:,} duplicates removed); {len(done):,} already done; {len(todo):,} to do -> {out}")
    if not todo:
        return
    device = args.device
    if device == "auto":
        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            device = "cpu"
    ex = Mock() if args.mock else real_extractor(args.threshold, device)
    import time
    t0 = time.time()
    with open(out, "a", encoding="utf-8") as f:
        for i in range(0, len(todo), args.batch):
            chunk = todo[i:i + args.batch]
            skills = ex.get_skills([posting_text(r["item"], args.max_chars) for r in chunk])
            for r, s in zip(chunk, skills):
                f.write(json.dumps({"id": str(r["item"]["id"]), "day": r["day"], "skills": sorted(set(s))}) + "\n")
            f.flush()
            if (i // args.batch) % 20 == 0:
                el = time.time() - t0
                n = i + len(chunk)
                print(f"  {n:,}/{len(todo):,}  {el/60:.1f} min  (~{el/n*(len(todo)-n)/60:.0f} min left)")
    print("done")


if __name__ == "__main__":
    main()
