"""
Month 3, source choice: how common is deglobalization vocabulary in each Skillab
source? Counts from the API's keyword filter, no posting text is downloaded.

For each source one reference window (a month by default, see WINDOWS) is
probed with requests of one row each; the server's `count` is what is used.

  1. total          postings in the window (no keyword)
  2. language words one very common function word per language (the, und, les,
                    het, och, και): count / total shows roughly which languages a
                    source's text is in
  3. index check    `manager` against `manag`, `engineer` against `engin`: if the
                    stem returns clearly more, the index is stemmed and counts for
                    unstemmed words are LOWER BOUNDS (week2 report, 9.10 items 4-5)
  4. terms          every term of lexicon/probe_terms.csv. A single word is one
                    request. For a multi-word term the filter cannot tell a phrase
                    from its words: in the first real run the phrase and the
                    `and` of its words returned identical counts in every case. So
                    one request is made (the words with `and`) and the count is
                    "all words anywhere in the posting, any order", an upper bound
                    that says little ("industrial" and "policy" in a posting that
                    mentions a privacy policy). Trust single words.

Result: hits and hits per 10,000 postings, per term and source. Read it with the
limits the week 2 report documents for this filter: it matches whole tokens only
(no stemming of the query), may index stemmed words in some sources, finds
a slash- or full-stop-joined word only as a whole, and says nothing about words
in the part of the posting it does not index. A zero is therefore weak evidence,
a high count strong evidence. Use the table to RANK sources, not to report
prevalences. One window per source is not a time series.

If the corpus file is present, the same English single words are also counted in
the local jobbland.se sample for the same month, to show how far the server's
count and a count on the text itself agree.

Each answer is written to data/raw/source_term_probe.json as soon as it arrives;
run the same command again to resume (failed requests are retried, answered ones
skipped). Slow sources (eures-escox answered one-row requests in 65 to 71 seconds
in the audit) can be run on their own: --sources eures-escox

Usage, from the repo root:
    python -m diagnostics.61_source_term_probe
    python -m diagnostics.61_source_term_probe --sources jobbland.se lesjeudis.com
    python -m diagnostics.61_source_term_probe --window eures-escox=2025-12-01:2025-12-31
    python -m diagnostics.61_source_term_probe --report-only     # rebuild the report from the saved answers
    python -m diagnostics.61_source_term_probe --check-only --sources eures-escox --window eures-escox=2025-09-01:2025-09-30

Output: docs/source_term_probe.md (no posting text; can be committed)
"""

import argparse
import csv
import json
import re
import time
from pathlib import Path

TERMS = Path("lexicon/probe_terms.csv")
RAW = Path("data/raw/source_term_probe.json")
REPORT = Path("docs/source_term_probe.md")
CORPUS = Path("data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl")

# source -> (from, to): one month with a large, known count (week 2 report, 9.3 and 9.6).
# Change with --window; an empty or timing-out window is reported, not hidden.
WINDOWS = {
    "jobbland.se": ("2026-03-01", "2026-03-31"),
    "lesjeudis.com": ("2025-06-01", "2025-06-30"),
    "kariera.gr": ("2026-03-01", "2026-03-31"),
    "eures": ("2025-12-01", "2025-12-31"),
    "eures-escox": ("2026-01-01", "2026-01-31"),
    "jobs.de": ("2024-10-01", "2024-10-31"),
    "kariera.fr": ("2024-10-01", "2024-10-31"),
}
LANG_WORDS = [("en", "the"), ("de", "und"), ("fr", "les"), ("nl", "het"), ("sv", "och"), ("el", "και")]
STEM_CHECKS = [("manager", "manag"), ("engineer", "engin")]


def read_terms(path):
    seen, out = set(), []
    for r in csv.DictReader(open(path, encoding="utf-8-sig", newline="")):
        t = (r.get("term") or "").strip()
        if t and t.lower() not in seen:
            seen.add(t.lower())
            out.append({"term": t, "language": (r.get("language") or "").strip(),
                        "channel": (r.get("channel") or "").strip(), "note": (r.get("note") or "").strip()})
    return out


def plan(terms):
    """(kind, label, keywords, logic) for every request after the total."""
    reqs = []
    for lang, w in LANG_WORDS:
        reqs.append(("lang", f"{lang}:{w}", [w], None))
    for a, b in STEM_CHECKS:
        reqs.append(("stem", a, [a], None))
        reqs.append(("stem", b, [b], None))
    for t in terms:
        words = t["term"].split()
        if len(words) == 1:
            reqs.append(("term", t["term"], [t["term"]], None))
        else:
            reqs.append(("and", t["term"], words, "and"))
    return reqs


