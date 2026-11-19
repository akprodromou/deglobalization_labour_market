"""
How many titles of a board are not English? A rough count with marker words and letters (no language-detection package), to state the language mix of the titles.
A title counts as French, German or Swedish when it contains one of that language's marker words or a letter that is typical of it
(French: é è ê à ç ù û ô î œ; German: ü ß; Swedish: å). Letters shared by German and Swedish (ä, ö) are not used. Approximate: titles of
only English-looking words (for example a French job title that is also an English word) count as English, so the shares are lower bounds.

Run (project root, venv active):
    python -m diagnostics.123_title_language --board lesjeudis
Output: docs/title_language_<board>.md (shares, shares by quarter if the titles file has a day, and 15 examples per language)
"""
import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path

FR_W = r"\b(ingénieur|ingenieur|chef|responsable|chargé|chargée|technicien|technicienne|développeur|developpeur|gestionnaire|contrôleur|acheteur|consultante|stagiaire|alternance|défense|sécurité|réseau|système|systèmes|projet|projets|poste|pour|avec|des|les|du|de la|et)\b"
DE_W = r"\b(mitarbeiter|fachkraft|kaufmann|kauffrau|sachbearbeiter|leiter|leitung|verkäufer|ausbildung|techniker|fahrer|entwickler|für|und|mit|m/w/d)\b"
SV_W = r"\b(söker|till|sökes|ledare|chef|för|och|med|ingenjör|säljare|sjuksköterska|undersköterska|butik|arbetsledare)\b"
RX = {
    "French": re.compile(FR_W + r"|[éèêàçùûôîœ]", re.I),
    "German": re.compile(DE_W + r"|[üß]", re.I),
    "Swedish": re.compile(SV_W + r"|å", re.I),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--titles")
    a = ap.parse_args()
    p = a.titles or f"data/tagged/titles_{a.board}.jsonl"
    recs = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    recs = [r for r in recs if r.get("has_title") and (r.get("title_clean") or "").strip()]
    n = len(recs)
    hit = {k: [r for r in recs if rx.search(r["title_clean"])] for k, rx in RX.items()}
    any_hit = {id(r) for v in hit.values() for r in v}
    md = [f"# Language mix of the titles (rough count): {a.board}", "", f"{n:,} postings with a title. A title counts for a language when it contains a marker word or a letter typical of it; "
          "a title can count for more than one. Shares are lower bounds for non-English titles.", "", "| language | titles | share |", "|---|---|---|"]
    md += [f"| {k} | {len(v):,} | {100 * len(v) / n:.1f}% |" for k, v in hit.items()]
    md += [f"| any of the three | {len(any_hit):,} | {100 * len(any_hit) / n:.1f}% |", ""]
    rnd = random.Random(1)
    for k, v in hit.items():
        md += [f"### {k}: 15 examples", ""] + [f"- {r['title_clean'][:100]}" for r in rnd.sample(v, min(15, len(v)))] + [""]
    Path("docs").mkdir(exist_ok=True)
    Path(f"docs/title_language_{a.board}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:11])); print(f"docs/title_language_{a.board}.md written")


if __name__ == "__main__":
    main()
