"""
Month 4, step 2: clean the posting titles (input A of the occupation clustering) for ONE board.

What is removed, and nothing else:
  * gender markers: (m/f/d), (m/w/d), (H/F), (F/H), M/F, F/M ...
  * a leading reference code that contains a digit and a hyphen (e.g. "RA-d2m-122 Innovation Coordinator")
  * a trailing reference code (IRC207099, 2024-112135, HT2025PM0103) and single (m)/(w) markers
  * trailing segments after a spaced separator (" - ", " | ", en dash) that look like an employer or a place:
      - the segment ends with a company-form word (AB, GmbH, AG, SAS, SARL, SA, Oy, AS, Inc, Ltd, LLC, KG, SE)
      - or contains municipality, kommun, region, county, university, universitet, hospital, group, groupe
      - or contains a comma (a place list such as "Fontenay-Sous-Bois, Ile de France, France")
      - or equals a word of the posting's own location field
    * or is a last segment that ends >= 25 titles of the same board (employers without a legal form, e.g. GlobalLogic)
    A segment starting with a digit ("75 - 100%") is never dropped.
    The first segment is always kept, and a segment that matches none of these is kept (so "GenAi - Manager / Consultant
    Senior" keeps its content). Hyphens inside words are never touched (only SPACED separators split).
Stage 2 (added after the first clustering showed that place and employer words pull titles into clusters of their own: "Cyber Security
Engineer to Helsingborg" and "Solution architect for Stockholm or Uppsala!" sat in a "project manager ... " cluster):
  * lead-in sentences: "<Employer> is looking for a Test Automatizer!" -> "Test Automatizer"
  * filler: wanted, wanted immediately, needed, urgent, hourly employment, part-time, full-time, until further notice, percentages,
    "summer 2026", years, exclamation marks
  * trailing places: "Personal Assistant Lidingo", "Solution architect for Stockholm or Uppsala" (a place is a name that occurs as a
    location in at least 3 postings of the board, or the posting's own location)
  * a trailing "for / to / at / with + Name": "Nurse for Enebacken", "Fullstack developer for Norconsult Digital Stockholm". Only a tail of
    capitalised words that the board otherwise writes as proper names (not as ordinary words) is cut, so "Specialist in Internal Medicine" and
    "Engineer for battery production" are kept. After "at / hos / bei / chez" one proper name in the tail is enough.
The report lists what stage 2 removed most often, 60 before / after pairs, the common words it removed (a check for over-removal) and
the named-occupation titles (script 92) before and after, so a removed word that matters shows up. --no-stage2 gives the old cleaning.
Titles are NOT translated: the next step uses multilingual-e5, which reads Swedish, German and French titles.

Output: data/tagged/titles_<label>.jsonl, one line per posting (duplicates removed as in the tagger):
  {"id", "day", "title", "title_clean", "has_title", "desc_start"}   desc_start = first 150 characters of the description,
used only as a fallback text for postings without a title.
The report lists the share of titles that changed and 25 random before/after pairs to check by eye.

Run (project root, one board per run):
    python -m diagnostics.90_prepare_titles --corpus <the board's corpus files> --label jobbland
Writes data/tagged/titles_<label>.jsonl and docs/titles_<label>.md
"""

import argparse
import json
import random
import re
import tempfile
import unicodedata
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

G = r"[mwfhdx]"
GENDER_RX = re.compile(rf"\(?\s*(?<![A-Za-z]){G}\s*[/|]\s*{G}(?:\s*[/|]\s*{G})?(?:\s*[/|]\s*nb)?(?![A-Za-z])\s*\)?", re.I)
SINGLE_G_RX = re.compile(r"\(\s*[mwfd]\s*\)", re.I)
TRAIL_CODE_RX = re.compile(r"\s*\(?\b(?:[A-Z]{2,4}\d{5,}|[A-Z]{1,3}\d{4}[A-Z]{1,3}\d{3,}|\d{4}-\d{4,})\b\)?\s*$")
REF_RX = re.compile(r"^\s*(?=\S*\d)[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+\s+")
SEP_RX = re.compile(r"\s+[-–—|]\s+")
FORM_RX = re.compile(r"\b(ab|aktiebolag|gmbh|ag|sas|sarl|sa|oy|as|inc|ltd|llc|kg|se)\.?$", re.I)
WORD_RX = re.compile(r"\b(municipality|kommun|region|county|university|universitet|hospital|group|groupe)\b", re.I)


