"""
Month 3, step 3a: tag every lexicon-flagged posting by channel and intensity with an LLM.

1. Flag: a posting is flagged if it contains at least one term of the lexicon
   (lexicon/lexicon.csv, or the seed list if the lexicon is not built yet).
   The flagged set is written once to data/tagged/flagged_<corpus>.jsonl, so
   that later changes to the lexicon cannot silently change which postings
   the tags and the annotation sample refer to (use --refresh to rebuild it).
2. Tag: for each flagged posting the prompt of prompts/tagging_v6.txt
   (a system part with the channel and intensity definitions and a user part with
   the title, the matched terms and the text) is sent to the model, which
   answers with JSON: channel, intensity, evidence. Temperature 0, fixed seed.
   The text sent is the title, the first --max-chars of the description and,
   when a matched term lies further in, short passages around it.
3. Save: one JSON line per posting is appended to
   data/tagged/tags_<model>_<prompt>.jsonl as soon as it is answered, so a run
   that stops (a Colab session that disconnects, say) is resumed by running the
   same command again: postings already in the file are skipped. Answers that
   are not valid are retried once and then stored with ok = false.

Pilot (--pilot N): before the full run, tag N flagged postings (default idea: 20)
   drawn with a fixed seed, round-robin over the channel of the first lexicon term found,
   so that every channel is represented. It writes
       data/tagging/pilot_sheet.csv   what you annotate BLIND (channel, intensity, note empty;
                                      an existing sheet is never overwritten)
       data/tagged/tags_<model>_<prompt>_pilot.jsonl   the model's tags
       docs/tagging_pilot.md          each posting with the model's tag; if pilot_sheet.csv
                                      has been filled, your tag beside it and the agreement
   Use it to check that the channel and intensity definitions work before tagging everything.

Backends (--backend)
    ollama      a local Ollama server (the brief names Mistral 7B or Qwen 2.5):
                --model qwen2.5:7b   or   --model mistral
    anthropic   the Claude API (the brief allows it): --model claude-haiku-4-5-20251001
                needs the `anthropic` package and ANTHROPIC_API_KEY in the environment
    mock        no model: a deterministic fake answer from the matched terms, only
                to test the pipeline (the output must not be analysed)

Colab (GPU runtime) recipe for Ollama, run in notebook cells:
    !apt-get -qq install -y zstd
    !curl -fsSL https://ollama.com/install.sh | sh
    import subprocess; subprocess.Popen(["ollama", "serve"])      # keep running
    !ollama pull qwen2.5:7b
    !python -m diagnostics.58_tag_postings --backend ollama --model qwen2.5:7b
Mount Drive (or upload the repo and the corpus) first, and write the outputs
to Drive so that they survive a disconnect.

Run (project root):
    python -m diagnostics.58_tag_postings --backend ollama --model qwen2.5:7b
    python -m diagnostics.58_tag_postings --backend mock --limit 50      # pipeline test
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus, posting_text, strip_boilerplate
    from diagnostics.lexicon_io import read_lexicon, compile_lexicon, match_terms, context
except ImportError:
    from corpus_io import load_corpus, posting_text, strip_boilerplate
    from lexicon_io import read_lexicon, compile_lexicon, match_terms, context

CORPUS = Path("data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl")
LEXICON = Path("lexicon/lexicon.csv")
SEEDS = Path("lexicon/seed_lexicon.csv")
PROMPT = Path("prompts/tagging_v6.txt")
OUT_DIR = Path("data/tagged")
CHANNELS = ["reshoring", "defense", "critical materials", "energy security",
            "trade compliance", "diversification", "none"]
INTENSITY = ["high", "medium", "low", "none"]
SEARCH_CHARS = 6000
# Answers that name a sector from the channel definitions instead of a channel are mapped to the channel
# the definition puts the sector in (recorded as mapped_from in the tag).
SECTOR_CHANNEL = {"aerospace": "reshoring", "space": "reshoring", "semiconductors": "reshoring",
                  "semiconductor": "reshoring", "batteries": "reshoring", "battery": "reshoring",
                  "satellites": "reshoring", "nuclear": "energy security", "nuclear power": "energy security",
                  "electricity grid": "energy security", "mining": "critical materials"}


def load_prompt(path):
    raw = path.read_text(encoding="utf-8")
    m = re.search(r"### SYSTEM\s*(.*?)\s*### USER\s*(.*)\s*$", raw, re.S)
    if not m:
        sys.exit(f"{path}: needs a '### SYSTEM' and a '### USER' part")
    return m.group(1).strip(), m.group(2).strip()


def build_text(item, matched, max_chars):
    """First max_chars of the description plus passages around terms that lie beyond it."""
    desc = re.sub(r"[ \t]+", " ", strip_boilerplate(item.get("description") or "")).strip()
    body = desc[:max_chars]
    extra = []
    for m in matched:
        pos = desc.lower().find(m.lower())
        if pos >= max_chars - 100:
            extra.append(context(desc, m, 250))
        if len(extra) == 3:
            break
    if extra:
        body += "\n[...]\n" + "\n[...]\n".join(extra)
    return body


def parse_answer(raw):
    """Channel, intensity, evidence from the model's answer, or None if invalid."""
    m = re.search(r"\{.*\}", raw or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    ch = str(d.get("channel", "")).strip().lower().replace("_", " ").replace("defence", "defense")
    mapped = None
    if ch not in CHANNELS and ch in SECTOR_CHANNEL:     # the model named the sector instead of the channel
        mapped, ch = ch, SECTOR_CHANNEL[ch]
    it = str(d.get("intensity", "")).strip().lower()
    if ch not in CHANNELS or it not in INTENSITY:
        return None
    if ch == "none":
        it = "none"
    elif it == "none":
        return None
    out = {"channel": ch, "intensity": it, "evidence": str(d.get("evidence", ""))[:300]}
    if mapped:
        out["mapped_from"] = mapped
    return out


def make_caller(backend, model, url, timeout):
    if backend == "ollama":
        import requests

        def call(system, user):
            r = requests.post(url.rstrip("/") + "/api/chat", timeout=timeout, json={
                "model": model, "stream": False, "format": "json",
                "options": {"temperature": 0, "seed": 0, "num_ctx": 8192, "num_predict": 200},
                "messages": [{"role": "system", "content": system},
                             {"role": "user", "content": user}]})
            r.raise_for_status()
            return r.json()["message"]["content"]
        return call
    if backend == "anthropic":
        import anthropic

        client = anthropic.Anthropic()

        def call(system, user):
            msg = client.messages.create(model=model, max_tokens=200, temperature=0, system=system,
                                         messages=[{"role": "user", "content": user}])
            return msg.content[0].text
        return call

    def call(system, user):                     # mock
        m = re.search(r"found in the posting: (.*)", user)
        terms = m.group(1) if m else ""
        for ch, words in (("trade compliance", ("cbam", "export control", "customs")),
                          ("reshoring", ("nearshoring", "friend")),
                          ("critical materials", ("critical raw", "rare earth")),
                          ("energy security", ("energy security",)),
                          ("defense", ("defence", "defense")),
                          ("diversification", ("trade agreement",))):
            if any(w in terms.lower() for w in words):
                return json.dumps({"channel": ch, "intensity": ["low", "medium", "high"][len(user) % 3],
                                   "evidence": "mock"})
        return json.dumps({"channel": "none", "intensity": "none", "evidence": "mock"})
    return call


def pick_pilot(flagged, ch_of, n, seed=0):
    """n flagged postings, round-robin over the channel of the first matched lexicon term."""
    import random
    rng = random.Random(seed)
    groups = {}
    for r in flagged:
        first = next((ch_of[t] for t in r["terms"] if t in ch_of), "other")
        groups.setdefault(first, []).append(r)
    for g in groups.values():
        rng.shuffle(g)
    order = sorted(groups)
    picked = []
    while len(picked) < n and any(groups.values()):
        for ch in order:
            if groups[ch] and len(picked) < n:
                picked.append(groups[ch].pop())
    return picked


def pilot_sheet(picked, by_id, path):
    import csv
    if path.exists():
        print(f"{path} exists; left unchanged (it may hold your annotations)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["posting_id", "title", "terms_found", "text", "channel", "intensity", "note"])
        for fl in picked:
            it = by_id[fl["posting_id"]]["item"]
            w.writerow([fl["posting_id"], (it.get("title") or "").strip(), "; ".join(fl["terms"]),
                        build_text(it, fl["matched"], 1800), "", "", ""])
    print(f"Pilot sheet for blind annotation: {path}")


def pilot_report(picked, by_id, tags_path, sheet_path, report_path):
    import csv
    tags = {}
    for line in open(tags_path, encoding="utf-8"):
        if line.strip():
            d = json.loads(line)
            tags[d["posting_id"]] = d
    mine = {}
    if sheet_path.exists():
        for r in csv.DictReader(open(sheet_path, encoding="utf-8-sig")):
            if r["channel"].strip():
                mine[r["posting_id"]] = (r["channel"].strip().lower(), r["intensity"].strip().lower())
    lines = ["# Tagging pilot", "",
             f"{len(picked)} flagged postings; model tags from `{tags_path.name}`.", ""]
    same_ch = same_both = n_mine = 0
    body = []
    for k, fl in enumerate(picked, 1):
        it = by_id[fl["posting_id"]]["item"]
        t = tags.get(fl["posting_id"], {})
        mt = f"{t.get('channel')} / {t.get('intensity')}" if t.get("ok") else "invalid answer"
        you = ""
        if fl["posting_id"] in mine:
            n_mine += 1
            c, i = mine[fl["posting_id"]]
            you = f" · **you:** {c} / {i or '-'}"
            same_ch += c == t.get("channel")
            same_both += (c == t.get("channel") and (i or "none") == t.get("intensity"))
        body += [f"## {k}. {(it.get('title') or '').strip()}", "",
                 f"Terms: {', '.join(fl['terms'])}  ", f"**model:** {mt}{you}  ",
                 f"Evidence: {t.get('evidence', '')}", "",
                 "> " + re.sub(r"\s+", " ", build_text(it, fl["matched"], 600)), ""]
    if n_mine:
        lines += [f"Your tags for {n_mine} postings: same channel {same_ch} ({same_ch / n_mine:.0%}); "
                  f"same channel and intensity {same_both} ({same_both / n_mine:.0%}).", "",
                  "Read the disagreements: they show which definition in the prompt or the guide is unclear.", ""]
    else:
        lines += ["No annotations found in the pilot sheet yet; annotate it blind, then rerun the same command "
                  "to add the comparison.", ""]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines + body), encoding="utf-8")
    print(f"Wrote {report_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", default=str(CORPUS))
    ap.add_argument("--lexicon", default=None, help="default: lexicon/lexicon.csv, else the seed list")
    ap.add_argument("--prompt", default=str(PROMPT))
    ap.add_argument("--backend", default="ollama", choices=["ollama", "anthropic", "mock"])
    ap.add_argument("--model", default="qwen2.5:7b")
    ap.add_argument("--url", default="http://localhost:11434")
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--max-chars", type=int, default=3000)
    ap.add_argument("--limit", type=int, default=0, help="tag at most this many (for tests)")
    ap.add_argument("--refresh", action="store_true", help="rebuild the flagged set")
    ap.add_argument("--pilot", type=int, default=0,
                    help="tag only a stratified pilot of this many postings and write the pilot sheet and report")
    args = ap.parse_args()

    lex_path = Path(args.lexicon) if args.lexicon else (LEXICON if LEXICON.exists() else SEEDS)
    if lex_path == SEEDS:
        print(f"NOTE: {LEXICON} not found, using the seed list {SEEDS}")
    rows, dropped = load_corpus(Path(args.corpus))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    flag_path = OUT_DIR / f"flagged_{Path(args.corpus).stem}.jsonl"

    if flag_path.exists() and not args.refresh:
        flagged = [json.loads(l) for l in open(flag_path, encoding="utf-8") if l.strip()]
        print(f"Flagged set read from {flag_path}: {len(flagged):,} postings")
    else:
        lex = compile_lexicon(read_lexicon(lex_path))
        flagged = []
        t0 = time.time()
        for k, r in enumerate(rows):
            hits = match_terms(lex, posting_text(r["item"], SEARCH_CHARS))
            if hits:
                flagged.append({"posting_id": str(r["item"]["id"]), "day": r["day"],
                                "terms": sorted({row["term"] for row, _ in hits}),
                                "matched": sorted({m for _, m in hits}),
                                "lexicon": str(lex_path)})
            if (k + 1) % 5000 == 0:
                print(f"  matched {k + 1:,} / {len(rows):,} postings ({time.time() - t0:.0f} s)")
        with open(flag_path, "w", encoding="utf-8") as f:
            for r in flagged:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"{len(flagged):,} of {len(rows):,} postings contain a lexicon term "
              f"({len(flagged) / len(rows):.1%}); written to {flag_path}")

    system, user_t = load_prompt(Path(args.prompt))
    prompt_name = Path(args.prompt).stem
    model_tag = re.sub(r"[^\w.-]+", "_", args.model if args.backend != "mock" else "mock")
    out_path = OUT_DIR / f"tags_{model_tag}_{prompt_name}{'_pilot' if args.pilot else ''}.jsonl"
    by_id = {str(r["item"]["id"]): r for r in rows}
    picked = None
    if args.pilot:
        ch_of = {r["term"]: r["channel"] for r in read_lexicon(lex_path)}
        picked = pick_pilot(flagged, ch_of, args.pilot)
        flagged = picked
        pilot_sheet(picked, by_id, Path("data/tagging/pilot_sheet.csv"))
    done = set()
    if out_path.exists():
        for line in open(out_path, encoding="utf-8"):
            if line.strip():
                done.add(json.loads(line)["posting_id"])
    todo = [r for r in flagged if r["posting_id"] not in done]
    if args.limit:
        todo = todo[:args.limit]
    print(f"{len(done):,} already tagged in {out_path}; {len(todo):,} to do "
          f"(backend {args.backend}, model {args.model}, prompt {prompt_name})")
    if not todo:
        if picked:
            pilot_report(picked, by_id, out_path, Path("data/tagging/pilot_sheet.csv"), Path("docs/tagging_pilot.md"))
        return

    call = make_caller(args.backend, args.model, args.url, args.timeout)
    t0, bad = time.time(), 0
    with open(out_path, "a", encoding="utf-8") as out:
        for n, fl in enumerate(todo, 1):
            item = by_id[fl["posting_id"]]["item"]
            user = user_t.format(title=(item.get("title") or "").strip(),
                                 terms=", ".join(fl["terms"]),
                                 text=build_text(item, fl["matched"], args.max_chars))
            ans, raw = None, ""
            for attempt in range(2):
                try:
                    raw = call(system, user if attempt == 0 else
                               user + "\n\nReply with the JSON object only.")
                    ans = parse_answer(raw)
                except Exception as e:          # network, server or API error
                    raw = f"ERROR: {e}"
                    time.sleep(2)
                if ans:
                    break
            if not ans:
                bad += 1
            rec = {"posting_id": fl["posting_id"], "ok": bool(ans), "model": args.model if args.backend != "mock" else "mock",
                   "backend": args.backend, "prompt": prompt_name, "terms": fl["terms"],
                   "raw": raw[:600], **(ans or {"channel": None, "intensity": None, "evidence": ""})}
            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out.flush()
            if n % 25 == 0 or n == len(todo):
                el = time.time() - t0
                print(f"  {n:,} / {len(todo):,}  ({el / n:.1f} s each, about "
                      f"{el / n * (len(todo) - n) / 60:.0f} min left; {bad} invalid)")
    print(f"Done. {out_path}")
    if picked:
        pilot_report(picked, by_id, out_path, Path("data/tagging/pilot_sheet.csv"), Path("docs/tagging_pilot.md"))


if __name__ == "__main__":
    main()
