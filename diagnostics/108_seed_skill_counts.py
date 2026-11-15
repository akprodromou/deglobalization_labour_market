"""
Month 4, feasibility check for a skill-seeded variant (idea adapted from Dawson, Williams and Rizoiu 2021, PLOS ONE, "AI adoption indicator"):
for each named occupation, which ESCO skills and Lightcast terms could serve as seeds, and how many postings carry them on each board?
Nothing is clustered here. The script only counts, per board and per seed group:
  * postings carrying at least one seed (and at least two different seeds, the stricter reading), as a share of the board
  * postings per quarter (raw counts of collected postings, not weighted) and the number of distinct seeds seen
  * per seed: postings
  * co-occurring skills: the ESCO skills most over-represented among the postings that carry a seed (lift = share among carriers / share on the board,
    at least 5 carriers), which is the "which other skills belong to this occupation" step of the paper
A seed marks a TOPIC (for example export controls), not necessarily a ROLE: a sales manager can carry the skill too. Read the counts as an upper
bound on the postings that could belong to the occupation.

Seeds are ESCO skill URIs taken from lexicon/skills.csv (grep of customs, export, import, sanction, battery, semiconductor, wafer, supply chain)
and Lightcast terms from the pruned block. Occupations without a specific ESCO skill (reshoring program manager) are listed with no seed.

Needs on the Mac: data/tagged/skills_local_full_<board>_t0.60.jsonl, data/tagged/lightcast_block_<board>.jsonl, lexicon/skills.csv (labels, optional)
Output: docs/seed_skill_counts.md and data/cluster/seed_skill_counts.csv
Run:  python -m diagnostics.108_seed_skill_counts
Test: python -m diagnostics.108_seed_skill_counts --mock
"""

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ESCO = {
    "trade compliance officer": {
        "35421ebd-dc4c-4827-adbb-faf4a98c1968": "ensure cargo complies with customs regulations",
        "42ab725f-e57f-4320-a9fd-ac3d6717963d": "ensure customs compliance",
        "666e7d29-247b-4032-a3ce-8ee27554a044": "customs law",
        "bfe7009d-4f93-4803-8b7d-9ee51b4860e6": "keep up to date with customs regulations",
        "00ff06cc-103f-4c85-b5df-6f75acff6abf": "advise on customs regulations",
        "c4118654-695f-44bc-b9d3-1b26f3a955f8": "international import export regulations",
        "7c02513e-c23b-4686-8bdd-1ad99de5a8eb": "manage import export licenses",
        "0959a14b-9743-4d71-93ba-a1fefa56e5ae": "import-export commercial documentation",
    },
    "export control specialist": {
        "66dd1398-6be6-4a0d-a0d0-4a8b3941963a": "export control principles",
        "cbf01241-d126-402a-af28-2eb81e2e24e8": "export regulations of dual-use goods",
        "84e953cf-6e59-4bae-8e4d-7582baaedd8d": "comply with export regulations in different countries",
        "b3a6dda3-e084-40e4-b211-7abb76a07eb6": "advise clients on export restrictions",
        "04cda8e8-e06b-4c91-bbb5-27414dc1cf14": "embargo regulations",
    },
    "semiconductor process engineer": {
        "8a4f920e-f068-4118-a730-9426580f68be": "clean wafers",
        "e78473ee-d208-4b9c-b241-339334ac9a7b": "polish wafers",
        "d8556036-dc03-412b-be42-c4d0a24e4c2c": "load electronic circuits onto wafers",
        "2399952b-9991-4c7c-83c7-ea984fa78830": "imprint circuit design onto wafers (photolithography)",
        "6c8e99ae-f429-4b6f-b243-6b404fa5f49b": "slice crystals into wafers",
        "9f0d30b2-cf59-4819-b3a6-29b1c031c313": "produce semiconductor crystals",
        "d2adf974-7868-4ede-bc48-9f88824ab250": "test semiconductors",
        "0d6ad185-dc2c-46e7-b7f7-a01681c9fddb": "inspect semiconductor components",
    },
    "battery cell technician": {
        "f820e9db-fdb1-4237-9c6b-6f912ca884e2": "battery formation, conditioning, cell preparation",
        "84cc8c9d-db57-42ec-8948-9b632bf06124": "battery chemistry",
        "8cf03262-b6b0-4fe8-9d66-91063bb32db3": "battery components",
        "42f92768-cc76-488d-a721-e90c59ccaade": "assemble batteries",
        "7c8a86b2-b0ae-4969-901a-5949d9974755": "operate battery test equipment",
        "78fc4e90-a522-480a-a2f0-21ff3dfe6ba7": "repair battery components",
        "1cdd0afe-196f-4d8a-924f-4d7473cce3c7": "battery management systems",
        "ad329eb4-463d-40ac-bf03-60e00538bb49": "battery testers",
    },
    "supply chain resilience analyst (generic supply chain skills only)": {
        "96d549bb-3e62-4c45-92a7-f114df089581": "analyse supply chain strategies",
        "b7e57889-a84f-440c-9e60-459aa69979e9": "analyse supply chain trends",
        "92e4064a-a93c-4e22-a63b-8da91757b90c": "detect bottlenecks in the supply chain",
        "cf579543-272b-43c8-b942-555836ae4241": "supply chain principles",
        "f929c89e-c363-4132-a918-e021d57b307c": "supply chain management",
    },
    "critical materials specialist (weak: no critical-raw-materials skill)": {
        "e13dc8bb-c81f-4bd1-aff6-f5f81f6195e2": "implement mineral processes",
        "614fdb7f-637f-4501-a80a-53c14a9804e5": "materials engineering (battery material)",
    },
    "reshoring program manager (no ESCO skill)": {},
}