def clean_title(title, location="", employers=frozenset()):
    t = unicodedata.normalize("NFKC", title or "")
    t = re.sub(r"\s+", " ", t).strip()
    if not t:
        return ""
    t = GENDER_RX.sub(" ", t)
    t = SINGLE_G_RX.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip(" -–—|,;:")
    t = REF_RX.sub("", t)
    loc_words = {w.lower() for w in re.findall(r"[^\W\d_]{4,}", location or "")}
    segs = SEP_RX.split(t)
    keep = [segs[0]]
    for s in segs[1:]:
        s = s.strip()
        if s[:1].isdigit():  # "75 - 100%, ..." : a percentage range, not an employer
            keep.append(s)
            continue
        drop = (s.lower() in employers or FORM_RX.search(s) or WORD_RX.search(s) or "," in s or s.lower() in loc_words
                or (loc_words and {w.lower() for w in re.findall(r"[^\W\d_]{4,}", s)} and
                    {w.lower() for w in re.findall(r"[^\W\d_]{4,}", s)} <= loc_words))
        if not drop:
            keep.append(s)
    out = " - ".join(keep)
    out = TRAIL_CODE_RX.sub("", out)
    out = re.sub(r"\s+", " ", out).strip(" -–—|,;:").rstrip(" .")
    return out or re.sub(r"\s+", " ", title or "").strip()


from collections import Counter

RULES = Counter()          # how often each stage-2 rule changed a title (printed in the report)
PREPS = {"to", "for", "with", "till", "för", "für", "zu", "pour", "à", "au", "aux", "dans", "en", "in", "i", "på", "im", "at", "hos", "bei", "chez", "mit", "med", "of"}
EMP_PREPS = {"to", "for", "till", "för", "at", "hos", "chez"}      # prepositions that can introduce an employer (never für, à, en, pour, in)
EMP_AT = {"at", "hos", "chez"}
LINKS = {"or", "and", "&", "/", ",", "eller", "och", "oder", "und", "ou", "et"}
SMALL = {"the", "a", "an", "of", "and", "or", "in", "to", "for", "at", "with", "de", "la", "le", "du", "des", "der", "die", "das", "och", "i", "på", "för"}
DANGLE = {"central", "centrala", "die", "der", "das", "den", "dem", "the", "our", "unsere", "unseren", "unser", "northern", "southern", "western", "eastern", "norra", "södra", "västra", "östra", "greater", "north", "south", "west", "east", "region", "county", "län", "municipality", "kommun", "st", "sankt", "saint", "about", "ca", "approx", "circa", "cirka", "ungefär", "from", "ab", "von", "bis", "until", "around", "im"}
MONTHS = (r"jan(?:uary|uar|uari|vier)?|jänner|feb(?:ruary|ruar|ruari|rier)?|mar(?:ch|z|s)?|märz|mars|apr(?:il)?|may|mai|maj|jun(?:e|i|)|juin|jul(?:y|i)?|juillet|"
          r"aug(?:ust|usti)?|août|sep(?:t|tember)?|septembre|oct(?:ober)?|okt(?:ober)?|octobre|nov(?:ember)?|novembre|dec(?:ember)?|dez(?:ember)?|décembre")
PCT = r"\d{1,3}(?:[.,]\d+)?\s?(?:[-–]\s?\d{1,3}(?:[.,]\d+)?\s?)?%"
LEAD_RX = re.compile(r"^.{2,70}?\b(?:is|are)\s+(?:now\s+)?(?:looking for|searching for|seeking|recruiting|hiring|in need of)\s+"
                     r"(?:an?\s+|the\s+|some\s+|several\s+|new\s+)?(?P<role>.{3,})$", re.I)
