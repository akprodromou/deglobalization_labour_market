"""
Month 4: infer a job title from the description for postings that have none (Qwen 2.5 7B through Ollama, runs on Colab).

Two groups are processed in one run:
  inferred    every posting without a title (has_title false in titles_<label>.jsonl of script 90)
  validation  a random sample of postings WITH a title, drawn from --val-from/--val-to, whose title is hidden from the model.
              Script 99b compares the inferred title with the real one, so the quality of the method is measured on postings
              where the answer is known.
The model sees up to --chars characters of the description and nothing else (no title, employer or place field). The prompt tells it
to skip the employer introduction and to answer UNKNOWN when the text does not say what the job is. Decoding is greedy (temperature 0).

Output (one line per posting, appended, so an interrupted run continues where it stopped):
  data/tagged/inferred_titles_<label>.jsonl
  {"id", "day", "kind": "inferred" | "validation", "title_inferred", "confidence", "true_title" (validation only)}

Run on Colab after starting Ollama (see colab_infer_titles.ipynb):
    python -m diagnostics.99_infer_titles --label jobbland --corpus data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl
Quick test of 20 postings per group:  add  --limit 20
Pipeline test without a model:         add  --backend mock
"""

import argparse
import json
import random
import re
import tempfile
import time
import urllib.request
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

PROMPT = """Below is the text of a job advertisement whose title field is missing. Write the title the employer would have put in the title field.

Rules:
- Name the role that is being recruited, in English, in 2 to 6 words (for example "Software Tester", "Quality Technician", "Head of Department, Social Administration", "Specialist Nurse").
- Do not include the employer, the place, working hours, gender markers such as "m/f/d", or the word "job".
- The text often starts with an introduction of the employer or a general sentence. Ignore it and look for the role in phrases such as "we are looking for", "as a", "the position", "your tasks", "job duties".
- If the text is about several different roles, or does not say what the job is, answer UNKNOWN as the title.

Answer with JSON only, in this form: {{"title": "...", "confidence": "high" or "medium" or "low"}}

Advertisement:
\"\"\"
{text}
\"\"\""""


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


def ask_ollama(prompt, model, url):
    body = json.dumps({"model": model, "stream": False, "format": "json",
                       "options": {"temperature": 0, "num_predict": 60, "num_ctx": 4096},
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(url.rstrip("/") + "/api/chat", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.loads(r.read())["message"]["content"]


def ask_mock(prompt, *_):
    m = re.search(r'looking for (?:an? )?([A-Za-z ]{3,40})', prompt)
    return json.dumps({"title": (m.group(1).strip().title() if m else "UNKNOWN"), "confidence": "low"})


def parse(answer):
    try:
        d = json.loads(answer)
        t, c = str(d.get("title", "")).strip(), str(d.get("confidence", "")).strip().lower()
    except Exception:
        m = re.search(r'"title"\s*:\s*"([^"]*)"', answer or "")
        t, c = (m.group(1).strip() if m else ""), ""
    if not t or t.upper() == "UNKNOWN":
        return "UNKNOWN", c if c in ("high", "medium", "low") else "low"
    return t[:120], c if c in ("high", "medium", "low") else "low"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--label", required=True)
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--titles")
    ap.add_argument("--out")
    ap.add_argument("--backend", choices=["ollama", "mock"], default="ollama")
    ap.add_argument("--model", default="qwen2.5:7b")
    ap.add_argument("--url", default="http://localhost:11434")
    ap.add_argument("--chars", type=int, default=3000)
    ap.add_argument("--validate", type=int, default=400, help="titled postings used as validation")
    ap.add_argument("--val-from", default="2025-10-01")
    ap.add_argument("--val-to", default="2026-03-31")
    ap.add_argument("--limit", type=int, default=0, help="postings per group (test run)")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    titles_p = a.titles or f"data/tagged/titles_{a.label}.jsonl"
    out_p = a.out or f"data/tagged/inferred_titles_{a.label}.jsonl"
    meta = {}
    for l in open(titles_p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            meta[str(r["id"])] = r
    rows, dup = load_all(a.corpus)
    byid = {str(r["item"]["id"]): r for r in rows}
    todo_inf = [i for i, m in meta.items() if not m.get("has_title", True) and i in byid]
    pool = [i for i, m in meta.items() if m.get("has_title", True) and (m.get("title_clean") or m.get("title")) and i in byid
            and a.val_from <= byid[i]["day"] <= a.val_to]
    rnd = random.Random(a.seed)
    todo_val = rnd.sample(sorted(pool), min(a.validate, len(pool)))
    todo_inf.sort()
    if a.limit:
        todo_inf, todo_val = todo_inf[:a.limit], todo_val[:a.limit]
    print(f"title-less postings: {len(todo_inf):,}; validation postings (title hidden): {len(todo_val):,} drawn from {len(pool):,} titled in {a.val_from} to {a.val_to}")
    done = set()
    if Path(out_p).exists():
        for l in open(out_p, encoding="utf-8"):
            if l.strip():
                done.add(json.loads(l)["id"])
        print(f"{len(done):,} postings already in {out_p}, skipped")
    Path(out_p).parent.mkdir(parents=True, exist_ok=True)
    jobs = [(i, "validation") for i in todo_val] + [(i, "inferred") for i in todo_inf]
    jobs = [(i, k) for i, k in jobs if i not in done]
    ask = ask_ollama if a.backend == "ollama" else ask_mock
    t0 = time.time()
    with open(out_p, "a", encoding="utf-8") as f:
        for n, (i, kind) in enumerate(jobs, 1):
            desc = re.sub(r"\s+", " ", byid[i]["item"].get("description") or "").strip()[:a.chars]
            if not desc:
                title, conf = "UNKNOWN", "low"
            else:
                try:
                    title, conf = parse(ask(PROMPT.format(text=desc), a.model, a.url))
                except Exception as e:
                    print("error on", i, e)
                    continue
            rec = {"id": i, "day": byid[i]["day"], "kind": kind, "title_inferred": title, "confidence": conf}
            if kind == "validation":
                rec["true_title"] = meta[i].get("title_clean") or meta[i].get("title")
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            if n % 50 == 0 or n == len(jobs):
                el = time.time() - t0
                print(f"{n:,}/{len(jobs):,} done, {el / 60:.1f} min, about {(len(jobs) - n) * el / n / 60:.1f} min left", flush=True)
    print("written", out_p)


if __name__ == "__main__":
    main()