def ask(client, source, lo, hi, kws, logic, timeout):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [source], "min_upload_date": lo, "max_upload_date": hi}
    if kws:
        form["keywords"] = kws
    if logic:
        form["keywords_logic"] = logic
    t0 = time.time()
    r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": 1, "page_size": 1},
                            data=form, timeout=timeout)
    dt = time.time() - t0
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:100]}")
    c = r.json().get("count")
    if c is None:
        raise RuntimeError("no 'count' in the answer")
    return int(c), dt


def key(source, lo, hi, kind, label):
    return f"{source}|{lo}|{hi}|{kind}|{label}"


def run(args, windows, terms):
    from skillab_client import SkillabClient
    client = SkillabClient()
    RAW.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(RAW.read_text(encoding="utf-8")) if RAW.exists() else {}
    reqs = plan(terms)
    if args.check_only:
        reqs = [r for r in reqs if r[0] in ("lang", "stem")]
    for source, (lo, hi) in windows.items():
        print(f"\n=== {source}  {lo} .. {hi}")
        todo = [("total", "total", [], None)] + reqs
        for n, (kind, label, kws, logic) in enumerate(todo, 1):
            k = key(source, lo, hi, kind, label)
            if k in data and "count" in data[k]:
                continue
            ans = None
            for attempt in range(args.retries + 1):
                try:
                    c, dt = ask(client, source, lo, hi, kws, logic, args.timeout)
                    ans = {"count": c, "seconds": round(dt, 1)}
                    break
                except Exception as exc:
                    ans = {"error": str(exc)[:200]}
                    time.sleep(5 * (attempt + 1))
            data[k] = ans
            RAW.write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")
            shown = ans.get("count", ans.get("error"))
            print(f"  [{n}/{len(todo)}] {kind:6s} {label[:38]:38s} {shown}")
            if kind == "total":
                if "count" not in ans:
                    print("  window total not available: source skipped (re-run later, or try another window)")
                    break
                if ans["count"] == 0:
                    print("  window is empty: source skipped (use --window to pick another)")
                    break
            time.sleep(args.pause)
    return data


def cell(data, source, win, kind, label, total):
    a = data.get(key(source, win[0], win[1], kind, label))
    if not a or "count" not in a:
        return None
    c = a["count"]
    rate = c / total * 10000 if total else None
    return c, rate


def local_rates(terms, month):
    try:
        from diagnostics.corpus_io import load_corpus, posting_text
    except ImportError:
        from corpus_io import load_corpus, posting_text
    rows, _ = load_corpus(CORPUS)
    rows = [r for r in rows if r["day"].startswith(month)]
    tw = sum(r["w"] for r in rows)
    texts = [(r["w"], posting_text(r["item"], 10 ** 6).lower()) for r in rows]
    out = {}
    for t in terms:
        rx = re.compile(r"(?<!\w)" + re.escape(t.lower()) + r"(?!\w)")
        hit = [(w, bool(rx.search(x))) for w, x in texts]
        out[t] = (sum(1 for _, h in hit if h), sum(w for w, h in hit if h) / tw * 10000 if tw else None)
    return out, len(rows)


