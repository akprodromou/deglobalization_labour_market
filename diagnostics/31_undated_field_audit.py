"""
Does the tracker hold ANOTHER date for postings that have no upload_date?

Two questions, both answered from the live API (no assumptions about the docs):

A. FIELD AUDIT. For `eures` and `eures-escox` we fetch evenly spaced pages of the
   unfiltered result set and list EVERY field the API actually returns (top level
   and one level down inside organization / skills / occupations / sectors), split
   by dated vs undated postings. Any field whose name looks like a date or time
   (date, time, created, updated, scrap, collect, crawl, insert, expir, valid,
   deadline, publish, posted) is printed with example values. The Swagger docs list
   only `upload_date`, but the real response may carry more.

B. ID AS A CLOCK. Postings are ordered by id, and the supervisor says the EURES
   upload_date is the insertion date. If ids grow with insertion time, the id of an
   undated posting can be turned into an approximate date by looking at dated
   postings with nearby ids. We test this honestly: for every dated posting we
   predict its date from the nearest dated posting in a DIFFERENT page (the
   situation of an undated posting in a long undated stretch) and report the error
   in days. A median error of a few days would make id-based dating usable for
   monthly analysis; weeks or months would not.

Usage, from the repo root (credentials in .env or env vars):
    python -m diagnostics.31_undated_field_audit
    python -m diagnostics.31_undated_field_audit --sources eures --pages 40

Resumable: pages are kept in data/raw/field_audit.json. Output: docs/field_audit.md.
"""

import argparse
import bisect
import json
import re
import statistics
import time
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

OUT_PATH = Path("data/raw/field_audit.json")
REPORT_PATH = Path("docs/field_audit.md")
PAGE_SIZE = 100
DOCUMENTED = {"organization", "skills", "occupations", "sectors", "id", "title", "description",
              "experience_level", "type", "location", "location_code", "nuts1", "nuts2", "nuts3",
              "upload_date", "source", "source_id"}
DATEISH = re.compile(r"date|time|created|updated|scrap|collect|crawl|insert|expir|valid|deadline|"
                     r"publish|posted|start|end", re.I)


def grid_pages(n_pages, k):
    k = min(k, n_pages)
    return sorted({max(1, min(n_pages, round((j + 0.5) * n_pages / k))) for j in range(k)})


def fetch(client, source, page, attempts=3):
    from skillab_client import BASE_URL, JOBS_ENDPOINT
    last = None
    for i in range(1, attempts + 1):
        try:
            r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": page, "page_size": PAGE_SIZE},
                                    data={"sources": [source]}, timeout=240)
            r.raise_for_status()
            p = r.json()
            return p.get("items", []), p.get("count")
        except Exception as exc:
            last = exc
            print(f"    attempt {i}/{attempts} failed: {exc}")
            time.sleep(5 * i)
    raise last


def to_date(s):
    try:
        return date.fromisoformat(str(s)[:10])
    except Exception:
        return None


def nonempty(v):
    return v not in (None, "", [], {})


def summarise(items):
    """Compact per-page record: field presence by dated/undated, date-like examples, (id, date) pairs."""
    pres = {"dated": Counter(), "undated": Counter()}
    nested = {"dated": Counter(), "undated": Counter()}
    examples = defaultdict(list)
    pairs = []
    n = {"dated": 0, "undated": 0}
    first_undated = None
    allkeys = Counter()
    for p in items:
        allkeys.update(p.keys())
        k = "dated" if p.get("upload_date") else "undated"
        n[k] += 1
        pairs.append([p.get("id"), str(p.get("upload_date"))[:10] if p.get("upload_date") else None])
        if k == "undated" and first_undated is None:
            first_undated = {a: (str(b)[:160] if isinstance(b, str) else b) for a, b in p.items()
                             if a not in ("skills", "occupations")}
            first_undated["skills"] = f"<{len(p.get('skills') or [])} items>"
            first_undated["occupations"] = (p.get("occupations") or [])[:1]
        for key, val in p.items():
            if nonempty(val):
                pres[k][key] += 1
            if DATEISH.search(key) and nonempty(val) and len(examples[key]) < 3:
                examples[key].append(str(val)[:60])
            vals = val if isinstance(val, list) else [val]
            for v in vals[:1]:
                if isinstance(v, dict):
                    for sub, sv in v.items():
                        if nonempty(sv):
                            nested[k][f"{key}.{sub}"] += 1
                        if DATEISH.search(sub) and nonempty(sv) and len(examples[f"{key}.{sub}"]) < 3:
                            examples[f"{key}.{sub}"].append(str(sv)[:60])
    return {"n": n, "present": {k: dict(v) for k, v in pres.items()},
            "nested": {k: dict(v) for k, v in nested.items()},
            "date_like_examples": dict(examples), "pairs": pairs, "first_undated": first_undated,
            "keys": dict(allkeys)}


