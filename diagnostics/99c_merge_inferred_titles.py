"""
Month 4: put the inferred titles (script 99) into a copy of the titles file, for clustering with script 92.

For every posting without a title (has_title false in titles_<label>.jsonl) that has an answer other than UNKNOWN in
inferred_titles_<label>.jsonl: title_clean = the inferred title, has_title = true, title_source = "inferred". Postings with a real title,
and title-less postings the model answered UNKNOWN for, are copied unchanged (the latter still embed their first 150 description characters).
The original titles file is not touched. Validation rows of script 99 are ignored.

Run (project root, venv active):
    python -m diagnostics.99c_merge_inferred_titles --label jobbland
Output: data/tagged/titles_<label>_inf.jsonl

Then cluster with the inferred titles under a separate board name, so nothing is overwritten (Colab, as before):
    python -m diagnostics.92_cluster_postings --board jobbland_inf --titles data/tagged/titles_jobbland_inf.jsonl ...
and run script 93 with  --board jobbland_inf --nuts data/tagged/nuts2_jobbland.jsonl --titles data/tagged/titles_jobbland.jsonl
(the ORIGINAL titles file, so that the postings without a real title are still counted as title-less).
"""

import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--label", required=True)
    ap.add_argument("--titles")
    ap.add_argument("--inferred")
    ap.add_argument("--out")
    a = ap.parse_args()
    tp = a.titles or f"data/tagged/titles_{a.label}.jsonl"
    ip = a.inferred or f"data/tagged/inferred_titles_{a.label}.jsonl"
    op = a.out or f"data/tagged/titles_{a.label}_inf.jsonl"
    inf = {}
    for l in open(ip, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            if r["kind"] == "inferred":
                inf[str(r["id"])] = r["title_inferred"]
    n = used = unk = missing = 0
    with open(op, "w", encoding="utf-8") as f:
        for l in open(tp, encoding="utf-8"):
            if not l.strip():
                continue
            r = json.loads(l)
            n += 1
            if not r.get("has_title", True):
                t = inf.get(str(r["id"]))
                if t is None:
                    missing += 1
                elif t == "UNKNOWN":
                    unk += 1
                else:
                    r["title_clean"], r["has_title"], r["title_source"] = t, True, "inferred"
                    used += 1
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{n:,} postings; {used:,} got an inferred title, {unk:,} stay title-less (UNKNOWN), {missing:,} title-less postings have no inferred title; written {op}")


if __name__ == "__main__":
    main()
