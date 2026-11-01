"""
Month 3, step 10: which ESCO skills characterise each deglobalization channel?

Uses the skills extracted locally with one threshold for every month (script 69; never the Tracker's skills) and the
channel tags of the model (tags file; intensity ignored). For each channel c and each skill k:

    share_in_channel(k) = weighted share of the postings tagged c that carry k
    share_in_all(k)     = weighted share of ALL postings that carry k
    lift(k)             = share_in_channel / share_in_all   (3.0 = three times as common in the channel)

Weights are the day weights of the corpus (duplicates removed, all files read as one corpus), as in scripts 64 to 66.
A skill is listed only if at least --min-n postings TAGGED c and carrying k were taken (default 5), because lifts
from a handful of postings are noise. The report also gives, per channel, how many postings were tagged (taken and
weighted). Intervals: bootstrap over postings inside each day, as in script 64, for the listed skills' lift.

Optional --split DATE (e.g. 2026-04-22) adds, per channel, how the skill shares of the channel's postings differ
before and after that date (ratio after/before, only for skills with at least --min-n taken in each period). With
the small number of tagged postings per channel this is descriptive: read it as a lead, not a test.

Labels: ESCO URIs are shown with their English preferred label, fetched from the public ESCO web service
(--esco-api, needs internet; only the listed skills are looked up, about 150, and cached in --labels-cache). Without
it, a URI takes the label the Tracker gave the same URI in the corpus, then the first words of the description in
--esco-csv (the package's skills.csv), then the URI tail. Labels are only for reading: no Tracker skill enters a number.

Two tables per channel. "Most common" ranks skills by their share among the channel's postings (generic skills such as
communication appear here). "Most specific" ranks by lift; a lift cannot exceed 1 / (channel's share of all postings), and
a skill that occurs only in the channel's postings reaches that ceiling, so the top of this table is a plateau, not a
ranking. "Specific" = share of all postings carrying the skill that are tagged with the channel.

Run (project root):
    python -m diagnostics.70_skills_per_channel \\
        --corpus <the four corpus files> \\
        --skills data/tagged/skills_local_t0.60.jsonl \\
        --tags data/tagged/tags_qwen2.5_7b_tagging_v8.jsonl [--split 2026-04-22] --esco-api
Writes docs/skills_per_channel.md and data/tagged/skills_per_channel.csv.
"""

import argparse
import csv
import json
import tempfile
from collections import defaultdict
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

CHANNELS = ["reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"]


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


def tracker_labels(rows):
    lab = {}
    for r in rows:
        for s in r["item"].get("skills") or []:
            if isinstance(s, dict):
                u = s.get("uri") or s.get("esco_uri") or s.get("id")
                l = s.get("label") or s.get("name") or s.get("preferred_label")
                if u and l and u not in lab:
                    lab[str(u)] = str(l)
    return lab


