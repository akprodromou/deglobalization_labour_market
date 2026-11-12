"""
Month 4: how concentrated is a cluster on a few employers?

A cluster that is mostly one employer's postings (Thales, Sopra Steria/CS, Safran ...) measures that employer's posting
campaign or job-title jargon (for example "IVVQ" at Thales), not an occupation of the market. For each cluster you name,
this script counts postings, distinct employers and the largest employers, overall and per quarter.

Employer key (--employer-from). `named` (default) looks for known employer names (Thales, Sopra Steria/CS, Safran, Alten ...)
in the first 1,500 characters of the description; postings without a recognised name count as unmatched, and the report lists
frequent capitalised words in them so the list can be extended. `organization` uses the corpus field of that name (empty on
lesjeudis.com and jobbland.se). `text` uses the first 80 characters of the description.

Two keys are shown. `full` is the normalised employer name. `group` is its first word, which merges variants of one group
("Thales AVS France", "Thales LAS France" -> "thales"); it can also merge unrelated names that start with the same word,
so read the example names in the table.

Options
    --clusters 68 139 ...       clusters of script 92 (labels_<board>_<input>.jsonl)
    --tags / --min-intensity    restrict to flagged postings (medium = tags with duties in or supporting the sector)
    --flagged-only              only flagged postings are counted (needs --tags)
    --employer-from organization|text
    --top 5                     largest employers listed per cluster

Run (project root, venv active), lesjeudis:
    python -m diagnostics.103_cluster_employers --board lesjeudis --input A --clusters 68 139 67 130 127 56 61 99 133 33 107 --corpus data/raw/corpus_lesjeudis.com_2024-08_2025-04.jsonl data/raw/corpus_lesjeudis.com_2025-05_2025-09.jsonl --tags data/tagged/tags_v12_lesjeudis.com_2024-08_2025-04.r71.post.jsonl data/tagged/tags_v12_lesjeudis.com_2025-05_2025-09.r71.post.jsonl --min-intensity medium --flagged-only

Output: docs/employers_<board>_<input>.md
"""

import argparse
import json
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

CH = ["reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"]
INT_RANK = {"low": 0, "medium": 1, "high": 2}
LEGAL = {"sa", "sas", "sasu", "sarl", "gmbh", "ag", "ab", "aktiebolag", "inc", "ltd", "llc", "se", "group", "groupe", "the", "la", "le", "les", "l"}


NAMED = {
    "thales": r"thales", "sopra steria": r"sopra\s*steria|\bCS\s+(?:group|is an independent)", "safran": r"safran",
    "alten": r"\balten\b", "scalian": r"scalian", "centum": r"centum", "naval group": r"naval\s+group",
    "airbus": r"airbus", "dassault": r"dassault", "mbda": r"\bmbda\b", "knds": r"\bknds\b|nexter", "arianegroup": r"arianegroup|ariane\s+group",
    "edf": r"\bedf\b", "capgemini": r"capgemini", "atos/eviden": r"\batos\b|eviden", "orange": r"\borange\b", "akkodis": r"akkodis|\baltran\b",
    "expleo": r"expleo", "assystem": r"assystem", "segula": r"segula", "ausy/randstad": r"\bausy\b|randstad", "sogeti": r"sogeti", "cgi": r"\bcgi\b",
    "accenture": r"accenture", "onepoint": r"onepoint", "bertrandt": r"bertrandt", "aubay": r"aubay", "extia": r"\bextia\b", "sii": r"\bsii\b",
    "davidson": r"davidson", "hays": r"\bhays\b", "michael page": r"michael\s+page", "scaleway": r"scaleway", "ovhcloud": r"\bovh", "stellantis": r"stellantis",
    "renault": r"renault", "michelin": r"michelin", "naval": r"\bdcns\b", "cea": r"\bcea\b", "inria": r"\binria\b", "onera": r"\bonera\b", "cnes": r"\bcnes\b",
    "dgse/drsd/defence ministry": r"minist[eè]re des arm[eé]es|armed forces|\bdrsd\b|\bdga\b",
}
NAMED_RX = {k: re.compile(v, re.I if k != "sopra steria" else 0) for k, v in NAMED.items()}
NAMED_RX["sopra steria"] = re.compile(r"sopra\s*steria|\bCS\s+(?:GROUP|Group|is an independent)", re.I)
CAP_STOP = {"the", "you", "your", "our", "join", "work", "place", "france", "company", "description", "who", "are", "about", "we", "with", "for", "and", "this", "that", "will",
            "position", "mission", "missions", "location", "within", "paris", "toulouse", "bordeaux", "lyon", "nantes", "rennes", "grenoble", "lille", "job", "role", "team"}