def load():
    return json.loads(OUT_PATH.read_text(encoding="utf-8")) if OUT_PATH.exists() else {}


def save(d):
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


def collect(sources, k):
    from skillab_client import SkillabClient
    client = SkillabClient()
    data = load()
    for source in sources:
        w = data.setdefault(source, {"pages": {}})
        if "count" not in w:
            try:
                _, w["count"] = fetch(client, source, 1)
            except Exception as exc:
                print(f"  {source}: could not get count ({exc})")
                continue
            save(data)
        n_pages = -(-w["count"] // PAGE_SIZE)
        wanted = grid_pages(n_pages, k)
        print(f"  {source}: {w['count']:,} postings, {n_pages:,} pages; {len(wanted)} pages")
        for page in wanted:
            key = str(page) if PAGE_SIZE == 100 else f"{page}@{PAGE_SIZE}"
            if key in w["pages"]:
                continue
            try:
                items, _ = fetch(client, source, page)
            except Exception as exc:
                print(f"    page {page}: FAILED ({exc})")
                continue
            w["pages"][key] = summarise(items)
            save(data)
            s = w["pages"][key]
            print(f"    page {page}: dated {s['n']['dated']}, undated {s['n']['undated']}")
    return data


def merge_presence(w, key):
    tot = {"dated": Counter(), "undated": Counter()}
    n = {"dated": 0, "undated": 0}
    for s in w["pages"].values():
        for k in ("dated", "undated"):
            n[k] += s["n"][k]
            tot[k].update(s[key][k])
    return tot, n


def id_clock_errors(w):
    """Leave-one-page-out nearest-neighbour prediction of upload date from id."""
    pts = []  # (id, ordinal, page)
    for page, s in w["pages"].items():
        for i, d in s["pairs"]:
            dd = to_date(d) if d else None
            if i is not None and dd:
                pts.append((i, dd.toordinal(), page))
    pts.sort()
    if len(pts) < 50:
        return None
    ids = [p[0] for p in pts]
    errs = []
    for idx, (i, o, page) in enumerate(pts):
        best = None
        for step in range(1, len(pts)):
            cand = []
            if idx - step >= 0 and pts[idx - step][2] != page:
                cand.append(pts[idx - step])
            if idx + step < len(pts) and pts[idx + step][2] != page:
                cand.append(pts[idx + step])
            if cand:
                best = min(cand, key=lambda c: abs(c[0] - i))
                break
            if idx - step < 0 and idx + step >= len(pts):
                break
        if best:
            errs.append(abs(best[1] - o))
    if not errs:
        return None
    errs.sort()
    q = lambda f: errs[min(len(errs) - 1, int(f * len(errs)))]
    # monotonicity: share of id-ordered neighbours (different pages) whose date goes backwards
    back = sum(1 for a, b in zip(pts, pts[1:]) if a[2] != b[2] and b[1] < a[1])
    cross = sum(1 for a, b in zip(pts, pts[1:]) if a[2] != b[2])
    return {"n": len(errs), "median": q(0.5), "p75": q(0.75), "p90": q(0.9), "max": errs[-1],
            "within_7": sum(e <= 7 for e in errs) / len(errs),
            "within_31": sum(e <= 31 for e in errs) / len(errs),
            "backwards_between_pages": f"{back}/{cross}"}


def report(data, sources):
    out = ["# Field audit and id-as-clock test for undated postings", "",
           "Script: `diagnostics/31_undated_field_audit.py`. Evenly spaced pages of the unfiltered "
           "result set (ordered by id).", ""]
    for source in sources:
        w = data.get(source)
        if not w or not w.get("pages"):
            continue
        tot, n = merge_presence(w, "present")
        out += [f"## {source}", "",
                f"Postings sampled: {n['dated']:,} dated, {n['undated']:,} undated "
                f"({len(w['pages'])} pages).", "",
                "### A. Fields actually returned (share of postings with a non-empty value)", "",
                "| Field | Documented | Dated | Undated |", "|---|---|---|---|"]
        keys = sorted(set(tot["dated"]) | set(tot["undated"]))
        for key in keys:
            d = tot["dated"][key] / n["dated"] * 100 if n["dated"] else 0
            u = tot["undated"][key] / n["undated"] * 100 if n["undated"] else 0
            out.append(f"| {key} | {'yes' if key in DOCUMENTED else '**NO**'} | {d:.0f}% | {u:.0f}% |")
        seen = Counter()
        n_with = 0
        for s_ in w["pages"].values():
            if "keys" in s_:
                seen.update(s_["keys"])
                n_with += 1
        if n_with:
            extra = sorted(k for k in seen if k not in DOCUMENTED)
            absent = sorted(DOCUMENTED - set(seen))
            out += ["", f"Keys present in the raw JSON (even when the value is always null), {n_with} of "
                    f"{len(w['pages'])} pages recorded:", "",
                    ("- Undocumented top-level keys: " + ", ".join(f"`{k}`" for k in extra)) if extra
                    else "- No top-level key beyond the documented JobSchema is returned.",
                    ("- Documented keys never returned: " + ", ".join(f"`{k}`" for k in absent)) if absent
                    else "- Every documented key is returned.", ""]
        else:
            extra = [k for k in keys if k not in DOCUMENTED]
            out += ["", ("Undocumented top-level fields with a non-empty value: " + ", ".join(extra)) if extra
                    else "No undocumented field with a non-empty value (all-null keys were not recorded for "
                         "these older pages).", ""]
        ntot, _ = merge_presence(w, "nested")
        nkeys = sorted(set(ntot["dated"]) | set(ntot["undated"]))
        out += ["Nested fields (first element of organization / skills / occupations / sectors):", ""]
        out.append(", ".join(f"`{k}`" for k in nkeys) if nkeys else "none")
        ex = {}
        for s in w["pages"].values():
            for key, vals in s["date_like_examples"].items():
                ex.setdefault(key, [])
                for v in vals:
                    if v not in ex[key] and len(ex[key]) < 3:
                        ex[key].append(v)
        out += ["", "Fields whose name looks like a date/time, with example values:", ""]
        if ex:
            out += [f"- `{k}`: {v}" for k, v in sorted(ex.items())]
        else:
            out.append("none")
        fu = next((s["first_undated"] for s in w["pages"].values() if s.get("first_undated")), None)
        if fu:
            out += ["", "One complete undated record (description truncated, skills/occupations shortened):", "",
                    "```", json.dumps(fu, indent=1, ensure_ascii=False)[:1800], "```"]
        res = id_clock_errors(w)
        out += ["", "### B. Can the id date an undated posting?", ""]
        if res:
            out += [f"Each dated posting (n={res['n']:,}) is predicted from the nearest dated posting "
                    "in a different page. Absolute error in days:", "",
                    "| median | 75th pct | 90th pct | max | within 7 days | within 31 days |",
                    "|---|---|---|---|---|---|",
                    f"| {res['median']} | {res['p75']} | {res['p90']} | {res['max']} | "
                    f"{res['within_7']:.0%} | {res['within_31']:.0%} |", "",
                    f"Neighbouring dated postings from different pages whose date goes backwards "
                    f"as id increases: {res['backwards_between_pages']}."]
        else:
            out.append("Not enough dated postings for the test.")
        out.append("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))
    print(f"\nWrote {REPORT_PATH}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="+", default=["eures", "eures-escox"])
    ap.add_argument("--pages", type=int, default=30)
    ap.add_argument("--analyse-only", action="store_true")
    ap.add_argument("--page-size", type=int, default=100,
                    help="rows per request; use 10-25 for sources whose big requests are dropped")
    args = ap.parse_args()
    global PAGE_SIZE
    PAGE_SIZE = args.page_size
    data = load() if args.analyse_only else collect(args.sources, args.pages)
    report(data, args.sources)


if __name__ == "__main__":
    main()
