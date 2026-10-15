"""
What does the API's `keywords` filter actually match? A ground-truth experiment.

Scripts 36-44 asked the filter for counts and tried to guess the rule from them.
Counts alone cannot show which postings the filter picks and why. This script
uses the documented `ids` filter of POST /jobs together with `keywords`: for a
sample of 100 postings whose full text we hold, it asks the server "of THESE ids,
which match this keyword?" and compares the answer, posting by posting, with what
the text says. A keyword that the server matches in a posting whose title and
description do not contain it points to another indexed field (for example a
translation or extracted keywords); a match only when the word is early in the
description points to a limit on the indexed text; and so on.

Steps
  1. Take 100 postings (source, month; page 1 of the date-filtered set) with full
     title and description.
  2. Choose test keywords from the sample itself:
       A. words that occur in titles (title words),
       B. words that occur only early in descriptions (first occurrence < 300 characters),
       C. words that occur only late in descriptions (first occurrence > 1,200 characters),
       D. variants of three title words: plural, last letter removed, with an asterisk,
          and a 4-letter stem with an asterisk.
  3. For each keyword, POST /jobs with `ids` = the 100 ids and `keywords` = [keyword],
     and record which of the 100 ids come back.
  4. Compare the returned set with candidate rules computed locally from the text:
       title (exact word), desc (exact word, anywhere), desc<=200 / <=500 / <=1000
       (exact word, first occurrence within that many characters), title|desc,
       substring (the keyword as a substring of title or description). For starred
       keywords the stem is matched as a prefix of a word.
     Per rule: true positives, false positives (returned but the rule says no),
     false negatives (the rule says yes, not returned) and F1.

Usage, from the repo root:
    python -m diagnostics.45_keyword_index_experiment
    python -m diagnostics.45_keyword_index_experiment --source kariera.gr --month 2026-03

Outputs: docs/keyword_index_experiment_<source>_<month>.md and data/raw/keyword_index_experiment_<source>_<month>.json (one pair per run).
About 45 requests of a few seconds each (the `ids` filter should make them fast; a
request that fails is reported and skipped). The default case, jobbland.se June
2024, is one in which the filter returns many hits for English words in Swedish text.
"""

import argparse
import calendar
import json
import re
import statistics
import time
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REPORT_PATH = Path("docs/keyword_index_experiment.md")
RAW_PATH = Path("data/raw/keyword_index_experiment.json")
TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)
try:
    import snowballstemmer
    STEMMERS = {"stem": snowballstemmer.stemmer("english"), "porter": snowballstemmer.stemmer("porter")}
except ImportError:  # pip install snowballstemmer
    STEMMERS = {}


def post(client, form, page=1, size=100):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    time.sleep(0.5)  # stay below the rate limit
    t0 = time.time()
    for attempt in range(6):
        r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": page, "page_size": size}, data=form, timeout=240)
        if r.status_code != 429:
            break
        try:
            wait = float(r.headers.get("Retry-After") or 0)
        except ValueError:
            wait = 0
        time.sleep(wait or 5 * (attempt + 1))
    dt = time.time() - t0
    if r.status_code != 200:
        return None, [], dt, f"HTTP {r.status_code}: {' '.join(r.text.split())[:80]}"
    j = r.json()
    return j.get("count"), j.get("items", []), dt, ""


class Doc:
    def __init__(self, p):
        self.id = p["id"]
        self.title = str(p.get("title") or "").lower()
        self.desc = str(p.get("description") or "").lower()
        self.title_tokens = set(TOKEN.findall(self.title))
        edge = ".,;:!?()[]{}\"'“”‘’«»…–—-"
        # whitespace tokens; apostrophes split a token ("role's" -> role, s); any non-letter/digit at the
        # ends of a token is dropped; punctuation inside a token (extras/actors, commercial.there) stays
        raw_text = (self.title + " " + self.desc).replace("’", "'")
        self.ws_tokens = {re.sub(r"^\W+|\W+$", "", part) for raw in raw_text.split() for part in raw.split("'")} - {""}
        # stems of the whitespace tokens: a stemmed index would hold these, not the words themselves
        self.stems = {n: {s.stemWord(t) for t in self.ws_tokens} for n, s in STEMMERS.items()}
        self.first = {}
        for m in TOKEN.finditer(self.desc):
            self.first.setdefault(m.group(0), m.start())


