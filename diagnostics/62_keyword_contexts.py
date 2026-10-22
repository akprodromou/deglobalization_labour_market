"""
What do the postings that the keyword filter returns actually say around the word?

The source term probe (script 61) counts postings containing a word. Some counts
are suspicious: `defense` in a French board (La Défense, the Paris business
district?), `tariffs` in a German board (a collective-bargaining "tariff
agreement"?), `customs`, `sovereignty`. This script fetches up to 100 postings
that the server returns for one keyword in one window and shows, from the text,
what stands around the word, so a false positive can be seen at once.

For each keyword it prints
  * how many of the postings really contain the word (the filter can return
    postings where only a stem or a variant occurs),
  * the words that most often stand just before and just after it,
  * the employers' titles most often returned,
  * a few short contexts.

Usage, from the repo root (credentials as for the other scripts):
    python -m diagnostics.62_keyword_contexts --source lesjeudis.com --window 2025-06-01:2025-06-30 --keywords defense défense
    python -m diagnostics.62_keyword_contexts --source jobs.de --window 2024-10-01:2024-10-31 --keywords tariffs customs
    python -m diagnostics.62_keyword_contexts --source kariera.fr --window 2024-10-01:2024-10-31 --keywords defense --page 3

--page chooses which block of 100 to read (the first block is the oldest or the
newest depending on the server; read two pages to be sure). Output: printed and
docs/keyword_contexts_<source>.md (one file per source, overwritten by each run for that
source; contains short snippets of postings). A failed request is retried twice.
"""

import argparse
import re
import time
import unicodedata
from collections import Counter
from pathlib import Path



def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def fetch(client, source, lo, hi, kw, page, timeout, retries=2):
    for attempt in range(retries + 1):
        try:
            return fetch_once(client, source, lo, hi, kw, page, timeout)
        except Exception:
            if attempt == retries:
                raise
            time.sleep(5 * (attempt + 1))


def fetch_once(client, source, lo, hi, kw, page, timeout):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    form = {"sources": [source], "min_upload_date": lo, "max_upload_date": hi, "keywords": [kw]}
    t0 = time.time()
    r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": page, "page_size": 100},
                            data=form, timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:100]}")
    j = r.json()
    return j.get("count"), j.get("items", []), time.time() - t0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--source", required=True)
    ap.add_argument("--window", required=True, metavar="FROM:TO")
    ap.add_argument("--keywords", nargs="+", required=True)
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()
    lo, hi = args.window.split(":", 1)

    from skillab_client import SkillabClient
    client = SkillabClient()
    L = [f"# Keyword contexts: {args.source}, {lo} to {hi}, page {args.page}", ""]
    for kw in args.keywords:
        try:
            count, items, dt = fetch(client, args.source, lo, hi, kw, args.page, args.timeout)
        except Exception as exc:
            L += [f"## {kw}", "", f"request failed: {exc}", ""]
            print(L[-2], L[-1])
            continue
        rx = re.compile(r"(?<!\w)" + re.escape(fold(kw)) + r"(?!\w)")
        before, after, titles, shown, real = Counter(), Counter(), Counter(), [], 0
        for it in items:
            raw = f"{it.get('title') or ''} . {it.get('description') or ''}"
            text = fold(raw)
            hits = list(rx.finditer(text))
            if hits:
                real += 1
                titles[(it.get("title") or "").strip()[:60]] += 1
            for m in hits[:3]:
                pre = re.findall(r"\w+", text[max(0, m.start() - 40):m.start()])
                post = re.findall(r"\w+", text[m.end():m.end() + 40])
                if pre:
                    before[pre[-1]] += 1
                if post:
                    after[post[0]] += 1
            if hits and len(shown) < 5:
                m = hits[0]
                shown.append(re.sub(r"\s+", " ", raw[max(0, m.start() - 70):m.end() + 70]).strip())
        L += [f"## {kw}", "",
              f"Server count in the window: {count:,}. Read {len(items)} postings; the word itself occurs in {real}.",
              "", f"Word before: {', '.join(f'{w} ({n})' for w, n in before.most_common(8))}",
              f"Word after: {', '.join(f'{w} ({n})' for w, n in after.most_common(8))}",
              f"Titles returned most often: {', '.join(f'{t} ({n})' for t, n in titles.most_common(5) if n > 1) or 'no repeats'}",
              "", "Contexts:"] + [f"- ...{c}..." for c in shown] + [""]
        print("\n".join(L[-(9 + len(shown)):]))
    report = Path(f"docs/keyword_contexts_{re.sub(r'[^A-Za-z0-9.-]+', '_', args.source)}.md")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"Wrote {report}")


if __name__ == "__main__":
    main()