LEAD2_RX = re.compile(r"^(?:now\s+)?(?:we are looking for|we are seeking|looking for|we need|wanted:?)\s+(?:an?\s+|the\s+|some\s+|several\s+)?(?P<role>.{3,})$", re.I)
REFCUT_RX = re.compile(r"\s*[,;(\[]?\s*\b(?:Kennzahl|Kennziffer|Chiffre|Referenz(?:nummer)?|Ref\.?|Job[- ]?ID)\s*[:#]?\s*\S*\d.*$", re.I)
AGEBAND_RX = re.compile(r"\s*,?\s*\bAltersbereich\b.*$", re.I)
ADDR_RX = re.compile(r"\b[\wäöüÄÖÜß-]*(?:straße|strasse|str\.|weg|platz|allee|gasse|ring|damm|stieg|halde|morgen)\s*\d+(?:\s?[a-zA-Z]\b)?(?:\s?[/-]\s?\d+)?|"
                     r"\b[\wäöüÄÖÜß-]+\s+(?:Straße|Strasse|Str\.|Weg|Platz|Allee|Gasse)\s*\d+(?:\s?[a-zA-Z]\b)?(?:\s?[/-]\s?\d+)?", re.I)
START_RX = re.compile(rf"\b(?:ab|from|starting(?:\s+from)?|beginning|zum|per|as of|dès|à partir de|från)\s+"
                      rf"(?:\d{{1,2}}\.\s?\d{{1,2}}\.?(?:\s?20\d\d)?|(?:\d{{1,2}}(?:st|nd|rd|th)?\.?\s+)?(?:{MONTHS})\b\.?(?:\s+\d{{1,2}}(?:st|nd|rd|th)?(?!\d))?(?:\s+20\d\d)?|20[2-3]\d)", re.I)
CONTRACT_RX = re.compile(rf"\(\s*{PCT}(?:\s*[-–]\s*{PCT})?\s*\)|(?:\b(?:about|ca\.?|approx\.?|circa|cirka|ungefär)\s+)?(?<![\w/])\b{PCT}|"
                         r"(?:(?<![/\w-])in\s+)?\b(?:voll|teil)[- ]?zeit\b|(?:(?<![/\w-])in\s+)?\b(?:voll|teil)-\s*(?:/|oder|und|&)\s*(?:voll|teil)zeit\b|"
                         r"\b(?:full|part)[- ]?time\s*(?:/|or|and|&)\s*(?:full|part)[- ]?time\b|"
                         r"\b(?:full|part)[- ]?(?:/|or|and|&)\s*(?:full|part)[- ]?time\b|\b(?:(?<![/\w-])in\s+)?(?:full|part)[- ]?time\b|"
                         r"\b(?:à\s+)?temps (?:plein|partiel)\b", re.I)
CDI_RX = re.compile(r"(?:\s*[-–—/]\s*)?\b(?:en\s+|in\s+)?(?:CDI|CDD)\b(?:\s*[-–—]\s*)?", re.I)
FILLER_RX = re.compile(r"\b(?:(?:is|are)\s+wanted|wanted(?:\s+(?:immediately|now|urgently))?|needed|urgent(?:ly)?|immediately|hourly(?:\s+employment)?|"
                       r"until further notice|(?:summer|autumn|fall|winter|spring)\s+20\d\d|\d{1,3}\s?h/v)\b[!.]*|(?<![\d./-])20[2-3]\d(?![\d/-])", re.I)
IFNEEDED_RX = re.compile(r"\b(if|as|when|where|is|are|be|only)\s+needed\b", re.I)
TAILFRAME_RX = re.compile(r"\s+(?:im\s+(?:Raum|Großraum|Umkreis)|in\s+and\s+around|in\s+the\s+(?:area|region)(?:\s+of)?|in\s+der\s+(?:Region|Umgebung))\s*$", re.I)
KEEPPUNCT = {"++", "+", "#"}
TOK_CLEAN = re.compile(r"^[\W_]+|[\W_]+$")


def tclean(w):
    return TOK_CLEAN.sub("", w).lower()


def trim(t):
    """strip separators at both ends, but keep a leading '.' of '.NET' and a trailing '#' / '++' of 'C#' / 'C++'."""
    t = t.strip(" -–—|,;:")
    while t.endswith(".") and not re.search(r"\b[A-Za-z]{1,2}\.$", t):
        t = t[:-1].rstrip(" -–—|,;:")
    return t


def hy(s):
    return s.replace("-", " ")