def named_employer(desc):
    """Earliest known employer name in the first 1,500 characters of the description ('' when none)."""
    text = desc[:1500]
    best, pos = "", 10 ** 9
    for k, rx in NAMED_RX.items():
        m = rx.search(text)
        if m and m.start() < pos:
            best, pos = k, m.start()
    return best


def cap_tokens(desc):
    return {w.lower() for w in re.findall(r"\b[A-Z][A-Za-z0-9&\-]{2,}", desc[:300])} - CAP_STOP


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


def norm(s):
    return re.sub(r"\W+", " ", (s or "").lower()).strip()


def employer_keys(item, mode):
    """(full, group) key of a posting; ('', '') when unknown."""
    if mode == "named":
        n = named_employer(item.get("description") or "")
        return (n, n) if n else ("", "")
    raw = item.get("organization") if mode == "organization" else (item.get("description") or "")[:80]
    full = norm(raw)
    if not full:
        return "", ""
    words = [w for w in full.split() if w not in LEGAL] or full.split()
    return full, words[0]


def quarter(day):
    y, m, _ = day.split("-")
    return f"{y}-Q{(int(m) - 1) // 3 + 1}"


def effective_n(counts):
    tot = sum(counts.values())
    return 1 / sum((c / tot) ** 2 for c in counts.values()) if tot else 0.0


