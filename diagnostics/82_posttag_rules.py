"""
Month 3, step 8b: three deterministic corrections applied AFTER the model has tagged (no model call, no Colab).

Why. The 7B tagger does not reliably follow three written rules, so they are enforced here on the saved answers.
Every change is logged with the rule name; the model's own answer is kept in the output (channel_model,
intensity_model, subtype_model), so the effect of each rule can be switched off and counted.

Rules (in this order)
  R1 supply-side   a diversification tag with subtype supply-side (or no subtype, unless sovereign-sector wording shows) is kept only if the evidence or the posting text
                   contains explicit diversification wording (dual or multiple sourcing, alternative suppliers,
                   reduce dependence on, single source, nearshoring, free trade agreement, new export markets).
                   Ordinary purchasing, supplier management and vendor selection become none.
  R2 secnumcloud   a posting whose lexicon terms include secnumcloud or eucs and whose model channel is none or
                   trade compliance becomes diversification, subtype sovereign-tech. Intensity: high when the
                   sentence that names the standard (posting text, else evidence) holds a duty verb (ensure, guarantee, prepare,
                   obtain, audit, maintain, align...), i.e. the work is keeping the company or a service in line with the
                   standard, and is not a 'plus', 'knowledge' or 'experience' requirement (user, 2026-11-07); otherwise low.
  R3 tech list     a sovereign-tech tag whose evidence is a list of tools or platforms (no verb of work, four or
                   more comma-separated items) and whose lexicon terms are only provider names becomes none.

Also: an invalid answer whose raw text names sovereign-cloud in the channel field is read as diversification
sovereign-tech (the parser in 58 does this from the next run on).

Run (project root, venv active), one command per tags file:
    python -m diagnostics.82_posttag_rules --tags data/tagged/tags_v12_lesjeudis.com_2024-08_2025-04.jsonl \
        --corpus data/raw/corpus_lesjeudis.com_2024-08_2025-04.jsonl
Writes <tags>.post.jsonl next to the input and docs/posttag_rules_<name>.csv (one line per changed posting).
Without --corpus the rules use the evidence only (R1 is then stricter). --texts takes a jsonl with posting_id and text.
"""
import argparse, csv, json, re
from collections import Counter
from pathlib import Path

SOVEREIGN_RX = re.compile(r"sovereign|secnumcloud|\beucs\b|gaia-x|ai factor|gigafactor|eurohpc|european cloud|cloud de confiance", re.I)
SUPPLY_RX = re.compile(
    r"dual[- ]?sourc|multi[- ]?sourc|multiple (sources|suppliers)|second[- ]source|alternative (supplier|sourc|source)s?|"
    r"diversif\w*\s+(the\s+|our\s+)?(supplier|supply|sourcing|source)|"
    r"(reduc\w+|less|lower|decreas\w+|minimi[sz]\w+)\s+(our\s+|the\s+)?(dependen\w+|reliance)|dependen\w+ on (a )?(single|one|china|chinese)|"
    r"single[- ]source|sole[- ]source|nearshor\w+|near-shor\w+|friend-?shor\w+|reshor\w+|free trade agreement|new export markets?|"
    r"source (from|outside) (china|asia)|supply chain resilien", re.I)
SEC_RX = re.compile(r"secnumcloud|eucs", re.I)
SEC_DUTY_RX = re.compile(r"qualif\w+|certif\w+|audit\w*|compliance|conformit\w+|homologat\w+|alignment|guarantee|ensure|accredit\w+", re.I)
WORK_RX = re.compile(r"\b(build|design|develop|operate|run|responsible|join|our|we|you|will|work|lead|manage|ensure|support|is|are|has|have|offers?|provides?)\b", re.I)
DUTY_RX = re.compile(r"\b(ensur\w*|guarantee\w*|prepar\w*|obtain\w*|audit\w*|maintain\w*|carry\w* out|conduct\w*|lead\w*|manag\w*|align\w*|implement\w*|follow\w*|monitor\w*|validat\w*|driv\w*)\b", re.I)
LISTY_RX = re.compile(r"\b(plus|appreciated|asset|knowledge|familiar\w*|prerequisite|nice to have|already offers|experience (of|in|with|as)|first experience|have experience|years of experience)\b", re.I)
PROVIDERS = {"s3ns", "outscale", "ovhcloud", "scaleway", "bleu", "numspot", "stackit", "cloud temple", "delos cloud",
             "gaia-x", "cloud de confiance", "eurostack", "aleph alpha", "secnumcloud", "eucs"}


def load_texts(a):
    texts = {}
    if a.texts:
        for l in open(a.texts, encoding="utf-8"):
            if l.strip():
                j = json.loads(l); texts[str(j["posting_id"])] = j["text"]
    for p in a.corpus or []:
        try:
            from diagnostics.corpus_io import load_corpus, posting_text
        except ImportError:
            from corpus_io import load_corpus, posting_text
        rows, _ = load_corpus(p)
        for r in rows:
            texts[str(r["item"].get("id") or r["item"].get("posting_id") or r["item"].get("job_id"))] = posting_text(r["item"], 6000)
    return texts


def is_tech_list(ev):
    ev = (ev or "").strip()
    items = [x for x in re.split(r"[,:;]", ev) if x.strip()]
    return len(ev) <= 200 and ev.count(",") >= 3 and not WORK_RX.search(ev) and all(len(x.split()) <= 4 for x in items)