def approx_label(desc):
    """Readable stand-in for an ESCO label from the package's description column: the lower-case label block
    (preferred label and synonyms run together; cut where its first word comes back) and the start of the definition."""
    w = desc.split()
    i = 0
    while i < len(w) and not w[i][0].isupper():
        i += 1
    head, defn = w[:i], w[i:]
    pref = head
    if len(head) > 3:
        pref = head[:5]
        for j in range(2, min(len(head), 9)):
            if head[j] == head[0]:
                pref = head[:j]
                break
    text = " ".join(defn[:12]) + ("..." if len(defn) > 12 else "")
    return (" ".join(pref) + " - " + text).strip(" -")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--skills", required=True)
    ap.add_argument("--tags", required=True)
    ap.add_argument("--min-n", type=int, default=5)
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--split", default=None)
    ap.add_argument("--esco-csv", default=None)
    ap.add_argument("--esco-api", action="store_true", help="look up English preferred labels at ec.europa.eu/esco")
    ap.add_argument("--labels-cache", default="data/tagged/esco_labels.json")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--out-md", default="docs/skills_per_channel.md")
    ap.add_argument("--out-csv", default="data/tagged/skills_per_channel.csv")
    args = ap.parse_args()

    rows, dup = load_all(args.corpus)
    labels = tracker_labels(rows)
    if not labels:
        ex = next((x for r in rows for x in (r["item"].get("skills") or [])[:1]), None)
        print("No Tracker labels found; a Tracker skill object looks like:", str(ex)[:200])
    csvp = args.esco_csv
    if not csvp:                                  # the extractor package ships the ESCO skills with their descriptions
        try:
            import esco_skill_extractor
            c = Path(esco_skill_extractor.__file__).parent / "data" / "skills.csv"
            csvp = str(c) if c.exists() else None
        except Exception:
            csvp = None
    if csvp:
        for r in csv.DictReader(open(csvp, encoding="utf-8")):
            labels.setdefault(r["id"], approx_label(r["description"]))
    sk = {}
    for l in open(args.skills, encoding="utf-8"):
        if l.strip():
            d = json.loads(l)
            sk[d["id"]] = set(d["skills"])
    tag = {}
    for l in open(args.tags, encoding="utf-8"):
        if l.strip():
            d = json.loads(l)
            if d.get("ok") and d.get("channel") in CHANNELS:
                tag[str(d["posting_id"])] = d["channel"]
    recs = [{"w": r["w"], "day": r["day"], "sk": sk[str(r["item"]["id"])], "ch": tag.get(str(r["item"]["id"]))}
            for r in rows if str(r["item"]["id"]) in sk]
    print(f"{len(rows):,} postings; {len(recs):,} with extracted skills; {sum(1 for r in recs if r['ch']):,} tagged with a channel")
    miss = len(rows) - len(recs)

    W = sum(r["w"] for r in recs)
    all_w = defaultdict(float)
    for r in recs:
        for k in r["sk"]:
            all_w[k] += r["w"]

    cache_path = Path(args.labels_cache)
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}

    fails = [0]

    def api_label(k):
        import urllib.error, urllib.parse, urllib.request
        if fails[0] >= 3:
            return None          # the service is unreachable: stop trying
        url = "https://ec.europa.eu/esco/api/resource/skill?language=en&uri=" + urllib.parse.quote(k, safe="")
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                d = json.loads(r.read().decode("utf-8"))
            pl = d.get("preferredLabel")
            return (pl.get("en") if isinstance(pl, dict) else pl) or d.get("title")
        except urllib.error.HTTPError:
            return None          # this URI is not in the service (older ESCO version): use the fallback label
        except Exception as e:
            fails[0] += 1
            print("  label lookup failed:", k.rsplit("/", 1)[-1][:8], type(e).__name__,
                  "(giving up after 3 failures)" if fails[0] >= 3 else "")
            return None

    def label(k):
        if k in cache:
            return cache[k]
        if args.esco_api:
            v = api_label(k)
            if v:
                cache[k] = v
                return v
        return labels.get(k) or k.rsplit("/", 1)[-1][:12]

    rng = np.random.default_rng(args.seed)
    L = ["# Skills per channel (ESCO skills extracted locally, one threshold for all months)", "",
         f"{len(recs):,} postings with extracted skills ({miss:,} corpus postings without; they are left out). Lift = share of the channel's "
         "tagged postings carrying the skill / share of all postings carrying it. 'n' = postings taken that are tagged with the channel and carry the skill. "
         f"Skills with n below {args.min_n} are not listed. Interval: bootstrap over postings inside each day.", ""]
    out = []
    by_day = defaultdict(list)
    for i, r in enumerate(recs):
        by_day[r["day"]].append(i)
    days = sorted(by_day)
    for c in CHANNELS:
        ci = [r for r in recs if r["ch"] == c]
        if not ci:
            continue
        cw = sum(r["w"] for r in ci)
        in_w = defaultdict(float)
        n_k = defaultdict(int)
        for r in ci:
            for k in r["sk"]:
                in_w[k] += r["w"]
                n_k[k] += 1
        cand = [k for k in in_w if n_k[k] >= args.min_n]
        lifts = {k: (in_w[k] / cw) / (all_w[k] / W) for k in cand}
        top = sorted(cand, key=lambda k: -lifts[k])[:args.top]
        # bootstrap: resample postings inside each day
        ch_idx = {id(r): None for r in ci}
        draws = []
        for _ in range(args.boot):
            tw_all = 0.0; tw_c = 0.0
            a = defaultdict(float); b = defaultdict(float)
            for d in days:
                idx = by_day[d]
                pick = rng.integers(0, len(idx), len(idx))
                for j in pick:
                    r = recs[idx[j]]
                    tw_all += r["w"]
                    if r["ch"] == c:
                        tw_c += r["w"]
                    for k in r["sk"]:
                        if k in lifts:
                            a[k] += r["w"]
                            if r["ch"] == c:
                                b[k] += r["w"]
            draws.append({k: ((b[k] / tw_c) / (a[k] / tw_all)) if tw_c and a[k] else np.nan for k in top})
        ceiling = W / cw
        L += [f"## {c}: {len(ci)} postings taken, about {cw:,.0f} in the population ({100*cw/W:.2f}% of all postings)", "",
              f"Most common skills in the channel's postings (lift cannot exceed {ceiling:.1f} for this channel):", "",
              "| Skill | n | Share in channel (%) | Share in all (%) | Lift |", "|---|---:|---:|---:|---:|"]
        common = sorted(cand, key=lambda k: -in_w[k])[:10]
        for k in common:
            L.append(f"| {label(k)} | {n_k[k]} | {100*in_w[k]/cw:.1f} | {100*all_w[k]/W:.1f} | {lifts[k]:.1f} |")
        L += ["", "Most specific skills (by lift; a skill found only in this channel sits at the ceiling):", "",
              "| Skill | n | Share in channel (%) | Share in all (%) | Lift (95% interval) | Specific (%) |", "|---|---:|---:|---:|---|---:|"]
        for k in top:
            v = np.array([d[k] for d in draws], dtype=float)
            lo, hi = np.nanpercentile(v, [2.5, 97.5]) if np.isfinite(v).any() else (np.nan, np.nan)
            spec = 100 * in_w[k] / all_w[k]
            L.append(f"| {label(k)} | {n_k[k]} | {100*in_w[k]/cw:.1f} | {100*all_w[k]/W:.1f} | {lifts[k]:.1f} ({lo:.1f} to {hi:.1f}) | {spec:.0f} |")
            out.append([c, k, label(k), n_k[k], round(in_w[k]/cw, 5), round(all_w[k]/W, 5), round(lifts[k], 3), round(spec, 1)])
        if args.split:
            pre = [r for r in ci if r["day"] < args.split]
            post = [r for r in ci if r["day"] >= args.split]
            wp, wq = sum(r["w"] for r in pre), sum(r["w"] for r in post)
            L += ["", f"Before / after {args.split}: {len(pre)} / {len(post)} tagged postings taken."]
            if pre and post:
                sp, sq, npre, npost = defaultdict(float), defaultdict(float), defaultdict(int), defaultdict(int)
                for r in pre:
                    for k in r["sk"]:
                        sp[k] += r["w"]; npre[k] += 1
                for r in post:
                    for k in r["sk"]:
                        sq[k] += r["w"]; npost[k] += 1
                ok = [k for k in sq if npre[k] >= args.min_n and npost[k] >= args.min_n]
                rat = sorted(ok, key=lambda k: -((sq[k] / wq) / (sp[k] / wp)))
                L += ["", "| Skill | n before | n after | Share before (%) | Share after (%) | After / before |", "|---|---:|---:|---:|---:|---:|"]
                for k in rat[:8] + rat[-4:] if len(rat) > 12 else rat:
                    L.append(f"| {label(k)} | {npre[k]} | {npost[k]} | {100*sp[k]/wp:.1f} | {100*sq[k]/wq:.1f} | {(sq[k]/wq)/(sp[k]/wp):.2f} |")
                if not rat:
                    L.append("No skill reaches the minimum in both periods.")
        L.append("")
    if cache:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")
    Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_md).write_text("\n".join(L), encoding="utf-8")
    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["channel", "skill_uri", "label", "n_taken", "share_in_channel", "share_in_all", "lift", "specific_pct"])
        wr.writerows(out)
    print(f"Wrote {args.out_md} and {args.out_csv}")


if __name__ == "__main__":
    main()