def board_stats(titles, locations):
    """places: names that occur as a location in >= 3 postings (hyphens read as spaces). common: words the board writes in lower case
    at least as often as capitalised. title_case: share of capitalised words inside titles (high on boards that write Title Case or German nouns),
    where capitalisation says nothing about proper names, so the employer-tail rule is switched off."""
    pc = Counter()
    for loc in locations:
        for part in re.split(r"[,/;()]| - ", loc or ""):
            part = re.sub(r"\s+", " ", hy(part)).strip().lower()
            if 3 <= len(part) <= 40 and not part.isdigit():
                pc[part] += 1
    places = frozenset(k for k, v in pc.items() if v >= 3)
    low, cap = Counter(), Counter()
    for t in titles:
        ws = (t or "").split()
        if not ws or t.isupper():
            continue
        for w in ws[1:]:
            c = tclean(w)
            if c.isalpha() and c not in SMALL and len(c) > 2:
                (cap if w[:1].isupper() else low)[c] += 1
    common = set()
    for c in set(low) | set(cap):
        n = low[c] + cap[c]
        if n >= 5 and low[c] / n >= 0.5:
            common.add(c)
    tot_c, tot_l = sum(cap.values()), sum(low.values())
    return places, frozenset(common), tot_c / max(1, tot_c + tot_l)


def strip_places(t, places, extra=frozenset()):
    ws = t.split()
    changed = True
    while changed and len(ws) >= 2:
        changed = False
        while ws and tclean(ws[-1]) == "" and ws[-1] not in KEEPPUNCT and ")" not in ws[-1] and "]" not in ws[-1]:
            ws.pop()
        for n in (4, 3, 2, 1):
            if len(ws) > n:
                name = " ".join(hy(tclean(w)) for w in ws[-n:])
                first = name.split(" ")[0]
                if name in places or name in extra or (n == 1 and "-" in ws[-1] and first in places and len(first) >= 4):
                    ws = ws[:-n]
                    while ws and (is_dangler(ws[-1])):
                        ws.pop()
                    changed = True
                    RULES["place"] += 1
                    break
    return " ".join(ws)


def is_dangler(w):
    c = tclean(w)
    if w in KEEPPUNCT:
        return False
    if w in ('"', "'", "»", "”", "“") or any(ch in w for ch in "€$£"):
        return False
    if c == "":
        return not (")" in w or "]" in w)
    if len(w) == 1 and w.isupper():           # "Engineer I": a level, not the Swedish preposition
        return False
    return c in PREPS or c in LINKS or c in DANGLE


def is_proper(w, common, places):
    c = tclean(w)
    if not c or c in SMALL:
        return None          # neutral
    if c in places:
        return True
    if not w[:1].isupper() and not w.isupper():
        return False
    return c not in common


def strip_proper_tail(t, common, places):
    """cut 'to / for / at + Name' when every word of Name looks like a proper name (not a word the board also writes in lower case).
    Only employer prepositions; 'in' and the German / French 'für', 'à', 'en', 'pour' are left alone because they introduce the field of work."""
    if t.isupper():
        return t
    ws = t.split()
    for i in range(len(ws) - 2, 0, -1):
        pw = tclean(ws[i])
        if pw not in EMP_PREPS:
            continue
        tail = ws[i + 1:]
        if not tail or len(tail) > 6:
            continue
        real = [f for f in (is_proper(w, common, places) for w in tail) if f is not None]
        if not real:
            continue
        ok = any(real) and real[0] is not False if pw in EMP_AT else (all(real) and real[0])
        if ok:
            RULES["employer tail"] += 1
            return " ".join(ws[:i])
    return t