def sec_sentence(text):
    """The sentence (or bullet) of the posting text that holds the first SecNumCloud or EUCS mention."""
    m = SEC_RX.search(text or "")
    if not m:
        return ""
    a = max([text.rfind(c, 0, m.start()) for c in ".;•\n"] + [-1]) + 1
    ends = [i for i in (text.find(c, m.end()) for c in ".;•\n") if i >= 0]
    return text[a:(min(ends) if ends else len(text))][:400]


EMPLOYER_RX = re.compile(r"\bwe offer\b|\bour own\b|already offers|reflected in|brand of|\bis an? (sovereign|leading|trusted)\b", re.I)


def sec_span(text):
    """The comma-separated span around the first SecNumCloud or EUCS mention: from the last '(' or sentence break before it
    to the next ')' or sentence break after it."""
    m = SEC_RX.search(text or "")
    if not m:
        return ""
    a = max([text.rfind(c, 0, m.start()) for c in "(.;•\n"] + [-1]) + 1
    ends = [i for i in (text.find(c, m.end()) for c in ").;•\n") if i >= 0]
    return text[a:(min(ends) if ends else len(text))]


def in_long_list(text):
    """True when the standard is one of three or more items (two commas, or a comma and 'or'/'and', in its span)."""
    span = sec_span(text)
    return len(re.findall(r",|\bor\b|\band\b|/", span)) >= 2


def sec_intensity(ev, text, model_intensity):
    """high: the sentence naming SecNumCloud or EUCS holds a duty verb (keeping the company or a service in line with the
    standard) and the standard is one of at most two items; a company paragraph keeps the model's intensity; otherwise low."""
    sent = sec_sentence(text) or (ev if SEC_RX.search(ev or "") else "")
    if not sent:
        return "low"
    if EMPLOYER_RX.search(sent):
        return model_intensity if model_intensity in ("low", "medium", "high") else "low"
    if DUTY_RX.search(sent) and not LISTY_RX.search(sent) and not in_long_list(text if text else ev):
        return "high"
    return "low"


def apply(rec, text):
    """returns (rule, new_channel, new_intensity, new_subtype) or None"""
    ch, it, ev = rec.get("channel"), rec.get("intensity"), rec.get("evidence") or ""
    terms = {t.lower() for t in rec.get("terms", [])}
    if not rec.get("ok"):
        m = re.search(r'"channel"\s*:\s*"sovereign[- ]cloud"\s*,\s*"intensity"\s*:\s*"(low|medium|high)"', rec.get("raw", ""))
        if m:
            return ("R0 sovereign-cloud channel field", "diversification", m.group(1), "sovereign-tech")
        return None
    if ch == "diversification" and rec.get("subtype") in ("supply-side", "", None):
        hay = ev + " " + (text or "")
        # a tag without subtype is checked as supply-side unless the posting shows sovereign-sector wording
        if (rec.get("subtype") == "supply-side" or not SOVEREIGN_RX.search(hay)) and not SUPPLY_RX.search(hay):
            return ("R1 supply-side without diversification wording", "none", "none", "")
    if ch in ("none", "trade compliance") and terms & {"secnumcloud", "eucs"}:
        return ("R2 secnumcloud/eucs in a role", "diversification", sec_intensity(ev, text, it), "sovereign-tech")
    if ch == "diversification" and rec.get("subtype") == "sovereign-tech" and is_tech_list(ev) and terms and terms <= PROVIDERS:
        return ("R3 provider named in a tool list", "none", "none", "")
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tags", nargs="+", required=True)
    ap.add_argument("--corpus", nargs="*")
    ap.add_argument("--texts")
    a = ap.parse_args()
    texts = load_texts(a)
    for tf in a.tags:
        out_rows, log, n = [], [], Counter()
        for l in open(tf, encoding="utf-8"):
            if not l.strip():
                continue
            rec = json.loads(l)
            res = apply(rec, texts.get(str(rec["posting_id"])))
            if res:
                rule, ch, it, st = res
                rec.update({"channel_model": rec.get("channel"), "intensity_model": rec.get("intensity"),
                            "subtype_model": rec.get("subtype", ""), "post_rule": rule, "ok": True,
                            "channel": ch, "intensity": it, "subtype": st})
                n[rule] += 1
                sent = sec_sentence(texts.get(str(rec["posting_id"]))) if rule.startswith("R2") else ""
                log.append([rec["posting_id"], rule, rec["channel_model"], rec["intensity_model"], ch, it, (rec.get("evidence") or "")[:120], sent[:300]])
            out_rows.append(rec)
        p = Path(tf)
        outp = p.with_suffix(".post.jsonl")
        with open(outp, "w", encoding="utf-8") as f:
            for r in out_rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        Path("docs").mkdir(exist_ok=True)
        lp = Path("docs") / f"posttag_rules_{p.stem}.csv"
        with open(lp, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["posting_id", "rule", "channel_before", "intensity_before", "channel_after", "intensity_after", "evidence", "secnumcloud_sentence"]); w.writerows(log)
        print(f"{p.name}: {len(out_rows)} postings, changed {sum(n.values())}: {dict(n)} -> {outp.name}, {lp}")


if __name__ == "__main__":
    main()
