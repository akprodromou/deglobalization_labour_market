"""Reading a lexicon file and matching its terms in text (used by scripts 55, 56, 58).

A lexicon file is a CSV with the columns
    term, channel, lang, variants, from_brief, note
`variants` holds alternative spellings separated by `|`. Each term (and each
variant) is turned into a regular expression that

  * ignores case and does not match inside a longer word at the start;
  * accepts a hyphen, a space or nothing where the term has a hyphen
    ("friend-shoring" also matches "friendshoring" and "friend shoring");
  * accepts a hyphen or a space where the term has a space;
  * accepts a plural -s/-es on the last word of an English term
    ("export control" matches "export controls");
  * for Swedish terms (lang = sv) accepts any word ending ("exportkontroll"
    matches "exportkontrollen").
"""

import csv
import re
from pathlib import Path


def term_regex(term, lang="en"):
    parts = re.split(r"([-\s]+)", term.strip())
    out = []
    for p in parts:
        if not p:
            continue
        if re.fullmatch(r"[-\s]+", p):
            out.append(r"[-\s]?" if "-" in p else r"[-\s]+")
        else:
            out.append(re.escape(p.lower()))
    body = "".join(out)
    tail = r"\w*" if lang == "sv" else r"(?:e?s)?"
    return r"(?<!\w)" + body + tail + r"(?!\w)"


def read_lexicon(path):
    """List of dicts: term, channel, lang, variants (list), from_brief, note."""
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if not (r.get("term") or "").strip():
                continue
            r["term"] = r["term"].strip()
            r["lang"] = (r.get("lang") or "en").strip() or "en"
            r["variants"] = [v.strip() for v in (r.get("variants") or "").split("|") if v.strip()]
            rows.append(r)
    return rows


def _key(form):
    """Longest alphabetic chunk of a term, lower-case: if the term matches, this
    chunk is in the text (used only to skip regexes that cannot match)."""
    toks = re.findall(r"[^\W\d_]+|\d+", form.lower())
    return max(toks, key=len) if toks else ""


class Entry(tuple):
    """(row, regex) pair that also carries the key words used as a pre-filter."""

    def __new__(cls, row, rx, keys):
        obj = super().__new__(cls, (row, rx))
        obj.keys = keys
        return obj


def compile_lexicon(rows):
    """[(row, compiled regex over the term and its variants)]."""
    out = []
    for r in rows:
        forms = [r["term"]] + r["variants"]
        alts = [term_regex(t, r["lang"]) for t in forms]
        rx = re.compile("|".join(alts), re.IGNORECASE)
        out.append(Entry(r, rx, [k for k in (_key(f) for f in forms) if k]))
    return out


def match_terms(compiled, text):
    """Terms of the lexicon found in `text`: list of (row, matched string).
    A regex is tried only if one of the term's key words occurs in the text."""
    low = text.lower()
    hits = []
    for e in compiled:
        r, rx = e
        if e.keys and not any(k in low for k in e.keys):
            continue
        m = rx.search(text)
        if m:
            hits.append((r, m.group(0)))
    return hits


def context(text, matched, width=160):
    """A short snippet around the first occurrence of `matched`."""
    i = text.lower().find(matched.lower())
    if i < 0:
        return ""
    s = max(0, i - width)
    return re.sub(r"\s+", " ", text[s:i + len(matched) + width]).strip()
