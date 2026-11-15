"""
Probe the Skillab Tracker API with keyword queries (for example the two named occupations that no board shows in the titles).
Logs in with the credentials in .env, queries /jobs for each keyword group, walks up to --max-pages pages and prints how many postings
come back, their sources, the first titles and the first posting's field names. Nothing is written to the corpus.

.env (project root, never in the report or in git):
    SKILLAB_USERNAME=...
    SKILLAB_PASSWORD=...
    SKILLAB_API_BASE_URL=...   optional; default https://skillab-tracker.csd.auth.gr/api

Run (project root, venv active):
    python -m diagnostics.113_skillab_keyword_probe --sources jobbland.se lesjeudis.com jobs.de --keywords "critical raw materials" "reshoring" --max-pages 3
"""
import argparse
import os
import time

import re
from collections import Counter

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def load_env(path=".env"):
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--keywords", nargs="+", required=True, help="one query per keyword; each is sent alone")
    ap.add_argument("--max-pages", type=int, default=3)
    ap.add_argument("--sources", nargs="*", default=[], help="one query per source and keyword (smaller queries time out less); empty = all sources in one query")
    ap.add_argument("--retries", type=int, default=2)
    a = ap.parse_args()
    load_env()
    base = os.environ.get("SKILLAB_API_BASE_URL", "https://skillab-tracker.csd.auth.gr/api").rstrip("/")
    r = requests.post(f"{base}/login", json={"username": os.environ["SKILLAB_USERNAME"], "password": os.environ["SKILLAB_PASSWORD"]},
                      headers={"accept": "application/json", "Content-Type": "application/json"}, verify=False, timeout=45)
    r.raise_for_status()
    hdr = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Bearer {r.text.replace(chr(34), '')}"}
    print("authenticated")
    for kw, src in [(k, sc) for k in a.keywords for sc in (a.sources or [None])]:
        label = kw if not src else f"{kw} @ {src}"
        n, shown, in_title = 0, 0, 0
        by_src = Counter()
        words = [w for w in re.split(r"\W+", kw.lower()) if len(w) > 3]
        for page in range(1, a.max_pages + 1):
            time.sleep(0.5)
            resp = None
            for attempt in range(a.retries + 1):
                try:
                    resp = requests.post(f"{base}/jobs?page={page}", headers=hdr, data={"sources": [src] if src else [], "keywords": [kw]}, verify=False, timeout=90)
                    break
                except requests.exceptions.RequestException as exc:
                    print(f"  [{label}] page {page}, attempt {attempt + 1}: {type(exc).__name__}")
                    time.sleep(10)
            if resp is None:
                print(f"  [{label}] page {page}: gave up, counts below are partial")
                break
            if resp.status_code != 200:
                print(f"  [{label}] page {page}: HTTP {resp.status_code}")
                break
            items = resp.json().get("items", [])
            if not items:
                break
            if page == 1:
                print(f"\n[{label}] fields of a posting: {sorted(items[0].keys())}")
            n += len(items)
            for it in items:
                by_src[it.get("source", "?")] += 1
                in_title += any(w in (it.get("title") or "").lower() for w in words)
                if shown < 8:
                    print("   ", (it.get("title") or "")[:90], "|", it.get("source", ""), "|", str(it.get("upload_date", it.get("date", "")))[:10])
                    shown += 1
        print(f"[{label}] {n} postings on up to {a.max_pages} pages; {in_title} have a keyword word in the title; by source: {dict(by_src)}")


if __name__ == "__main__":
    main()