def clean_stage2(t, places, common, loc="", use_tail=True):
    orig = t
    if not t:
        return t
    for rx in (LEAD_RX, LEAD2_RX):
        m = rx.match(t)
        if m:
            role = m.group("role")
            if re.fullmatch(r"(?:you|us|someone|people|colleagues?|new colleagues?|more|dig|dej|er|vous|toi)[ !?.]*", role.strip(), re.I) or len(role.strip()) < 4:
                RULES["lead-in kept (role is a pronoun)"] += 1
                break
            t = role
            RULES["lead-in sentence"] += 1
            break
    t0 = t
    t = IFNEEDED_RX.sub(lambda m: m.group(1) + " NEEDEDKEEP", t)
    t = REFCUT_RX.sub("", t)
    t = AGEBAND_RX.sub("", t)
    t = ADDR_RX.sub(" ", t)
    if t != t0:
        RULES["reference / address"] += 1
    t1 = t
    t = START_RX.sub(" ", t)
    if t != t1:
        RULES["start date"] += 1
    t1 = t
    t = CONTRACT_RX.sub(" ", t)
    t = CDI_RX.sub(" - ", t)
    t = re.sub(r"\s*[/(]\s*NB\s*\)?", " ", t)
    t = FILLER_RX.sub(" ", t)
    t = t.replace("NEEDEDKEEP", "needed")
    if t != t1:
        RULES["filler / hours / contract"] += 1
    t = re.sub(r"[!?]+", " ", t)
    t = re.sub(r"[(\[]\s*[-–—]?\s*[)\]]", " ", t)
    t = re.sub(r"\(\s*[,;]\s*", "(", t)
    t = re.sub(r"(?:\s*[-–—]\s*){2,}", " - ", t)
    t = re.sub(r",\s*(?:,\s*)+", ", ", t)
    t = re.sub(r"\s+([,;:])", r"\1", t)
    t = re.sub(r"\s+", " ", t)
    t = trim(t)
    extra = frozenset(hy(w.lower()) for w in re.findall(r"[^\W\d_]{4,}", loc or ""))
    t = strip_places(t, places, extra)
    if use_tail:
        t = strip_proper_tail(t, common, places)
        t = strip_places(t, places, extra)
    t = TAILFRAME_RX.sub("", t)
    ws = t.split()
    while len(ws) > 1 and tclean(ws[0]) in LINKS and ws[0] not in KEEPPUNCT:
        ws.pop(0)
    while len(ws) > 1 and is_dangler(ws[-1]):
        ws.pop()
    t = trim(" ".join(ws))
    t = re.sub(r"[\[(]\s*[\])]", "", t)
    if "(" not in t:
        t = re.sub(r"\s*\)+$", "", t)
    t = trim(re.sub(r"\s+", " ", t))
    return t if len(t) >= 3 else orig


def frequent_suffixes(titles, min_count=25):
    """Last spaced segments that end >= min_count titles of the board: employers without a legal-form word
    (GlobalLogic, Omegapoint ...), and place names. Data-driven, so no employer list is needed."""
    from collections import Counter
    c = Counter()
    for t in titles:
        segs = SEP_RX.split(re.sub(r"\s+", " ", t or "").strip())
        if len(segs) > 1 and not segs[-1][:1].isdigit():
            c[segs[-1].strip().lower()] += 1
    return frozenset(k for k, v in c.items() if v >= min_count and len(k) > 1)


