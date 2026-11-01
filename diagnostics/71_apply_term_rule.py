"""
Month 3, step 11: keep a `critical materials` tag only if the posting matched a term tied to the EU lists.

Why: prompt v9 defines critical materials by the EU strategic and critical raw materials lists, which exclude iron ore.
Qwen 2.5 7B did not apply that rule: in the v9 run 15 of its 29 `critical materials` tags rested only on the lexicon
term "mining and mineral" (LKAB iron-ore and Boliden postings) and 2 more on "precious metals" or "batteries" alone.
A written rule fixes this without a model: a `critical materials` tag stays only if at least one matched lexicon term is
one of the EU-anchored terms below; otherwise the tag becomes `none` (intensity `none`). Every other tag is untouched.
Changed tags keep the model's answer in `model_channel` / `model_intensity` and get `rule = "no_eu_anchored_term"`.

EU-anchored terms: critical raw materials, rare earths, strategic raw materials, battery materials, lithium,
raw materials security, critical metals, strategic resource, battery recycling.
Not anchored (so not enough on their own): mining and mineral, precious metals, batteries, battery storage,
battery manufacturing (battery production is reshoring in the guide).

Run (project root):
    python -m diagnostics.71_apply_term_rule --tags data/tagged/tags_qwen2.5_7b_tagging_v9.jsonl
Writes data/tagged/tags_qwen2.5_7b_tagging_v9r.jsonl and prints how many tags changed.
"""

import argparse
import json
from collections import Counter
from pathlib import Path

ANCHORED = {"critical raw materials", "rare earths", "strategic raw materials", "battery materials", "lithium",
            "raw materials security", "critical metals", "strategic resource", "battery recycling"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--tags", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    src = Path(args.tags)
    out = Path(args.out or src.with_name(src.name.replace("_v9.jsonl", "_v9r.jsonl")))
    n = changed = 0
    by_term = Counter()
    with open(src, encoding="utf-8") as f, open(out, "w", encoding="utf-8") as g:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            n += 1
            if r.get("ok") and r.get("channel") == "critical materials" and not (set(r.get("terms") or []) & ANCHORED):
                r["model_channel"], r["model_intensity"] = r["channel"], r.get("intensity")
                r["channel"], r["intensity"] = "none", "none"
                r["rule"] = "no_eu_anchored_term"
                changed += 1
                by_term.update(r.get("terms") or [])
            g.write(json.dumps(r, ensure_ascii=False) + "\n")
    kept = sum(1 for line in open(out, encoding="utf-8") if line.strip() and json.loads(line).get("channel") == "critical materials")
    print(f"{n:,} tags; {changed} critical-materials tags changed to none; {kept} critical-materials tags remain -> {out}")
    print("matched terms of the changed tags:", dict(by_term))


if __name__ == "__main__":
    main()