def rules(kw, docs):
    """Candidate rules: name -> set of ids that the rule says match."""
    star = kw.endswith("*")
    stem = kw.rstrip("*").lower()

    def hit(token):
        return token.startswith(stem) if star else token == stem

    out = defaultdict(set)
    for d in docs:
        in_title = any(hit(t) for t in d.title_tokens)
        offs = [o for t, o in d.first.items() if hit(t)]
        if in_title:
            out["title"].add(d.id)
        if offs:
            out["desc"].add(d.id)
            for n in (200, 500, 1000):
                if min(offs) <= n:
                    out[f"desc<={n}"].add(d.id)
        if in_title or offs:
            out["title|desc"].add(d.id)
        if stem in d.title or stem in d.desc:
            out["substring"].add(d.id)
        if any(hit(t) for t in d.ws_tokens):
            out["ws"].add(d.id)  # split on whitespace, punctuation stripped at the ends only
        for name, stems in d.stems.items():
            if not star and stem in stems:
                out[name].add(d.id)  # the query is compared with the stems of the words in the text
    return out


def score(returned, truth):
    tp, fp, fn = len(returned & truth), len(returned - truth), len(truth - returned)
    f1 = 2 * tp / (2 * tp + fp + fn) if (tp + fp + fn) else 1.0
    return tp, fp, fn, f1


def snippet(d, kw):
    star = kw.endswith("*")
    stem = kw.rstrip("*").lower()
    pat = r"(?<![^\W\d_])" + re.escape(stem) + ("" if star else r"(?![^\W\d_])")
    for text in (d.title, d.desc):
        m = re.search(pat, text)
        if m:
            return text[max(0, m.start() - 40): m.end() + 40].replace("\n", " ").replace("`", "'")
    return ""


