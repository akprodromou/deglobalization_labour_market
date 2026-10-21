"""Shared helpers for the Month 3 lexicon and tagging scripts (55 to 60).

Kept in one small module so that the corpus is read, de-duplicated and
weighted in exactly one way everywhere (same rules as script 53).

    load_corpus(path)         postings with day weights, exact duplicates dropped
    norm(text)                lower-case, punctuation to spaces
    segments(text)            text cut at sentence, list and bracket breaks
    words(segment)            alphabetic words (hyphen/apostrophe inside a word kept)
    frequent_ngrams(...)      document frequency of 1..n-grams without keeping
                              every rare n-gram in memory (Apriori pruning)
"""

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

STOP = set(ENGLISH_STOP_WORDS) | {"will", "also", "may", "within", "including", "etc"}
_SEG_RX = re.compile(r"[.!?;:,\n\r\t•·|()\[\]{}/\"“”]+")
_WORD_RX = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*")


def norm(t):
    return re.sub(r"\W+", " ", (t or "").lower()).strip()


def posting_text(item, max_chars=None):
    t = ((item.get("title") or "").strip() + ". " + (item.get("description") or "")).strip()
    return t[:max_chars] if max_chars else t


def load_corpus(path):
    """Deduplicated postings with their day weights.

    Each posting of the day-stratified corpus (script 52) stands for
    (day total / postings taken that day) postings of its day. Exact duplicate
    descriptions are dropped and the day weight recomputed, as in script 53
    (an approximation: the population is treated as distinct texts).
    Returns (list of {"item", "day", "w"}, number of duplicates dropped).
    """
    by_day = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            for it in r["items"]:
                by_day[r["day"]].append((r["total"], it))
    seen, out, dropped = set(), [], 0
    for day in sorted(by_day):
        kept = []
        for total, it in by_day[day]:
            h = hashlib.md5(norm(it.get("description")).encode()).hexdigest()
            if h in seen:
                dropped += 1
                continue
            seen.add(h)
            kept.append((total, it))
        for total, it in kept:
            out.append({"item": it, "day": day, "w": total / len(kept)})
    return out, dropped


def segments(text):
    return [s for s in _SEG_RX.split((text or "").lower()) if s.strip()]


def words(segment):
    return _WORD_RX.findall(segment)


def _edge_ok(toks):
    return toks[0] not in STOP and toks[-1] not in STOP and len(toks[0]) > 1 and len(toks[-1]) > 1


def frequent_ngrams(texts, min_df=5, max_n=4):
    """Document frequency of 1..max_n-grams that occur in at least min_df
    documents. N-grams never cross a sentence, comma, bracket or line break.
    Apriori pruning: an n-gram is counted only if its two (n-1)-gram parts are
    already frequent, so rare n-grams never fill the memory.
    Phrases starting or ending with a stop word are dropped from the result
    (a stop word inside, as in "security of supply", is kept).
    Returns {phrase (str): document frequency}.
    """
    docs = [[words(s) for s in segments(t)] for t in texts]

    def count(n, allowed):
        c = Counter()
        for segs in docs:
            seen = set()
            for toks in segs:
                for i in range(len(toks) - n + 1):
                    g = tuple(toks[i:i + n])
                    if allowed is not None and (g[:-1] not in allowed or g[1:] not in allowed):
                        continue
                    seen.add(g)
            c.update(seen)
        return {g: k for g, k in c.items() if k >= min_df}

    level = count(1, None)
    result = {g: k for g, k in level.items() if _edge_ok(g)}
    for n in range(2, max_n + 1):
        level = count(n, set(level))
        if not level:
            break
        result.update({g: k for g, k in level.items() if _edge_ok(g)})
    return {" ".join(g): k for g, k in result.items()}


def project_root():
    return Path.cwd()