def load_all(paths):
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tmp:
        for p in paths:
            for line in open(p, encoding="utf-8"):
                if line.strip():
                    tmp.write(line.rstrip("\n") + "\n")
        name = tmp.name
    try:
        return load_corpus(name)
    finally:
        Path(name).unlink()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--tail", choices=["auto", "on", "off"], default="auto", help="employer-tail rule (to / for / at + Name): auto = on when the capitalised-word share is below 55%%")
    ap.add_argument("--no-stage2", action="store_true", help="old cleaning only (stage 1)")
    args = ap.parse_args()
    rows, dup = load_all(args.corpus)
    out = Path(f"data/tagged/titles_{args.label}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    employers = frequent_suffixes([(r["item"].get("title") or "") for r in rows])
    recs = []
    stage1 = [clean_title((r["item"].get("title") or "").strip(), r["item"].get("location") or "", employers) for r in rows]
    places, common, tc = board_stats(stage1, [r["item"].get("location") or "" for r in rows])
    use_tail = (tc < 0.55) if args.tail == "auto" else args.tail == "on"
    for r, c1 in zip(rows, stage1):
        it = r["item"]
        t = (it.get("title") or "").strip()
        c = c1 if args.no_stage2 else clean_stage2(c1, places, common, it.get("location") or "", use_tail)
        recs.append({"id": str(it["id"]), "day": r["day"], "title": t, "title_stage1": c1, "title_clean": c, "has_title": bool(t),
                     "desc_start": re.sub(r"\s+", " ", (it.get("description") or ""))[:150].strip()})
    with open(out, "w", encoding="utf-8") as f:
        for x in recs:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    n = len(recs)
    titled = [x for x in recs if x["has_title"]]
    changed = [x for x in titled if x["title_clean"] != re.sub(r"\s+", " ", x["title"]).strip()]
    random.seed(args.seed)
    sample = random.sample(changed, min(25, len(changed)))
    md = [f"# Title cleaning: {args.label}", "",
          f"{n:,} postings after removing {dup:,} duplicates; {n-len(titled):,} without a title; "
          f"{len(changed):,} titles changed ({len(changed)/max(1,len(titled)):.1%} of the titled ones).", "",
          "## 25 random before / after pairs (changed titles only)", ""]
    md += [f"- `{x['title']}`  ->  `{x['title_clean']}`" for x in sample]
    if not args.no_stage2:
        from collections import Counter
        ch2 = [x for x in titled if x["title_clean"] != x["title_stage1"]]
        md += ["", f"## Stage 2: {len(ch2):,} titles changed ({len(ch2)/max(1,len(titled)):.1%} of the titled ones); {len(places):,} place names, {len(common):,} common words known; capitalised-word share {tc:.0%} -> employer-tail rule {'ON' if use_tail else 'OFF'}", "",
              "Rule counts: " + ", ".join(f"{k} {v:,}" for k, v in RULES.most_common()), ""]
        removed = Counter()
        removed_common = Counter()
        for x in ch2:
            a_, b_ = x["title_stage1"].split(), x["title_clean"].split()
            tail = " ".join(a_[len(b_):]) if a_[:len(b_)] == b_ else ""
            if tail:
                removed[tail.lower()] += 1
            for w in a_:
                if tclean(w) in common and tclean(w) not in {tclean(v) for v in b_} and tclean(w) not in PREPS and tclean(w) not in SMALL:
                    removed_common[tclean(w)] += 1
        md += ["### Most frequent removed tails (the text cut off the end)", ""]
        md += [f"- `{k}` ({v})" for k, v in removed.most_common(40)]
        md += ["", "### Ordinary words that stage 2 removed most often (check that none carries the occupation)", ""]
        md += [f"- `{k}` ({v})" for k, v in removed_common.most_common(40)]
        big = sorted(ch2, key=lambda x: len(x["title_stage1"].split()) - len(x["title_clean"].split()), reverse=True)[:30]
        md += ["", "### 30 largest cuts (most words removed by stage 2; read these first)", ""]
        md += [f"- `{x['title_stage1']}`  ->  `{x['title_clean']}`" for x in big]
        random.seed(args.seed + 1)
        smp = random.sample(ch2, min(60, len(ch2)))
        md += ["", "### 60 random stage-2 before / after pairs", ""]
        md += [f"- `{x['title_stage1']}`  ->  `{x['title_clean']}`" for x in smp]
        try:
            try:
                from diagnostics.cluster_named import NAMED_RX
            except ImportError:
                import importlib.util
                sp = importlib.util.spec_from_file_location("c92", str(Path(__file__).with_name("92_cluster_postings.py")))
                m_ = importlib.util.module_from_spec(sp)
                sp.loader.exec_module(m_)
                NAMED_RX = m_.NAMED_RX
            md += ["", "### Named-occupation titles (script 92) before and after stage 2", "", "| occupation | stage 1 | after stage 2 | lost | gained |", "|---|---|---|---|---|"]
            for k, rx in NAMED_RX.items():
                b1 = {x["id"] for x in titled if rx.search(x["title_stage1"])}
                b2 = {x["id"] for x in titled if rx.search(x["title_clean"])}
                md.append(f"| {k} | {len(b1)} | {len(b2)} | {len(b1 - b2)} | {len(b2 - b1)} |")
        except Exception as e:
            md += ["", f"(named-occupation check skipped: {e})"]
    md += ["", f"## {len(employers)} frequent trailing segments removed as employers/places (>= 25 titles)", ""]
    md += [f"- {e}" for e in sorted(employers)[:60]]
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/titles_{args.label}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{n:,} postings ({dup:,} duplicates removed); {n-len(titled):,} without a title; "
          f"{len(changed):,} titles changed -> {out}, docs/titles_{args.label}.md")


if __name__ == "__main__":
    main()
