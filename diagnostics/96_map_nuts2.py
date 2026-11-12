"""
Month 4: place every posting in a NUTS-2 region from its location text, with the method recorded.

Order of methods (first that works wins):
  1 field     the posting's own nuts2 field (jobbland.se only; names such as "Västsverige" become codes SE11..SE33)
  2 county    a Swedish county (län) named in the location string -> its NUTS-2 code (fixed official table)
  3 learned   the place name (first part of the location) was seen with a nuts2 field on other postings of the board
  4 manual    a row of the optional --manual csv (columns: place,nuts2) for places the gazetteer does not know
  5 gazetteer the place name is looked up in the GeoNames country file (name, ascii name and alternative names,
              populated places and municipalities ADM3/ADM4); its coordinates are placed in the NUTS-2 polygon of that country
              (GISCO NUTS 2021 level 2). A name with several places in different regions takes the largest
              population and is counted as ambiguous. A point outside every polygon (generalised coasts) takes
              the nearest polygon within 0.15 degrees and is counted as nearest.
  vague       only a country or a multi-country area is named (for example "sweden", "de nordiska länderna"):
              dropped from HHI, and its share is reported.
  unmatched   everything else: listed by size so that a manual row can be added.

Run (project root, venv active); example, lesjeudis:
    python -m diagnostics.96_map_nuts2 --label lesjeudis --country FR --corpus data/raw/corpus_lesjeudis.com_2024-08_2025-04.jsonl data/raw/corpus_lesjeudis.com_2025-05_2025-09.jsonl
Writes data/tagged/nuts2_<label>.jsonl ({"id","nuts2","method"}) and docs/nuts2_<label>.md.
"""
import argparse
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

from shapely.geometry import Point, shape

VAGUE = {"sweden", "sverige", "france", "germany", "deutschland", "allemagne", "europe", "european union", "eu",
         "de nordiska landerna", "nordeuropa", "nordic countries", "emea", "remote", "worldwide"}

