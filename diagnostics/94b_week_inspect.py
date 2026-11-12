"""
Month 4: what is inside a spike? Lists the flagged postings of a date range: channel counts, most common titles,
and most common first 80 characters of the description (a template proxy), with the share of flagged postings that the
largest template group holds. Use it on the weeks that 94_sampling_check.py lists as furthest from their quarter.

Run (project root, venv active), jobbland 2025-W16 (14 to 20 April 2025) as an example:
    python -m diagnostics.94b_week_inspect --corpus data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl --tags data/tagged/tags_v12_jobbland.final.post.jsonl --from 2025-04-14 --to 2025-04-20
"""
import argparse
import json
import re
from collections import Counter

CH = {"reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--tags", nargs="+", required=True)
    ap.add_argument("--from", dest="d0", required=True)
    ap.add_argument("--to", dest="d1", required=True)
    ap.add_argument("--top", type=int, default=12)
    a = ap.parse_args()
    tag = {}
    for p in a.tags:
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                tag[str(r["posting_id"])] = r.get("channel") if r.get("ok") and r.get("channel") in CH else None
    n = fl = 0
    ch, ti, te, days = Counter(), Counter(), Counter(), set()
    for p in a.corpus:
        for l in open(p, encoding="utf-8"):
            if not l.strip():
                continue
            r = json.loads(l)
            if not (a.d0 <= r["day"] <= a.d1):
                continue
            days.add(r["day"])
            for it in r["items"]:
                n += 1
                c = tag.get(str(it["id"]))
                if c:
                    fl += 1
                    ch[c] += 1
                    ti[(it.get("title") or "").strip()[:70]] += 1
                    te[re.sub(r"\W+", " ", (it.get("description") or "")[:80].lower()).strip()] += 1
    print(f"{a.d0} to {a.d1}: {len(days)} sampled days, {n} postings, {fl} flagged ({fl / max(n, 1):.1%}; duplicates not removed here)")
    print("\nchannels:", dict(ch))
    print("\nmost common titles among flagged:")
    for t, c in ti.most_common(a.top):
        print(f"  {c:4d}  {t}")
    print("\nmost common description openings among flagged:")
    for t, c in te.most_common(a.top):
        print(f"  {c:4d}  {t}")
    if te:
        print(f"\nlargest template group holds {te.most_common(1)[0][1] / fl:.1%} of the flagged postings")


if __name__ == "__main__":
    main()
