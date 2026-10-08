"""
Do different sources contain the same postings?

Why: in the postings sample the pairs jobmedic / jobmedic.co.uk,
jobbland / jobbland.se, lesjeudis / lesjeudis.com and jobbguru / jobbguru.se
have identical sample sizes, identical year splits and identical sector
counts. That is unlikely for independent draws, so this checks whether the
same postings appear under more than one source name (or twice within one
source). If they do, per-source and per-country counts are inflated and the
duplicates must be handled before any aggregate is reported.

Three matching keys are used, from strict to loose:
  id           the API's own `id` (or `source_id`)
  content      normalised (title, organization, location, upload date)
  description  hash of the first 300 normalised characters of the description

Usage, from the repo root:
    python -m diagnostics.20_check_duplicate_postings
"""

import hashlib
import json
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

POSTINGS_PATH = Path("data/raw/postings_sample.jsonl")
OUT_PATH = Path("data/raw/duplicate_check.json")
MIN_DESCRIPTION_CHARS = 80
TOP_PAIRS = 20


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def norm(value):
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip().lower()


def key_id(p):
    for field in ("id", "source_id"):
        if p.get(field) not in (None, ""):
            return f"{field}:{p[field]}"
    return None


def key_content(p):
    parts = [norm(p.get("title")), norm(p.get("organization")), norm(p.get("location")),
             norm(p.get("upload_date"))[:10]]
    return "|".join(parts) if parts[0] else None


def key_description(p):
    text = norm(p.get("description"))
    if len(text) < MIN_DESCRIPTION_CHARS:
        return None
    return hashlib.md5(text[:300].encode("utf-8")).hexdigest()


KEYS = {"id": key_id, "content": key_content, "description": key_description}


def analyse(postings, key_fn):
    groups = defaultdict(list)
    for index, p in enumerate(postings):
        k = key_fn(p)
        if k is not None:
            groups[k].append(index)

    keyed = sum(len(v) for v in groups.values())
    within = Counter()
    pairs = Counter()
    for members in groups.values():
        if len(members) < 2:
            continue
        sources = [postings[i].get("source", "UNKNOWN") for i in members]
        for source, c in Counter(sources).items():
            if c > 1:
                within[source] += c - 1
        for a, b in combinations(sorted(set(sources)), 2):
            pairs[(a, b)] += 1
    return keyed, within, pairs


def main():
    postings = load(POSTINGS_PATH)
    sizes = Counter(p.get("source", "UNKNOWN") for p in postings)
    print(f"{len(postings):,} postings loaded from {len(sizes)} sources.\n")
    report = {}

    for name, fn in KEYS.items():
        keyed, within, pairs = analyse(postings, fn)
        print(f"=== Key: {name} (usable on {keyed:,} of {len(postings):,} postings) ===")
        if within:
            print("Repeated inside one source (extra copies):")
            for source, c in within.most_common():
                print(f"  {source:<18} {c:>6} ({c / sizes[source]:.1%} of its sample)")
        else:
            print("No repeats inside a single source.")
        if pairs:
            print("Shared between two sources (keys present in both):")
            for (a, b), c in pairs.most_common(TOP_PAIRS):
                smaller = min(sizes[a], sizes[b])
                print(f"  {a:<16} / {b:<16} {c:>6} shared ({c / smaller:.1%} of the smaller sample)")
        else:
            print("No key shared between two sources.")
        print()
        report[name] = {
            "usable": keyed,
            "repeats_within_source": dict(within),
            "shared_between_sources": {f"{a} / {b}": c for (a, b), c in pairs.items()},
        }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