def choose_keywords(docs):
    title_df, desc_df, offsets = Counter(), Counter(), defaultdict(list)
    for d in docs:
        for t in d.title_tokens:
            if len(t) >= 4:
                title_df[t] += 1
        for t, o in d.first.items():
            if len(t) >= 4:
                desc_df[t] += 1
                offsets[t].append(o)
    A = [w for w, c in title_df.most_common() if c >= 3][:8]
    B, C = [], []
    for w, c in desc_df.most_common():
        if w in title_df or not 5 <= c <= 60:
            continue
        med = statistics.median(offsets[w])
        if med < 300 and len(B) < 8:
            B.append(w)
        elif med > 1200 and len(C) < 8:
            C.append(w)
    D, seen = [], set(A) | set(B) | set(C)
    for w in A[:3]:
        for v in (w + "s", w[:-1], w[:-1] + "*", w + "*", w[:4] + "*"):
            if v not in seen:
                seen.add(v)
                D.append(v)
    return [("A title word", A), ("B early in description", B), ("C late in description", C), ("D variants", D)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="jobbland.se")
    ap.add_argument("--month", default="2024-06")
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--extra", nargs="*", default=[], help="additional keywords to test, e.g. 'nurs*' 'energ*'")
    args = ap.parse_args()
    global REPORT_PATH, RAW_PATH
    REPORT_PATH = Path(f"docs/keyword_index_experiment_{args.source}_{args.month}.md")  # one file per run
    RAW_PATH = Path(f"data/raw/keyword_index_experiment_{args.source}_{args.month}.json")
    if not STEMMERS:
        print("Note: snowballstemmer is not installed, so the stem columns stay empty "
              "(python -m pip install snowballstemmer).")

    from skillab_client import SkillabClient
    client = SkillabClient()
    y, m = (int(x) for x in args.month.split("-"))
    lo, hi = date(y, m, 1).isoformat(), date(y, m, calendar.monthrange(y, m)[1]).isoformat()

    count, items, dt, err = post(client, {"sources": [args.source], "min_upload_date": lo, "max_upload_date": hi},
                                 page=args.page)
    if not items:
        raise SystemExit(f"Could not fetch the sample page: {err or 'empty'}")
    docs = [Doc(p) for p in items]
    ids = [d.id for d in docs]
    print(f"Sample: {len(docs)} postings of {count:,} in {args.source} {args.month} (page {args.page}, {dt:.0f} s)")

    L = [f"# Keyword index experiment: {args.source}, {args.month}", "",
         f"Sample: {len(docs)} postings (page {args.page} of {count:,}). For each keyword the server was asked which of "
         "these ids match. Per rule: TP = returned and rule says match, FP = returned but rule says no, "
         "FN = rule says match but not returned. The best rule is the one with the highest F1.", ""]
    raw = {"source": args.source, "month": args.month, "ids": ids, "results": {}}
    wins = Counter()
    groups = choose_keywords(docs)
    if args.extra:
        groups.append(("E extra keywords", args.extra))
    byid = {d.id: d for d in docs}
    ctx = []
    ctx2 = []
    for gname, words in groups:
        L += [f"## {gname}", "", "| keyword | returned | best rule | TP / FP / FN (best) | title | desc | stem | substring | ws | note |",
              "|---|---:|---|---|---|---|---|---|---|---|"]
        for kw in words:
            form = {"sources": [args.source], "ids": ids, "keywords": [kw]}
            try:
                cnt, res, dt, err = post(client, form)
            except Exception as exc:
                cnt, res, dt, err = None, [], 0.0, f"FAILED: {exc}"
            if cnt is None:
                L.append(f"| `{kw}` | - | - | - | - | - | - | - | - | {err} |")
                continue
            returned = {p["id"] for p in res} & set(ids)
            note = "" if cnt == len(returned) else f"count {cnt} vs {len(returned)} returned in sample"
            truth = rules(kw, docs)
            scores = {n: score(returned, truth.get(n, set())) for n in
                      ("title", "desc", "desc<=200", "desc<=500", "desc<=1000", "title|desc", "substring", "ws", "stem", "porter")}
            best = max(scores, key=lambda n: scores[n][3])
            tp, fp, fn, f1 = scores[best]
            if not returned and not any(truth.values()):
                best_txt = "(no match anywhere)"
            else:
                best_txt = f"{best} (F1 {f1:.2f})"
                wins[best] += 1
            fmt = lambda n: f"{scores[n][0]}/{scores[n][1]}/{scores[n][2]}"
            L.append(f"| `{kw}` | {len(returned)} | {best_txt} | {tp}/{fp}/{fn} | {fmt('title')} | {fmt('desc')} | "
                     f"{fmt('stem')} | {fmt('substring')} | {fmt('ws')} | {note} |")
            missed = sorted(truth.get("title|desc", set()) - returned)
            if missed:
                got = sorted(truth.get("title|desc", set()) & returned)
                ctx.append((kw, [(i, "MISSED", snippet(byid[i], kw)) for i in missed[:4]] +
                            [(i, "returned", snippet(byid[i], kw)) for i in got[:2]], len(missed)))
            unexpected = [] if kw.endswith("*") else sorted(returned - truth.get("ws", set()))
            if unexpected:
                ctx2.append((kw, [(i, snippet(byid[i], kw)) for i in unexpected[:4]], len(unexpected)))
            raw["results"][kw] = {"returned": sorted(returned), "scores": {n: list(v) for n, v in scores.items()}}
            print(f"{kw}: returned {len(returned)}, best {best_txt}")
        L.append("")

    L += ["## Which rule fits best", "", "| rule | number of keywords where it fits best |", "|---|---:|"]
    L += [f"| {n} | {c} |" for n, c in wins.most_common()]
    if ctx:
        L += ["", "## Postings that contain the keyword (title or description) but were not returned", "",
              "Up to 4 missed postings (and 2 returned ones for comparison) per keyword, 40 characters either side "
              "of the first occurrence.", ""]
        for kw, rows, n_missed in ctx:
            L += [f"### `{kw}`: {n_missed} missed", ""]
            L += [f"- {tag} (id {i}): `{sn}`" for i, tag, sn in rows]
            L.append("")
    if ctx2:
        L += ["", "## Returned by the server although the whitespace rule (`ws`) says no", "",
              "The server splits words in a way that differs from `ws` for these postings. Text around the first "
              "occurrence of the word:", ""]
        for kw, rows, n in ctx2:
            L += [f"### `{kw}`: {n} posting(s)", ""]
            L += [f"- id {i}: `{sn}`" for i, sn in rows]
            L.append("")
    L += ["", "Reading: columns title, desc, desc<=500 and substring give TP/FP/FN against that rule. A keyword whose "
          "returned postings are all TP for `title` and with few FN means the filter searches the title (exact words). "
          "FN under `desc` with TP under `desc<=500` means only the start of the description is indexed. FP under every "
          "rule means the server matches text we do not hold (translation, extracted keywords). Starred keywords are "
          "compared as prefixes; if their FN stay high under every rule, the asterisk is not a prefix wildcard."]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(raw), encoding="utf-8")
    print(f"\nWritten: {REPORT_PATH} and {RAW_PATH}")


if __name__ == "__main__":
    main()
