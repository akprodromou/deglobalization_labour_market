"""
What language are a source's postings in, and from which countries? Read from the
text of a small sample, not from the keyword filter.

The keyword filter cannot answer this for sources whose index is stemmed (script
61's index check): common words such as "the" are dropped there and return 0
although the text is English. This script fetches a few pages of postings from
one window and classifies every posting by counting function words of nine
languages (en, de, fr, nl, sv, es, it, pl, el) in its description. A posting is
assigned to the language with the most function words, provided it has at least
5 hits and a clear lead (more than twice the runner-up); otherwise it is "mixed
or unclear". The `location_code` of the same postings gives the country mix.

It is a heuristic with known weaknesses: very short descriptions are unclear,
postings that mix languages are split by whichever dominates, and the function
word lists are short. Treat shares of a few percent as noise.

Usage, from the repo root:
    python -m diagnostics.63_language_sample --source eures-escox --window 2026-01-12:2026-01-18
    python -m diagnostics.63_language_sample --source eures --window 2025-12-15:2025-12-21 --pages 3
    python -m diagnostics.63_language_sample --source lesjeudis.com --window 2025-06-01:2025-06-30 --page-size 100 --pages 2

--page-size 25 (the default) is what eures-escox answers (100-row requests were
dropped in the audit, and each request took about a minute); fast sources accept
--page-size 100. The pages are consecutive from --first-page; for a wider spread
use --first-page with different numbers in separate runs.

Output: printed and docs/language_sample_<source>.md (titles only, no description text)
"""

import argparse
import re
import time
import unicodedata
from collections import Counter
from pathlib import Path

STOP = {
    "en": "the and of to in for with a is are you we our will be as on that this your or by from at an have it".split(),
    "de": "und der die das mit für von zu den im ist sie wir ein eine auf bei als oder nicht sich werden dem".split(),
    "fr": "les des et de la le du pour avec une un dans vous nous sur est que qui au aux en ou par pas".split(),
    "nl": "het een van de en voor met je wij u op te zijn bij ook naar niet als maar dat die".split(),
    "sv": "och att i på för med är en som du vi till av det den har ett kan inte om eller våra".split(),
    "es": "los las del con para por una que es en el la y de se su al como más o sus nuestro".split(),
    "it": "il lo gli le di del della con per una che è sono nel nella e ed in non si come tra più".split(),
    "pl": "i w z na do się jest oraz nie dla przez lub który od jak to po przy czy".split(),
    "el": "και το την του της τα των με για στο στη από που να είναι σε ένα μια".split(),
}
# words that exist in several languages are left in only one list on purpose
for lang, words in list(STOP.items()):
    STOP[lang] = set(words)
ALL = {}
for lang, ws in STOP.items():
    for w in ws:
        ALL.setdefault(w, set()).add(lang)


def fold(s):
    return unicodedata.normalize("NFC", s.lower())


def classify(text):
    words = re.findall(r"[^\W\d_]+", fold(text))
    c = Counter()
    for w in words:
        langs = ALL.get(w)
        if langs and len(langs) == 1:
            c[next(iter(langs))] += 1
    if not c:
        return "unclear", 0
    (l1, n1), *rest = c.most_common(2)
    n2 = rest[0][1] if rest else 0
    if n1 >= 5 and n1 > 2 * n2:
        return l1, n1
    return "unclear", n1


def fetch(client, source, lo, hi, page, page_size, timeout, retries):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [source], "min_upload_date": lo, "max_upload_date": hi}
    for attempt in range(retries + 1):
        try:
            r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": page, "page_size": page_size},
                                    data=form, timeout=timeout)
            if r.status_code != 200:
                raise RuntimeError(f"HTTP {r.status_code}")
            j = r.json()
            return j.get("count"), j.get("items", [])
        except Exception as exc:
            if attempt == retries:
                print(f"  page {page}: failed ({exc})")
                return None, []
            time.sleep(5 * (attempt + 1))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--source", required=True)
    ap.add_argument("--window", required=True, metavar="FROM:TO")
    ap.add_argument("--pages", type=int, default=4)
    ap.add_argument("--first-page", type=int, default=1)
    ap.add_argument("--page-size", type=int, default=25)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--retries", type=int, default=2)
    args = ap.parse_args()
    lo, hi = args.window.split(":", 1)

    from skillab_client import SkillabClient
    client = SkillabClient()
    langs, by_country, by_lang_country, titles, n, total = Counter(), Counter(), Counter(), {}, 0, None
    for p in range(args.first_page, args.first_page + args.pages):
        count, items = fetch(client, args.source, lo, hi, p, args.page_size, args.timeout, args.retries)
        if count is not None:
            total = count
        for it in items:
            lang, _ = classify(f"{it.get('title') or ''} . {it.get('description') or ''}")
            cc = str(it.get("location_code") or "none")
            langs[lang] += 1
            by_country[cc] += 1
            by_lang_country[(cc, lang)] += 1
            titles.setdefault(lang, []).append((it.get("title") or "").strip()[:60])
            n += 1
        print(f"  page {p}: {len(items)} postings (total so far {n})")
    if not n:
        raise SystemExit("no postings fetched")

    L = [f"# Language sample: {args.source}, {lo} to {hi}", "",
         f"{n} postings read (pages {args.first_page}-{args.first_page + args.pages - 1} of {args.page_size}); "
         f"window total {total:,}. Language by function-word count; see the script header for the method and its limits.", "",
         "| Language | Postings | Share |", "|---|---:|---:|"]
    for lang, c in langs.most_common():
        L.append(f"| {lang} | {c} | {c / n:.0%} |")
    L += ["", "| Country (`location_code`) | Postings | Share | Languages within the country |", "|---|---:|---:|---|"]
    for cc, c in by_country.most_common():
        inner = ", ".join(f"{l} {k}" for (c2, l), k in by_lang_country.most_common() if c2 == cc)
        L.append(f"| {cc} | {c} | {c / n:.0%} | {inner} |")
    L += ["", "Titles by language (first 4):", ""]
    for lang in langs:
        L.append(f"- {lang}: " + "; ".join(titles[lang][:4]))
    out = Path(f"docs/language_sample_{re.sub(r'[^A-Za-z0-9.-]+', '_', args.source)}.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:12]))
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