LIGHTCAST = {
    "trade compliance officer": ["Certified Customs Specialist"],
    "semiconductor process engineer": ["Semiconductor Manufacturing Process", "Wafer Fabrication", "Lithography", "Photolithography", "Dry Etching",
                                       "Plasma Etching", "Thin Film Coating", "Metallization", "Wafer Testing", "Wafer Bonding", "Wafer Dicing",
                                       "Semiconductor Device Fabrication", "Semiconductor Fabrication Plant", "Semiconductor Package"],
    "battery cell technician": ["Battery Production Process", "Battery Formation", "Battery Production Equipment", "Battery Recycling Processes",
                                "Battery Industry", "Battery Inspection", "Battery Life Cycle Management", "Battery Maintenance", "Battery Disassembly",
                                "Battery Cycler", "Battery Diagnostics", "Battery Charge/Discharge", "Battery Conditioning"],
}


def load_jsonl(p):
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def quarter(day):
    return f"{day[:4]}-Q{(int(day[5:7]) - 1) // 3 + 1}"


def mock_board(seed):
    import random
    random.seed(seed)
    sk, lc = [], []
    pool = [f"http://data.europa.eu/esco/skill/s{i}" for i in range(60)]
    seeds = [f"http://data.europa.eu/esco/skill/{u}" for u in list(ESCO["export control specialist"]) + list(ESCO["battery cell technician"])]
    for i in range(3000):
        s = random.sample(pool, 5)
        if random.random() < 0.03:
            s += random.sample(seeds, random.choice([1, 2]))
        sk.append({"id": str(i), "day": f"2025-{random.randint(1, 9):02d}-10", "skills": s})
        lc.append({"id": str(i), "terms": ["Battery Formation"] if random.random() < 0.01 else []})
    return sk, lc


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--boards", nargs="+", default=["jobbland", "lesjeudis", "jobsde"])
    ap.add_argument("--tagged", default="data/tagged")
    ap.add_argument("--esco-csv", default="lexicon/skills.csv")
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--out", default="data/cluster")
    ap.add_argument("--top", type=int, default=12, help="co-occurring skills listed per group")
    ap.add_argument("--min-carriers", type=int, default=5)
    ap.add_argument("--show-titles", type=int, default=0, help="list the titles of up to N carriers per group (groups with at most 150 carriers), to see whether they hold the occupation or only mention the topic")
    ap.add_argument("--titles-jobbland", default="titles_jobbland_inf.jsonl", help="file name in --tagged used for jobbland (inferred titles); other boards use titles_<board>.jsonl")
    ap.add_argument("--mock", action="store_true")
    args = ap.parse_args()

    label = {}
    if Path(args.esco_csv).exists():
        with open(args.esco_csv, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                label[r["id"].rsplit("/", 1)[-1]] = r.get("description", "")[:45]

    rows, md = [], ["# Seed skills for the named occupations: how many postings carry them", "",
                    "Counts of collected postings (not weighted). A seed marks a topic, not necessarily a role, so these are upper bounds on postings that could belong to the occupation. "
                    "ESCO seeds are skills extracted from the full text (script 69b, threshold 0.6); Lightcast seeds are terms of the pruned block (script 91).", ""]
    for bi, board in enumerate(args.boards):
        if args.mock:
            sk, lc = mock_board(bi)
        else:
            sp, lp = Path(args.tagged) / f"skills_local_full_{board}_t0.60.jsonl", Path(args.tagged) / f"lightcast_block_{board}.jsonl"
            if not sp.exists():
                print(f"skip {board}: missing {sp}")
                continue
            sk = load_jsonl(sp)
            lc = load_jsonl(lp) if lp.exists() else []
        lcmap = {r["id"]: set(r.get("terms", [])) for r in lc}
        title_by_id = {}
        if args.show_titles and not args.mock:
            tp = Path(args.tagged) / (args.titles_jobbland if board == "jobbland" else f"titles_{board}.jsonl")
            if tp.exists():
                for r in load_jsonl(tp):
                    t = (r.get("title_clean") or "").strip() if r.get("has_title") else ""
                    title_by_id[r["id"]] = t or ("(no title) " + (r.get("desc_start") or "")[:60])
            else:
                print(f"no titles file {tp}")
        N = len(sk)
        sets = [set(u.rsplit("/", 1)[-1] for u in r["skills"]) for r in sk]
        days = [r.get("day", "") for r in sk]
        df = Counter(s for st in sets for s in st)
        md += [f"## {board}: {N:,} postings", "", "| occupation | seed skills | postings with any seed | share | with 2+ different seeds | Lightcast seed terms: postings | any ESCO or Lightcast |",
               "|---|---|---|---|---|---|---|"]
        details = []
        for occ, seeds in ESCO.items():
            ids = set(seeds)
            lt = set(LIGHTCAST.get(occ.split(" (")[0], []))
            hit_e = [len(st & ids) for st in sets]
            hit_l = [len(lcmap.get(r["id"], set()) & lt) for r in sk]
            any_e = sum(1 for h in hit_e if h >= 1)
            two_e = sum(1 for h in hit_e if h >= 2)
            any_l = sum(1 for h in hit_l if h >= 1)
            any_el = sum(1 for a, b in zip(hit_e, hit_l) if a >= 1 or b >= 1)
            md.append(f"| {occ} | {len(ids)} | {any_e} | {any_e / N:.2%} | {two_e} | {any_l} | {any_el} ({any_el / N:.2%}) |")
            rows.append({"board": board, "occupation": occ, "seeds": len(ids), "any_esco": any_e, "share_esco": any_e / N, "two_plus_esco": two_e,
                         "lightcast": any_l, "any": any_el})
            if not ids:
                continue
            carriers = [i for i, h in enumerate(hit_e) if h >= 1]
            perseed = Counter(s for i in carriers for s in sets[i] & ids)
            byq = Counter(quarter(days[i]) for i in carriers if days[i])
            nq = Counter(quarter(d) for d in days if d)
            co = Counter(s for i in carriers for s in sets[i] - ids)
            lift = sorted(((c / len(carriers)) / (df[s] / N), c, s) for s, c in co.items() if c >= args.min_carriers)
            both = [i for i in range(N) if hit_e[i] >= 1 or hit_l[i] >= 1]
            tl = []
            if args.show_titles and len(both) <= 150:
                for i in both[: args.show_titles]:
                    why = [seeds[s] for s in sets[i] & ids] + sorted(lcmap.get(sk[i]["id"], set()) & lt)
                    tl.append(f"{days[i]} | {title_by_id.get(sk[i]['id'], '(titles file missing)')[:70]} | {'; '.join(why)[:90]}")
            details.append((occ, seeds, perseed, byq, nq, list(reversed(lift))[: args.top], len(carriers), tl))
        md.append("")
        for occ, seeds, perseed, byq, nq, lift, nc, tl in details:
            if nc == 0:
                md += [f"### {board}: {occ}", "", "No posting carries a seed.", ""]
                continue
            md += [f"### {board}: {occ} ({nc} carriers)", "", "Seeds found: " + "; ".join(f"{seeds[s]} ({n})" for s, n in perseed.most_common()), "",
                   "Postings per quarter (carriers / all collected): " + ", ".join(f"{q} {byq.get(q, 0)}/{nq[q]}" for q in sorted(nq)), ""]
            if lift:
                md += ["Skills most over-represented among the carriers (lift = share among carriers / share on the board):", "",
                       "| skill | carriers with it | lift |", "|---|---|---|"]
                md += [f"| {label.get(s, s)} | {c} | {l:.1f} |" for l, c, s in lift]
                md.append("")
            if tl:
                md += [f"Titles of the carriers (date | cleaned title | seeds matched):", ""] + [f"- {x}" for x in tl] + [""]
    md += ["Reading notes", "",
           "- Seeds that carry only a handful of postings per board cannot support a series; a group with 100+ carriers can.",
           "- A high lift for skills of an unrelated field means the seed skill is a false match or generic; a coherent list (for example customs, licences, documents) supports the seed.",
           "- Carriers of ESCO seeds depend on the extractor (false matches exist, see the D v2 reports); carriers of Lightcast seeds are literal phrase hits and more reliable but fewer."]
    Path(args.docs).mkdir(parents=True, exist_ok=True)
    Path(args.out).mkdir(parents=True, exist_ok=True)
    Path(f"{args.docs}/seed_skill_counts.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    if rows:
        with open(f"{args.out}/seed_skill_counts.csv", "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            wr.writeheader()
            wr.writerows(rows)
    print(f"wrote {args.docs}/seed_skill_counts.md")


if __name__ == "__main__":
    main()
