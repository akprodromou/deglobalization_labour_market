"""
Postings per location code and source, from the server.

GET /descriptive-analytics/jobs/locations returns "the number of appearances of
each location code", filterable by source, location_code and occupation_id. It
has no date filter, so the counts cover all months of a source. This script
calls it once without a source (all postings) and once per source, and writes:

  * the raw first rows of the first call, so the field names are on record;
  * for each source: total postings with a location code, number of distinct
    codes, the ten largest codes with counts and shares;
  * the location code spellings in use (for example EL against GR for Greece).

Sources: by default the list from GET /jobs/sources if that call works,
otherwise the five boards used in the event analysis. --sources overrides both.
Use --limit if a source has more than 300 distinct codes (the default of the API
is 100, which cuts off the list).

Usage, from the repo root:
    python -m diagnostics.43_locations_by_source
    python -m diagnostics.43_locations_by_source --sources kariera.gr jobbland.se --occupation-id <ESCO URI>

Output: docs/locations_by_source.md; raw responses in data/raw/locations_by_source.json.
One request per source (a few seconds each); about 30 requests for all sources.
"""

import argparse
import json
import time
from pathlib import Path

REPORT_PATH = Path("docs/locations_by_source.md")
RAW_PATH = Path("data/raw/locations_by_source.json")
ENDPOINT = "/descriptive-analytics/jobs/locations"
FALLBACK_SOURCES = ["kariera.gr", "lesjeudis.com", "jobbland.se", "jobs.de", "kariera.fr"]


def get(client, path, params=None, timeout=600):
    from skillab_client import BASE_URL
    try:
        r = client.session.get(f"{BASE_URL}{path}", params=params or {}, timeout=timeout)
    except Exception as exc:
        return None, f"FAILED: {exc}"
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}: {r.text[:120]}"
    try:
        return r.json(), ""
    except Exception:
        return None, "not JSON"


def list_sources(client):
    body, err = get(client, "/jobs/sources", timeout=120)
    if isinstance(body, list) and body:
        names = [b if isinstance(b, str) else (b.get("source") or b.get("name")) for b in body]
        names = [n for n in names if n]
        if names:
            return sorted(names), "from GET /jobs/sources"
    return FALLBACK_SOURCES, f"fallback list ({err or 'unexpected format'})"


def split_row(row):
    """Return (code, count) from one response row, whatever the field names are."""
    if not isinstance(row, dict):
        return None, None
    num = [k for k, v in row.items() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    txt = [k for k, v in row.items() if isinstance(v, str)]
    code = row.get("location_code") or (row[txt[0]] if txt else None)
    cnt = row.get("Freq") if isinstance(row.get("Freq"), (int, float)) else (row[num[0]] if num else None)
    return code, cnt


def summarise(body):
    pairs = [split_row(r) for r in body] if isinstance(body, list) else []
    pairs = [(c, n) for c, n in pairs if c is not None and n is not None]
    pairs.sort(key=lambda p: -p[1])
    return pairs, sum(n for _, n in pairs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="+")
    ap.add_argument("--limit", type=int, default=300)
    ap.add_argument("--occupation-id", default=None)
    args = ap.parse_args()

    from skillab_client import SkillabClient
    client = SkillabClient()
    if args.sources:
        sources, how = args.sources, "given on the command line"
    else:
        sources, how = list_sources(client)
    print(f"{len(sources)} sources ({how})")

    raw = {}
    L = ["# Postings per location code, by source", "",
         f"Endpoint `GET {ENDPOINT}`, limit {args.limit}"
         f"{', occupation ' + args.occupation_id if args.occupation_id else ''}. Source list: {how}. "
         "No date filter: counts cover all months of a source.", ""]

    def run(label, source):
        params = {"limit": args.limit}
        if source:
            params["source"] = source
        if args.occupation_id:
            params["occupation_id"] = args.occupation_id
        t0 = time.time()
        body, err = get(client, ENDPOINT, params)
        raw[label] = {"params": params, "error": err, "body": body}
        print(f"{label}: {time.time() - t0:.0f}s {err}")
        return body, err

    body, err = run("ALL", None)
    L += ["## All sources", ""]
    if body is None:
        L += [f"Request failed: {err}", ""]
    else:
        L += ["First 5 rows as returned:", "", "```json", json.dumps(body[:5] if isinstance(body, list) else body, indent=1,
                                                               ensure_ascii=False)[:1500], "```", ""]
        pairs, tot = summarise(body)
        L += [f"Distinct codes: {len(pairs)}; total: {tot:,}.", "",
              "| code | postings | share |", "|---|---:|---:|"]
        L += [f"| {c} | {n:,} | {100 * n / tot:.1f}% |" for c, n in pairs[:15]] if tot else []
        L.append("")

    L += ["## By source", "", "| source | postings with a code | distinct codes | largest codes (share) |", "|---|---:|---:|---|"]
    for s in sources:
        body, err = run(s, s)
        if body is None:
            L.append(f"| {s} | request failed | - | {err} |")
            continue
        pairs, tot = summarise(body)
        top = ", ".join(f"{c} {100 * n / tot:.0f}%" for c, n in pairs[:6]) if tot else "(empty)"
        flag = " (list may be cut off by limit)" if len(pairs) >= args.limit else ""
        L.append(f"| {s} | {tot:,} | {len(pairs)}{flag} | {top} |")

    L += ["", "Reading: compare the code spellings with those used in earlier filters (for example `EL` against `GR`), "
          "and the totals with the source totals of Report Section 9.6; a source whose total is far below its "
          "posting count has many postings without a location code."]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten: {REPORT_PATH} and {RAW_PATH}")


if __name__ == "__main__":
    main()