def summarise(rows, cluster_of, mode, keep, top):
    """rows: [{'day','item'}]; cluster_of: id -> cluster; keep: id -> bool. Returns {cluster: dict}."""
    per = defaultdict(list)
    for r in rows:
        i = str(r["item"]["id"])
        c = cluster_of.get(i)
        if c is None or not keep(i):
            continue
        full, grp = employer_keys(r["item"], mode)
        per[c].append((r["day"], full, grp, (r["item"].get("organization") or "").strip(), "" if grp else (r["item"].get("description") or "")))
    out = {}
    for c, lst in per.items():
        known = [x for x in lst if x[2]]
        unk_tok = Counter(t for x in lst if not x[2] for t in cap_tokens(x[4]))
        gcount = Counter(x[2] for x in known)
        fcount = Counter(x[1] for x in known)
        names = defaultdict(Counter)
        for _, _, g, raw, _d in known:
            names[g][raw or g] += 1
        byq = defaultdict(list)
        for d, _, g, _, _d in known:
            byq[quarter(d)].append(g)
        qrows = {}
        for q, gl in sorted(byq.items()):
            qc = Counter(gl)
            top1, n1 = qc.most_common(1)[0]
            qrows[q] = {"n": len(gl), "groups": len(qc), "top": top1, "top_share": n1 / len(gl)}
        out[c] = {
            "n": len(lst), "unknown": len(lst) - len(known), "full": len(fcount), "groups": len(gcount),
            "eff": effective_n(gcount), "eff_full": effective_n(fcount), "top": [(g, n, names[g].most_common(2)) for g, n in gcount.most_common(top)],
            "top1_share": (gcount.most_common(1)[0][1] / len(known)) if known else 0.0,
            "top3_share": (sum(n for _, n in gcount.most_common(3)) / len(known)) if known else 0.0,
            "byq": qrows, "unk_tokens": unk_tok.most_common(12),
        }
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--input", default="A")
    ap.add_argument("--clusters", nargs="+", type=int, required=True)
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--labels")
    ap.add_argument("--tags", nargs="+")
    ap.add_argument("--min-intensity", choices=["low", "medium", "high"], default="low")
    ap.add_argument("--flagged-only", action="store_true")
    ap.add_argument("--employer-from", choices=["organization", "text", "named"], default="named")
    ap.add_argument("--top", type=int, default=5)
    a, _ignored = ap.parse_known_args()
    labels_p = a.labels or f"data/cluster/labels_{a.board}_{a.input}.jsonl"
    if not Path(labels_p).exists():
        raise SystemExit(f"labels file not found: {labels_p}")
    want = set(a.clusters)
    cluster_of = {}
    for l in open(labels_p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            if int(r["cluster"]) in want:
                cluster_of[str(r["id"])] = int(r["cluster"])
    flag = set()
    for p in a.tags or []:
        if not Path(p).exists():
            raise SystemExit(f"tags file not found: {p}")
        for l in open(p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                if r.get("ok") and r.get("channel") in CH and INT_RANK.get(r.get("intensity") or "low", 0) >= INT_RANK[a.min_intensity]:
                    flag.add(str(r["posting_id"]))
    if a.flagged_only and not a.tags:
        raise SystemExit("--flagged-only needs --tags")
    rows, _dup = load_all(a.corpus)
    keep = (lambda i: i in flag) if a.flagged_only else (lambda i: True)
    res = summarise(rows, cluster_of, a.employer_from, keep, a.top)
    md = [f"# Employer concentration of clusters {a.clusters}: {a.board} input {a.input}", "",
          f"Employer key: {dict(organization='organization field', text='first 80 characters of the description', named='known employer names found in the first 1,500 characters of the description')[a.employer_from]}; "
          f"postings counted: {'flagged only (intensity ' + a.min_intensity + ' or higher)' if a.flagged_only else 'all taken postings'}. "
          "Counts are postings taken (not weighted). `group` merges names that share a first word. Effective employers = 1 / sum of squared shares "
          "(1 means one employer, N means N equal employers).", "",
          "| cluster | postings | employer unknown | distinct names | effective names | distinct groups | effective groups | top group share | top 3 share | largest groups (postings; example name) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for c in a.clusters:
        s = res.get(c)
        if not s:
            md.append(f"| {c} | 0 | | | | | | | | |")
            continue
        tops = "; ".join(f"{g} {n} ({nm[0][0]})" for g, n, nm in s["top"])
        md.append(f"| {c} | {s['n']} | {s['unknown']} | {s['full']} | {s['eff_full']:.1f} | {s['groups']} | {s['eff']:.1f} | {s['top1_share']:.0%} | {s['top3_share']:.0%} | {tops} |")
    md += ["", "## Frequent capitalised words in the first 300 characters of postings without a recognised employer (candidates to add to the list)", ""]
    for c in a.clusters:
        s_ = res.get(c)
        if s_ and s_["unk_tokens"]:
            md.append(f"- Cluster {c} ({s_['unknown']} unmatched): " + ", ".join(f"{t} {n}" for t, n in s_["unk_tokens"]))
    md += ["", "## By quarter (does one employer carry the quarter in which the cluster crossed the line?)", ""]
    for c in a.clusters:
        s = res.get(c)
        if not s:
            continue
        md += [f"### Cluster {c}", "", "| quarter | postings | distinct groups | largest group | its share |", "|---|---|---|---|---|"]
        md += [f"| {q} | {v['n']} | {v['groups']} | {v['top']} | {v['top_share']:.0%} |" for q, v in s["byq"].items()]
        md.append("")
    Path("docs").mkdir(exist_ok=True)
    out_p = f"docs/employers_{a.board}_{a.input}.md"
    Path(out_p).write_text("\n".join(md) + "\n", encoding="utf-8")
    print(out_p + " written")


if __name__ == "__main__":
    main()
