"""
Month 4, step 1: extract ESCO skills locally from the FULL posting text, one threshold for every month and board.

Why: script 69 read the title and only the first --max-chars (3,000) characters of the description. On jobbland.se the
median description is 3,146 characters and 54% are longer than 3,000, so for more than half of the postings the late
part (where the duties usually sit, after the company description) never reached the extractor. This script reads the
whole text: the text that script 69 would build (title and description, boilerplate removed, via
corpus_io.posting_text) is cut into windows of at most --max-chars characters at paragraph, line or sentence
boundaries, the extractor runs on every window, and the skills of a posting are the union over its windows.

Same package, same threshold (0.6), same boilerplate removal as script 69, so the results are comparable with it.
Tracker skills are not used anywhere. The Month 3 file skills_local_t0.60.jsonl is NOT touched: script 70 used it.

Run ONE BOARD PER RUN (boards are never merged: duplicates are removed inside a board, as in the tagger):
    python -m diagnostics.69b_extract_skills_full --corpus <the board's corpus files> --out data/tagged/skills_local_full_<board>_t0.60.jsonl
Output: one JSON line per posting {"id", "day", "skills": [ESCO URIs], "windows": n}, appended in batches, so an
interrupted run (a Colab disconnect) is continued by running the same command again.
Options: --threshold 0.6  --max-chars 3000  --max-windows 8  --batch 64 (windows per call)  --limit N  --mock
A posting with more than --max-windows windows is cut after the last window; the count of such postings is printed.
Test the pipeline without the package: --mock --limit 200.
"""

import argparse
import json
import tempfile
import time
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus, posting_text
except ImportError:
    from corpus_io import load_corpus, posting_text

FULL = 10 ** 9


def split_windows(text, size):
    """Cut text into windows of at most `size` characters, preferably at a paragraph, line or sentence end."""
    text = (text or "").strip()
    if len(text) <= size:
        return [text] if text else []
    out, start = [], 0
    while start < len(text):
        if len(text) - start <= size:
            out.append(text[start:].strip())
            break
        seg = text[start:start + size]
        cut = -1
        for sep in ("\n\n", "\n", ". ", "; ", " "):
            k = seg.rfind(sep)
            if k >= size // 2:
                cut = k + len(sep)
                break
        if cut < 0:
            cut = size
        piece = text[start:start + cut].strip()
        if piece:
            out.append(piece)
        start += cut
    return out


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
    ap.add_argument("--max-chars", type=int, default=3000)
    ap.add_argument("--max-windows", type=int, default=8)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--device", default="auto")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows, dup = load_all(args.corpus)
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

    t0 = time.time()
    n_done = n_cut = n_windows = 0
    # postings are processed in groups; the windows of a group are sent to the extractor in batches of --batch
    group = max(1, args.batch // 2)
    with open(out, "a", encoding="utf-8") as f:
        for i in range(0, len(todo), group):
            chunk = todo[i:i + group]
            wins, owner = [], []
            for k, r in enumerate(chunk):
                w = split_windows(posting_text(r["item"], FULL), args.max_chars)
                if len(w) > args.max_windows:
                    n_cut += 1
                    w = w[:args.max_windows]
                wins.extend(w)
                owner.extend([k] * len(w))
            found = [set() for _ in chunk]
            for j in range(0, len(wins), args.batch):
                part = wins[j:j + args.batch]
                res = ex.get_skills(part)
                for o, s in zip(owner[j:j + args.batch], res):
                    found[o].update(s)
            for k, r in enumerate(chunk):
                f.write(json.dumps({"id": str(r["item"]["id"]), "day": r["day"], "skills": sorted(found[k]),
                                    "windows": owner.count(k)}) + "\n")
            f.flush()
            n_done += len(chunk)
            n_windows += len(wins)
            if (i // group) % 20 == 0:
                el = time.time() - t0
                print(f"  {n_done:,}/{len(todo):,}  {n_windows:,} windows  {el/60:.1f} min  "
                      f"(~{el/n_done*(len(todo)-n_done)/60:.0f} min left)")
    print(f"done; {n_cut:,} postings had more than {args.max_windows} windows and were cut after the last one")


if __name__ == "__main__":
    main()