def report(data, windows, terms):
    L = ["# Source term probe", "",
         "Counts from the API keyword filter (one-row requests, `count` only) in one window per source. "
         "Hits per 10,000 postings in brackets. See the header of `diagnostics/61_source_term_probe.py` for what the "
         "filter can and cannot see; use this to rank sources, not to state prevalences.", ""]
    tot = {}
    L += ["## 1. Windows and totals", "", "| Source | Window | Postings |", "|---|---|---:|"]
    for s, w in windows.items():
        a = data.get(key(s, w[0], w[1], "total", "total"))
        c = a.get("count") if a else None
        tot[s] = c
        L.append(f"| {s} | {w[0]} to {w[1]} | {'not answered' if c is None else f'{c:,}'} |")
    srcs = [s for s in windows if tot.get(s)]
    L += ["", "## 2. Language words (share of the window's postings containing the word)", "",
          "| Source | " + " | ".join(f"{l}: {w}" for l, w in LANG_WORDS) + " |", "|---" * (len(LANG_WORDS) + 1) + "|"]
    for s in srcs:
        cells = []
        for l, w in LANG_WORDS:
            x = cell(data, s, windows[s], "lang", f"{l}:{w}", tot[s])
            cells.append("-" if not x else f"{x[0] / tot[s]:.0%}")
        L.append(f"| {s} | " + " | ".join(cells) + " |")
    L += ["", "A rough indicator: a word can also occur in postings of another language (names, loan words), "
          "and a stemmed index can lower the count.", "",
          "## 3. Index check (exact word against its stem)", "",
          "| Source | " + " | ".join(f"{a} / {b}" for a, b in STEM_CHECKS) + " | reading |", "|---" * (len(STEM_CHECKS) + 2) + "|"]
    for s in srcs:
        cells, stemmed = [], False
        for a, b in STEM_CHECKS:
            x = cell(data, s, windows[s], "stem", a, tot[s])
            y = cell(data, s, windows[s], "stem", b, tot[s])
            cells.append("-" if not x or not y else f"{x[0]:,} / {y[0]:,}")
            if x and y and y[0] > 1.5 * max(x[0], 1):
                stemmed = True
        L.append(f"| {s} | " + " | ".join(cells) + " | " +
                 ("stem returns more: index looks STEMMED, unstemmed counts are lower bounds" if stemmed
                  else "no sign of stemming") + " |")
    L += ["", "## 4. Terms", "",
          "`form`: word = one keyword; all words = every word of a multi-word term with `and`, anywhere in the posting "
          "(the filter does not match phrases: an upper bound that says little). Cells: hits (per 10,000).", "",
          "| Term | Lang | Channel | Form | " + " | ".join(srcs) + " |", "|---" * (4 + len(srcs)) + "|"]
    best = {s: [] for s in srcs}
    for t in terms:
        forms = [("word", "term")] if " " not in t["term"] else [("all words", "and")]
        for fname, kind in forms:
            cells = []
            for s in srcs:
                x = cell(data, s, windows[s], kind, t["term"], tot[s])
                cells.append("-" if not x else f"{x[0]:,} ({x[1]:.1f})")
                if x and fname == "word":
                    best[s].append((x[1], t["term"], x[0]))
            L.append(f"| {t['term']} | {t['language']} | {t['channel']} | {fname} | " + " | ".join(cells) + " |")
    L += ["", "## 5. Per source: terms with hits and the most frequent terms", "",
          "| Source | terms with at least 1 hit | with at least 10 hits | highest rates (hits per 10,000) |",
          "|---|---:|---:|---|"]
    for s in srcs:
        b = best[s]
        top = ", ".join(f"{t} {r:.1f}" for r, t, c in sorted(b, reverse=True)[:8] if c)
        L.append(f"| {s} | {sum(1 for r, t, c in b if c >= 1)} | {sum(1 for r, t, c in b if c >= 10)} | {top} |")
    L += ["", "Generic words (for example `customs`, `Zoll`, `Lieferkette`, `defence`) dominate the rates; read the table "
          "by term, not by the sum. Counts of terms that are also ordinary words say little about deglobalization.", ""]
    if "jobbland.se" in srcs and CORPUS.exists():
        w = windows["jobbland.se"]
        single = [t["term"] for t in terms if " " not in t["term"] and t["language"] in ("en", "any")]
        loc, n = local_rates(single, w[0][:7])
        L += ["## 6. Check against the local jobbland.se sample", "",
              f"Same English single words, counted on the text of the {n:,} sampled postings of {w[0][:7]} "
              "(day-weighted, exact duplicates dropped). Server hits per 10,000 against local weighted hits per 10,000 "
              "(local number of postings in brackets). A sample of this size shows rare words only by chance.", "",
              "| Term | server | local |", "|---|---:|---:|"]
        for t in single:
            x = cell(data, "jobbland.se", w, "term", t, tot["jobbland.se"])
            c, r = loc[t]
            L.append(f"| {t} | {'-' if not x else f'{x[1]:.1f}'} | {'-' if r is None else f'{r:.1f}'} ({c}) |")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\nWrote {REPORT}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--terms", default=str(TERMS))
    ap.add_argument("--sources", nargs="*", default=None, help=f"default: {' '.join(WINDOWS)}")
    ap.add_argument("--window", action="append", default=[], metavar="SOURCE=FROM:TO",
                    help="override a window, e.g. eures-escox=2025-12-01:2025-12-31")
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--pause", type=float, default=0.3)
    ap.add_argument("--report-only", action="store_true")
    ap.add_argument("--check-only", action="store_true",
                    help="only the total, the language words and the index check (about 10 requests per source): "
                         "answers 'what language is this source in' cheaply, e.g. in a small window of a slow source")
    args = ap.parse_args()

    windows = dict(WINDOWS)
    for w in args.window:
        s, rng = w.split("=", 1)
        lo, hi = rng.split(":", 1)
        windows[s] = (lo, hi)
    if args.sources:
        windows = {s: windows[s] for s in args.sources if s in windows}
    terms = read_terms(Path(args.terms))
    if args.report_only:
        data = json.loads(RAW.read_text(encoding="utf-8")) if RAW.exists() else {}
    else:
        n = len(plan(terms)) + 1
        print(f"{len(terms)} terms, {n} requests per source, {len(windows)} sources. "
              "Requests already answered in the saved file are skipped.")
        data = run(args, windows, terms)
    report(data, windows, terms)


if __name__ == "__main__":
    main()