LAN = {  # county -> NUTS-2 (Sweden has 21 counties and 8 NUTS-2 regions)
    "stockholms": "SE11",
    "uppsala": "SE12", "sodermanlands": "SE12", "ostergotlands": "SE12", "orebro": "SE12", "vastmanlands": "SE12",
    "jonkopings": "SE21", "kronobergs": "SE21", "kalmar": "SE21", "gotlands": "SE21",
    "blekinge": "SE22", "skane": "SE22",
    "hallands": "SE23", "vastra gotalands": "SE23",
    "varmlands": "SE31", "dalarnas": "SE31", "gavleborgs": "SE31",
    "vasternorrlands": "SE32", "jamtlands": "SE32",
    "vasterbottens": "SE33", "norrbottens": "SE33",
}
SE_NAMES = {"stockholm": "SE11", "ostra mellansverige": "SE12", "smaland med oarna": "SE21", "sydsverige": "SE22",
            "vastsverige": "SE23", "norra mellansverige": "SE31", "mellersta norrland": "SE32", "ovre norrland": "SE33"}


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[-'’.()]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def parts(loc):
    """Location split at commas. In the first part, '... och 2 andra' (and 2 others: a multi-site posting; the
    first place is kept) and '(Bodensee)'-style qualifiers are removed."""
    pp = [x for x in (loc or "").split(",") if x.strip()]
    if pp:
        pp[0] = re.sub(r"\s+(?:och|and)\s+\d+\s+(?:andra|others?)\s*$", "", pp[0], flags=re.I)
        pp[0] = re.sub(r"\([^)]*\)", " ", pp[0]).split("/")[0]
    return [norm(x) for x in pp]


def first_full(loc):
    """First part of the location with its bracket qualifier kept ('Frankfurt (Oder)' -> 'frankfurt oder'), and
    whether there was a qualifier."""
    pp = [x for x in (loc or "").split(",") if x.strip()]
    if not pp:
        return "", False
    f = re.sub(r"\s+(?:och|and)\s+\d+\s+(?:andra|others?)\s*$", "", pp[0], flags=re.I).split("/")[0]
    return norm(f), bool(re.search(r"\([^)]*\)", f))


GENERIC = {"le", "la", "les", "st", "saint", "sainte", "val", "port", "pointe", "mont", "sur", "en", "de", "du", "des",
           "bad", "neu", "alt", "gross", "klein", "sankt", "ober", "unter", "nieder"}


def load_polygons(path, country):
    gj = json.load(open(path, encoding="utf-8"))
    polys = []
    for f in gj["features"]:
        p = f["properties"]
        if p.get("CNTR_CODE") == country and str(p.get("LEVL_CODE", "2")) == "2":
            polys.append((p["NUTS_ID"], shape(f["geometry"])))
    return polys


def region_of(lon, lat, polys):
    pt = Point(lon, lat)
    for code, g in polys:
        if g.covers(pt):
            return code, "exact"
    best = min(((g.distance(pt), code) for code, g in polys), default=(9, None))
    return (best[1], "nearest") if best[0] <= 0.15 else (None, "none")


def load_gazetteer(path):
    idx = defaultdict(list)  # name -> [(population, lat, lon)]
    for line in open(path, encoding="utf-8"):
        c = line.rstrip("\n").split("\t")
        if len(c) < 15 or not (c[6] == "P" or c[7] in ("ADM3", "ADM4")):
            continue
        rec = (int(c[14] or 0), float(c[4]), float(c[5]))
        for n in {c[1], c[2]} | set(c[3].split(",")):
            k = norm(n)
            if k:
                idx[k].append(rec)
    return idx


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--country", required=True, choices=["SE", "FR", "DE"])
    ap.add_argument("--geonames")
    ap.add_argument("--nuts", default="data/geo/nuts2_2021.geojson")
    ap.add_argument("--manual")
    ap.add_argument("--no-gazetteer", action="store_true", help="places that only the gazetteer could place stay unmatched (use for Sweden)")
    a = ap.parse_args()
    a.geonames = a.geonames or f"data/geo/{a.country}.txt"
    items = []
    for p in a.corpus:
        for l in open(p, encoding="utf-8"):
            if l.strip():
                for it in json.loads(l)["items"]:
                    items.append((str(it["id"]), it.get("location") or "", it.get("nuts2")))
    learned = defaultdict(Counter)
    for _, loc, n2 in items:
        pp = parts(loc)
        if n2 and pp and norm(n2) in SE_NAMES:
            learned[pp[0]][SE_NAMES[norm(n2)]] += 1
    learned = {k: v.most_common(1)[0][0] for k, v in learned.items() if len(v) == 1}
    manual = {}
    if a.manual:
        for r in csv.DictReader(open(a.manual, encoding="utf-8")):
            if (r.get("country") or "").strip() in ("", a.country):
                manual[norm(r["place"])] = r["nuts2"].strip()
    polys = load_polygons(a.nuts, a.country)
    gaz = load_gazetteer(a.geonames)
    cache, amb, detail = {}, set(), {}

    def resolve(loc):
        pp = parts(loc)
        if not pp or all(x in VAGUE for x in pp):
            return None, "vague"
        for x in pp[1:]:
            m = re.sub(r" lan$", "", x)
            if x.endswith(" lan") and m in LAN:
                return LAN[m], "county"
        place = pp[0]
        if place in VAGUE:
            return None, "vague"
        if place.endswith(" lan") and re.sub(r" lan$", "", place) in LAN:
            return LAN[re.sub(r" lan$", "", place)], "county"
        if place in learned:
            return learned[place], "learned"
        full, qual = first_full(loc)
        mk = full if full in manual else place
        if mk in manual:
            m = manual[mk]
            return (None, {"OUT": "outside", "VAGUE": "vague"}[m]) if m in ("OUT", "VAGUE") else (m, "manual")
        if a.no_gazetteer:
            return None, "unmatched"
        cand, how = None, "gazetteer"
        if qual and full in gaz:  # the qualifier names a place of its own: Frankfurt (Oder), Halle (Westfalen)
            cand = gaz[full]
        else:
            cand = gaz.get(place)
        if not cand and not qual:  # merged communes and long names: try the leading words ("evry courcouronnes" -> "evry")
            tok = place.split()
            for k in range(len(tok) - 1, 0, -1):
                head = " ".join(tok[:k])
                if len(head) >= 4 and head not in GENERIC and head in gaz:
                    cand, how = gaz[head], "prefix"
                    break
        if not cand:
            return None, "unmatched"
        res = [(pop,) + region_of(lon, lat, polys) for pop, lat, lon in cand]
        res = [r for r in res if r[1]]
        if not res:
            return None, "unmatched"
        if qual and not (full in gaz) and len({r[1] for r in res}) > 1:
            return None, "unmatched"  # the qualifier was dropped and the bare name sits in several regions: no guess
        best = max(res, key=lambda r: r[0])
        if len({r[1] for r in res}) > 1:
            amb.add(place)
            alts = sorted({(r[1], r[0]) for r in res if r[1] != best[1]}, key=lambda t: -t[1])
            detail[place] = (best[1], best[0], alts[:3])
        return best[1], ("nearest" if best[2] == "nearest" else how)

    meth, reg, miss, vag = Counter(), Counter(), Counter(), Counter()
    amb_n = 0
    # validation on Sweden: postings that carry their own nuts2 field, resolved again by the county and gazetteer routes
    val = {"county": [0, 0], "gazetteer": [0, 0]}
    dis = Counter()
    if a.country == "SE":
        saved = dict(learned)
        learned.clear()
        for id_, loc, n2 in items:
            if n2 and norm(n2) in SE_NAMES and loc not in cache:
                code, m = resolve(loc)
                if m in ("county", "gazetteer", "prefix"):
                    key = "county" if m == "county" else "gazetteer"
                    val[key][0] += 1
                    val[key][1] += code == SE_NAMES[norm(n2)]
                    if code != SE_NAMES[norm(n2)]:
                        dis[(loc, SE_NAMES[norm(n2)], code, m)] += 1
            cache.pop(loc, None)
        learned.update(saved)
        cache.clear()
        amb.clear()
        detail.clear()
    Path("data/tagged").mkdir(parents=True, exist_ok=True)
    with open(f"data/tagged/nuts2_{a.label}.jsonl", "w", encoding="utf-8") as f:
        for id_, loc, n2 in items:
            if n2 and norm(n2) in SE_NAMES:
                code, m = SE_NAMES[norm(n2)], "field"
            else:
                if loc not in cache:
                    cache[loc] = resolve(loc)
                code, m = cache[loc]
            meth[m] += 1
            if m in ("gazetteer", "prefix", "nearest") and parts(loc) and parts(loc)[0] in amb:
                amb_n += 1
            if code:
                reg[code] += 1
            elif m == "unmatched":
                miss[loc] += 1
            else:
                vag[loc] += 1
            f.write(json.dumps({"id": id_, "nuts2": code, "method": m}) + "\n")
    n = len(items)
    placed = sum(reg.values())
    md = [f"# NUTS-2 mapping: {a.label}", "",
          f"{n:,} sampled items (duplicates not removed). Placed in a region: {placed:,} ({placed / n:.1%}). "
          f"Vague, dropped from HHI: {meth['vague']:,} ({meth['vague'] / n:.1%}). Unmatched: {meth['unmatched']:,} ({meth['unmatched'] / n:.1%}).", "",
          "| method | postings | share |", "|---|---|---|"]
    md += [f"| {k} | {v:,} | {v / n:.1%} |" for k, v in meth.most_common()]
    if a.country == "SE":
        md += ["", "Validation on postings with their own nuts2 field (the route is applied to their location text and compared):"]
        md += [f"- {k}: {v[1]:,} of {v[0]:,} agree ({v[1] / max(v[0], 1):.1%})" for k, v in val.items()]
    if a.country == "SE" and dis:
        md += ["", "Disagreements in that validation (location, own field, route result, route):"]
        md += [f"- {k[0]}: field {k[1]}, route {k[2]} ({k[3]}), {v} postings" for k, v in dis.most_common(15)]
    md += ["", f"Postings in ambiguous names: {amb_n:,} ({amb_n / n:.1%}). Ambiguous place names (several regions, largest place taken): {len(amb)}. Regions found: {len(reg)} of {len(polys)} in the polygon file.", "",
           "## Postings per region", "", "| NUTS-2 | postings | share of placed |", "|---|---|---|"]
    md += [f"| {k} | {v:,} | {v / max(placed, 1):.1%} |" for k, v in sorted(reg.items(), key=lambda kv: -kv[1])]
    md += ["", "## Largest unmatched locations (add to the manual csv: place,nuts2)", "", "| location | postings |", "|---|---|"]
    md += [f"| {k} | {v:,} |" for k, v in miss.most_common(25)]
    md += ["", "## Largest vague locations", "", "| location | postings |", "|---|---|"]
    md += [f"| {k} | {v:,} |" for k, v in vag.most_common(8)]
    if amb:
        pc = Counter()
        for id_, loc, n2 in items:
            pp = parts(loc)
            if pp and pp[0] in amb:
                pc[pp[0]] += 1
        md += ["", "## Ambiguous names with most postings (chosen region with population, then the next candidates)", "",
               "| place | postings | chosen (population) | other candidates (population) |", "|---|---|---|---|"]
        for k, v in pc.most_common(40):
            d = detail.get(k)
            if d:
                md.append(f"| {k} | {v:,} | {d[0]} ({d[1]:,}) | " + ", ".join(f"{c} ({p:,})" for c, p in d[2]) + " |")
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/nuts2_{a.label}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
