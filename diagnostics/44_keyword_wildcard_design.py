"""
Does the API keyword filter treat '*' as a wildcard, and where? A designed test.

Script 39 found, in kariera.gr March 2026: `nurs*` 58 postings, `energ*` 12,
but `software*`, `engineer*` and `manager*` 0, and every plain word 0. That left
the rule unexplained. The supervisor's hypothesis: `nurs*` works because the
asterisk stands for characters that FOLLOW in the same word (nurses, nursing),
whereas `engineer*` fails because in these postings 'engineer' is followed by a
space and the asterisk finds nothing to complete.

The earlier probes mostly used words with a count of 0, which cannot tell the
hypotheses apart. This script uses words whose plain count is known to be
positive (a control) and builds, for each word w, the same set of forms:

    w          the plain word (control: count > 0)
    w*         asterisk after the whole word
    w[:-1]*    last letter replaced by the asterisk
    w[:-2]*    last two letters replaced
    w[:n/2]*   a half-word stem
    ws, ws*    plural, plural with asterisk
    *w[1:]     leading asterisk

For each form it prints the count and, among the first 100 returned postings, the
actual word forms in the title and description that start with the stem (or end
with it, for a leading asterisk). Reading the table:

  * asterisk ignored:   w* = w, and w[:-1]* = w[:-1] (probably 0)
  * wildcard for any following characters, including none: w* >= w, and
    w[:-1]* >= w, with the longer word forms (plural, -ing, -ment) visible
  * wildcard that needs at least one following character (the supervisor's
    hypothesis): w* excludes postings where w stands alone, so w* < w, while
    w[:-1]* includes w, and the word forms found for w* are only longer words

Default cases (source : month : word), each with a known or likely positive count:
    jobbland.se : 2024-06 : software   (269 of 2,879 postings matched `software` in script 40)
    kariera.gr  : 2026-03 : hotel      (1,748 postings in script 36)
    kariera.gr  : 2026-03 : nurse      (plain 0, `nurs*` 58 in script 39)
    kariera.gr  : 2026-03 : engineer   (plain 0, `engineer*` 0 in script 39)

Usage, from the repo root:
    python -m diagnostics.44_keyword_wildcard_design
    python -m diagnostics.44_keyword_wildcard_design --cases jobbland.se:2024-06:software lesjeudis.com:2024-10:data

Output: docs/keyword_wildcard_design.md. About 9 requests per case, a few seconds each.
"""

import argparse
import calendar
import re
import time
from collections import Counter
from datetime import date
from pathlib import Path

REPORT_PATH = Path("docs/keyword_wildcard_design.md")
TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)
DEFAULT_CASES = [
    "jobbland.se:2024-06:software",
    "kariera.gr:2026-03:hotel",
    "kariera.gr:2026-03:nurse",
    "kariera.gr:2026-03:engineer",
]


def forms_for(w):
    out = [w, w + "*", w[:-1] + "*", w[:-2] + "*", w[: max(3, len(w) // 2)] + "*", w + "s", w + "s*", "*" + w[1:]]
    seen, res = set(), []
    for f in out:
        if f not in seen and f.strip("*"):
            seen.add(f)
            res.append(f)
    return res


def post(client, source, lo, hi, kws):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [source], "min_upload_date": lo, "max_upload_date": hi}
    if kws:
        form["keywords"] = kws
    t0 = time.time()
    r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": 1, "page_size": 100}, data=form, timeout=240)
    dt = time.time() - t0
    if r.status_code != 200:
        return None, [], dt, f"HTTP {r.status_code}: {r.text[:100]}"
    j = r.json()
    return j.get("count"), j.get("items", []), dt, ""


def word_forms(items, kw):
    leading = kw.startswith("*")
    stem = kw.strip("*").lower()
    c = Counter()
    for p in items:
        text = f"{p.get('title') or ''} {p.get('description') or ''}".lower()
        for t in TOKEN.findall(text):
            if (t.endswith(stem) if leading else t.startswith(stem)):
                c[t] += 1
    return ", ".join(f"{w} {n}" for w, n in c.most_common(6)) or "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", nargs="+", default=DEFAULT_CASES, help="source:YYYY-MM:word")
    args = ap.parse_args()

    from skillab_client import SkillabClient
    client = SkillabClient()
    L = ["# Keyword wildcard design test", "",
         "Per form: count of the API's `keywords` filter (one keyword) and the word forms found in the title and "
         "description of the first 100 returned postings (top 6 with number of postings). 'plain' is the control: a "
         "count above 0 shows the word occurs in that month.", ""]
    for case in args.cases:
        source, ym, word = case.split(":")
        y, m = (int(x) for x in ym.split("-"))
        lo, hi = date(y, m, 1).isoformat(), date(y, m, calendar.monthrange(y, m)[1]).isoformat()
        L += [f"## {source}, {ym}, word `{word}`", "", "| form | count | seconds | word forms in the first 100 postings | note |",
              "|---|---:|---:|---|---|"]
        for f in forms_for(word.lower()):
            try:
                count, items, dt, note = post(client, source, lo, hi, [f])
            except Exception as exc:
                count, items, dt, note = None, [], 0.0, f"FAILED: {exc}"
            wf = word_forms(items, f) if items else "-"
            label = f"`{f}`" + (" (plain)" if f == word.lower() else "")
            L.append(f"| {label} | {'-' if count is None else f'{count:,}'} | {dt:.0f} | {wf} | {note} |")
            print(f"{source} {ym} {f}: {count}")
        L.append("")

    L += ["Reading: compare, within one case, the plain word with its starred forms (see the three patterns in the "
          "header of `diagnostics/44`). A starred form that returns more than the plain word together with longer word "
          "forms (plural, -ing, -ment) shows a wildcard for following characters; a starred form that returns less than "
          "the plain word shows that the asterisk needs a following character; identical counts show that the asterisk "
          "is ignored. A case in which even the plain word is 0 says nothing about the rule."]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"\nWritten: {REPORT_PATH}")


if __name__ == "__main__":
    main()
