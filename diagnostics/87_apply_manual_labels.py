"""
Month 3: apply the author's labels from a review sheet to a tags file (a direct override, logged).

Takes the sheet written by script 86 (`channel` and `intensity` filled in by the author) and sets those two fields on the
matching postings of a `.post.jsonl` tags file. Rows with an empty `channel` are skipped. The tag before the override stays in
`channel_before_manual` / `intensity_before_manual`, the model's own answer stays where earlier steps put it, and
`rule` gets the suffix "; manual_review". Valid channels: reshoring, defense, critical materials, energy security,
trade compliance, diversification, none. The subtype is cleared unless the new channel is diversification.

Run (project root):
    python -m diagnostics.87_apply_manual_labels --tags data/tagged/tags_v12_jobbland.r71.post.jsonl \\
        --review data/tagging/cm_removed_review.csv --out data/tagged/tags_v12_jobbland.final.post.jsonl
"""
import argparse
import csv
import json
from collections import Counter

CHANNELS = {"reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification", "none"}
LEVELS = {"high", "medium", "low", "none", ""}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--tags", required=True)
    ap.add_argument("--review", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    labels = {}
    for r in csv.DictReader(open(a.review, encoding="utf-8-sig")):
        ch = (r.get("channel") or "").strip().lower()
        it = (r.get("intensity") or "").strip().lower()
        if not ch:
            continue
        if ch not in CHANNELS or it not in LEVELS:
            raise SystemExit(f"posting {r['posting_id']}: unknown channel '{ch}' or intensity '{it}'")
        if ch != "none" and it in ("", "none"):
            raise SystemExit(f"posting {r['posting_id']}: channel '{ch}' needs an intensity")
        labels[str(r["posting_id"])] = (ch, "none" if ch == "none" else it)
    n = 0
    moves = Counter()
    seen = set()
    with open(a.tags, encoding="utf-8") as f, open(a.out, "w", encoding="utf-8") as g:
        for line in f:
            if not line.strip():
                continue
            t = json.loads(line)
            pid = str(t["posting_id"])
            if pid in labels:
                ch, it = labels[pid]
                t["channel_before_manual"], t["intensity_before_manual"] = t.get("channel"), t.get("intensity")
                moves[(t.get("channel"), ch)] += 1
                t["channel"], t["intensity"] = ch, it
                if ch != "diversification":
                    t["subtype"] = ""
                t["rule"] = "; ".join(x for x in (t.get("rule"), "manual_review") if x)
                seen.add(pid)
                n += 1
            g.write(json.dumps(t, ensure_ascii=False) + "\n")
    missing = set(labels) - seen
    print(f"{n} of {len(labels)} labelled postings updated -> {a.out}")
    for (b, c), k in moves.items():
        print(f"  {b} -> {c}: {k}")
    if missing:
        print("WARNING: not found in the tags file:", sorted(missing))


if __name__ == "__main__":
    main()
