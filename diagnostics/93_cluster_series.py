"""
Month 4, step 3: quarterly series, emergence, baseline change, channel mix and regional HHI for every cluster.

Reads the clusters of script 92 (labels_<board>_<input>.jsonl), the corpus with day weights, the Month 3 tags and the
NUTS-2 mapping of script 96. A posting stands for (day total / postings taken that day) postings of its day
(duplicates removed, corpus_io.load_corpus). Noise (label -1) is kept as its own row.

Per cluster and quarter (data/cluster/series_<board>_<input>.csv)
    share            weighted share of all postings of the quarter, with two 95% intervals:
                     A = postings redrawn inside each day (independent postings), C = whole ISO weeks redrawn.
                     Report C when judging a change; A is the narrower, optimistic interval (see the sampling check, script 94).
    weighted_sampled share x weighted postings of the sampled days
    weighted_adjusted share x weighted postings x (calendar days / sampled days): an estimate for the whole quarter, valid
                     only if the unsampled days resemble the sampled ones. Edge quarters use the days between the first
                     and last collected day. Quarters with fewer than --min-days sampled days never count as crossings.

Emergence (docs/emergence_<board>_<input>.md)
    A cluster crosses when weighted_adjusted >= --threshold (default 100 postings a quarter) or, in the share version,
    when share >= --share-threshold (default 0.001). First crossing in the board's first usable quarter is "already present",
    not new. Occupation Emergence Rate = clusters newly crossing per quarter, next to the number of active clusters.

Baseline (--event NAME=YYYY-MM-DD): share in the --window-days days before the event day (default 90) against the same
number of days from it on, difference and ratio, with a 95% interval for the difference from resampling ISO weeks inside each
period. --window-days 0 uses the whole board on each side.

Channel mix: weighted share of the cluster's postings carrying a Month 3 flag, and its largest channel.
Template check: share of the cluster's taken postings in its largest group of postings with the same first 80
description characters. A cluster dominated by one group (default above 30%) is not eligible: it describes one
employer's batch, not an occupation.

Regional HHI (data/cluster/hhi_<board>_<input>.csv): sum of squared weighted regional shares over postings placed in a
NUTS-2 region; unplaced postings (vague, outside, unmatched) are left out and their weighted share is reported. Normalised
HHI = (HHI - 1/R) / (1 - 1/R), R = regions of the country (SE 8, FR 22, DE 38 in the NUTS 2021 files). Compare clusters within a
board, not across boards. Rows under --min-placed placed postings are marked unreliable.

Run (project root, venv active), jobbland example:
    python -m diagnostics.93_cluster_series --board jobbland --country SE --input A --event AccelerateEU=2026-04-22 --corpus data/raw/corpus_jobbland.se_2024-01_2024-12.jsonl data/raw/corpus_jobbland.se_2025-01_2025-12.jsonl data/raw/corpus_jobbland.se_2026-01_2026-08.jsonl data/raw/corpus_jobbland.se_2026-09_2026-09.jsonl --tags data/tagged/tags_v12_jobbland.final.post.jsonl
"""

import argparse
import csv
import json
import re
import tempfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

import numpy as np

try:
    from diagnostics.corpus_io import load_corpus
except ImportError:
    from corpus_io import load_corpus

CH = ["reshoring", "defense", "critical materials", "energy security", "trade compliance", "diversification"]
REGIONS = {"SE": 8, "FR": 22, "DE": 38}


INT_RANK = {"low": 0, "medium": 1, "high": 2}

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


PERIOD = ["quarter"]


def quarter(day):
    """Period label of a day: quarter (2025-Q4) or, with --period month, month (2025-12). The name is kept for brevity."""
    y, m, _ = day.split("-")
    if PERIOD[0] == "month":
        return f"{y}-{m}"
    return f"{y}-Q{(int(m) - 1) // 3 + 1}"


def qbounds(q):
    if "-Q" not in q:
        y, m = int(q[:4]), int(q[5:7])
        b = date(y + (m == 12), 1 if m == 12 else m + 1, 1)
        return date(y, m, 1), date.fromordinal(b.toordinal() - 1)
    y, n = int(q[:4]), int(q[-1])
    a = date(y, 3 * n - 2, 1)
    b = date(y + (n == 4), 1 if n == 4 else 3 * n + 1, 1)
    return a, date.fromordinal(b.toordinal() - 1)


def week(day):
    y, w, _ = date.fromisoformat(day).isocalendar()
    return f"{y}-W{w:02d}"


def q95(a, axis=0):
    return np.quantile(a, [0.025, 0.975], axis=axis)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--board", required=True)
    ap.add_argument("--country", required=True, choices=list(REGIONS))
    ap.add_argument("--input", default="A", help="clustering input of script 92: A, D, Dv2 ...")
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--labels")
    ap.add_argument("--tags", nargs="+")
    ap.add_argument("--min-intensity", choices=["low", "medium", "high"], default="low",
                    help="count a posting as flagged only at this intensity or higher (low = every tag, the default; medium = duties in or supporting the sector, company text alone excluded)")
    ap.add_argument("--nuts")
    ap.add_argument("--titles")
    ap.add_argument("--event")
    ap.add_argument("--period", choices=["quarter", "month"], default="quarter")
    ap.add_argument("--from", dest="d_from", default="0000-00-00", help="first day used (YYYY-MM-DD): restrict to one coverage regime")
    ap.add_argument("--to", dest="d_to", default="9999-99-99", help="last day used")
    ap.add_argument("--window-days", type=int, default=90, help="days before and from the event used for the baseline (0 = whole board)")
    ap.add_argument("--threshold", type=float, default=None, help="weighted postings per period; default 100 a quarter, 33.3 a month")
    ap.add_argument("--share-threshold", type=float, default=0.001)
    ap.add_argument("--min-days", type=int, default=None, help="sampled days a period needs to be usable; default 20 a quarter, 12 a month")
    ap.add_argument("--min-placed", type=int, default=50)
    ap.add_argument("--max-template", type=float, default=0.30)
    ap.add_argument("--max-titleless", type=float, default=0.50, help="clusters made mostly of postings without a title are not eligible")
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    PERIOD[0] = a.period
    if a.threshold is None:
        a.threshold = 100 if a.period == "quarter" else 100 / 3
    if a.min_days is None:
        a.min_days = 20 if a.period == "quarter" else 12
    rng = np.random.default_rng(a.seed)
    labels_p = a.labels or f"data/cluster/labels_{a.board}_{a.input}.jsonl"
    nuts_p = a.nuts or f"data/tagged/nuts2_{a.board}.jsonl"
    titles_p = a.titles or f"data/tagged/titles_{a.board}.jsonl"

    rows, dup = load_all(a.corpus)
    rows = [r for r in rows if a.d_from <= r["day"] <= a.d_to]
    lab = {}
    for l in open(labels_p, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            lab[str(r["id"])] = int(r["cluster"])
    flag = {}
    if a.tags:
        for p in a.tags:
            for l in open(p, encoding="utf-8"):
                if l.strip():
                    r = json.loads(l)
                    if r.get("ok") and r.get("channel") in CH and INT_RANK.get(r.get("intensity") or "low", 0) >= INT_RANK[a.min_intensity]:
                        flag[str(r["posting_id"])] = r["channel"]
    reg = {}
    if not Path(nuts_p).exists():
        print(f"NOTE: {nuts_p} not found, so every posting counts as unplaced and HHI stays empty. Run script 96 for this board first.")
    if Path(nuts_p).exists():
        for l in open(nuts_p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                reg[str(r["id"])] = r["nuts2"]
    ttl, notitle = {}, set()
    if Path(titles_p).exists():
        for l in open(titles_p, encoding="utf-8"):
            if l.strip():
                r = json.loads(l)
                ttl[str(r["id"])] = r.get("title_clean") or r.get("title") or ""
                if not r.get("has_title", True):
                    notitle.add(str(r["id"]))

    ids = [str(r["item"]["id"]) for r in rows]
    unl = sum(i not in lab for i in ids)
    cl = np.array([lab.get(i, -2) for i in ids])
    days = sorted({r["day"] for r in rows})
    di = {d: i for i, d in enumerate(days)}
    D = len(days)
    dix = np.array([di[r["day"]] for r in rows])
    w = np.array([r["w"] for r in rows])
    n_d = np.bincount(dix, minlength=D).astype(float)
    W_d = np.bincount(dix, weights=w, minlength=D)
    qs = sorted({quarter(d) for d in days})
    qix_day = np.array([qs.index(quarter(d)) for d in days])
    clusters = sorted(set(cl.tolist()))
    K = len(clusters)
    kmap = {c: i for i, c in enumerate(clusters)}
    kix = np.array([kmap[c] for c in cl])
    C = np.zeros((K, D))
    np.add.at(C, (kix, dix), 1)
    first_day, last_day = date.fromisoformat(days[0]), date.fromisoformat(days[-1])

    # ---- series per cluster and quarter
    series, qinfo = [], {}
    for qi, q in enumerate(qs):
        idx = np.where(qix_day == qi)[0]
        a0, b0 = qbounds(q)
        cal = (min(b0, last_day) - max(a0, first_day)).days + 1
        pop = W_d[idx].sum()
        adj = cal / len(idx)
        full = len(idx) >= a.min_days
        qinfo[q] = {"days": len(idx), "cal": cal, "pop": pop, "adj": adj, "full": full}
        wk = np.array([week(days[i]) for i in idx])
        uw = sorted(set(wk))
        wmask = np.array([wk == u for u in uw])
        Wq, nq = W_d[idx], n_d[idx]
        for k, c in enumerate(clusters):
            cc = C[k, idx]
            p = cc / nq
            num_d = Wq * p
            share = num_d.sum() / pop
            dr = rng.binomial(nq[None, :].astype(int), p[None, :], size=(a.boot, len(idx)))
            sA = (dr * (Wq / nq)).sum(1) / pop
            numw = np.array([num_d[m].sum() for m in wmask])
            denw = np.array([Wq[m].sum() for m in wmask])
            ii = rng.integers(0, len(uw), size=(a.boot, len(uw)))
            sC = numw[ii].sum(1) / denw[ii].sum(1)
            loA, hiA = q95(sA)
            loC, hiC = q95(sC)
            series.append({"cluster": c, "quarter": q, "days": len(idx), "calendar_days": cal, "taken": int(cc.sum()),
                           "share": share, "share_lo_A": loA, "share_hi_A": hiA, "share_lo_C": loC, "share_hi_C": hiC,
                           "weighted_sampled": share * pop, "weighted_adjusted": share * pop * adj,
                           "adjusted_lo_C": loC * pop * adj, "adjusted_hi_C": hiC * pop * adj, "full_quarter": int(full)})
    Path("data/cluster").mkdir(parents=True, exist_ok=True)
    Path("docs").mkdir(exist_ok=True)
    tag = f"{a.board}_{a.input}" + ("" if a.min_intensity == "low" else f"_int{a.min_intensity}") + ("" if a.period == "quarter" else "_month") + ("" if a.d_from == "0000-00-00" and a.d_to == "9999-99-99" else f"_{a.d_from}_{a.d_to}")
    with open(f"data/cluster/series_{tag}.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(series[0].keys()))
        wr.writeheader()
        wr.writerows(series)

    # ---- weekly population (coverage regimes)
    wkl = sorted({week(d) for d in days})
    with open(f"data/cluster/population_{a.board}.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["week", "sampled_days", "taken", "weighted_postings"])
        for u in wkl:
            m = np.array([week(d) == u for d in days])
            wr.writerow([u, int(m.sum()), int(n_d[m].sum()), round(float(W_d[m].sum()), 1)])

    # ---- emergence
    by = defaultdict(dict)
    for r in series:
        by[r["cluster"]][r["quarter"]] = r
    fullq = [q for q in qs if qinfo[q]["full"]]
    first_cross, first_cross_s = {}, {}
    for c in clusters:
        if c < 0:
            continue
        for q in fullq:
            r = by[c][q]
            if c not in first_cross and r["weighted_adjusted"] >= a.threshold:
                first_cross[c] = q
            if c not in first_cross_s and r["share"] >= a.share_threshold:
                first_cross_s[c] = q
    emerg = []
    newlist = []     # (cluster, period index, period) : clearly new
    for qn, q in enumerate(fullq):
        act = sum(by[c][q]["weighted_adjusted"] >= a.threshold for c in clusters if c >= 0)
        act_s = sum(by[c][q]["share"] >= a.share_threshold for c in clusters if c >= 0)
        new = sum(v == q and q != fullq[0] for v in first_cross.values())
        new_s = sum(v == q and q != fullq[0] for v in first_cross_s.values())
        # strict: the whole interval C is above the line now, and was wholly below it in the previous usable quarter
        clear = sum(by[c][q]["adjusted_lo_C"] >= a.threshold for c in clusters if c >= 0)
        strict = sum(qn > 0 and by[c][q]["adjusted_lo_C"] >= a.threshold and by[c][fullq[qn - 1]]["adjusted_hi_C"] < a.threshold
                     for c in clusters if c >= 0)
        for c in clusters:
            if c >= 0 and qn > 0 and by[c][q]["adjusted_lo_C"] >= a.threshold and by[c][fullq[qn - 1]]["adjusted_hi_C"] < a.threshold:
                newlist.append((c, qn, q))
        emerg.append((q, act, new, act_s, new_s, clear, strict))

    # ---- baseline
    base = {}
    if a.event:
        ev_name, ev_day = a.event.split("=")
        pre_d = np.array([d < ev_day for d in days])
        ev = date.fromisoformat(ev_day)

        def inwin(d):
            if a.window_days <= 0:
                return True
            k_ = (date.fromisoformat(d) - ev).days
            return -a.window_days <= k_ <= a.window_days - 1

        keys = sorted({(week(d), d < ev_day) for d in days if inwin(d)})
        uix = {k: i for i, k in enumerate(keys)}
        U = np.zeros((D, len(keys)))
        for i, d in enumerate(days):
            if inwin(d):
                U[i, uix[(week(d), d < ev_day)]] = 1
        P = (C / n_d[None, :]) * W_d[None, :]
        NUM, DEN = P @ U, W_d @ U
        upre = np.array([i for i, k in enumerate(keys) if k[1]])
        upost = np.array([i for i, k in enumerate(keys) if not k[1]])
        if len(upre) and len(upost):
            ip = rng.choice(upre, size=(a.boot, len(upre)))
            iq = rng.choice(upost, size=(a.boot, len(upost)))
            sp = NUM[:, ip].sum(2) / DEN[ip].sum(1)[None, :]
            sq = NUM[:, iq].sum(2) / DEN[iq].sum(1)[None, :]
            lo, hi = q95(sq - sp, axis=1)
            pre_s = NUM[:, upre].sum(1) / DEN[upre].sum()
            post_s = NUM[:, upost].sum(1) / DEN[upost].sum()
            for k, c in enumerate(clusters):
                base[c] = (pre_s[k], post_s[k], post_s[k] - pre_s[k], post_s[k] / pre_s[k] if pre_s[k] > 0 else float("nan"), lo[k], hi[k])

    # ---- flags, templates, titles
    fl_w, ch_w = np.zeros(K), defaultdict(Counter)
    fl_n = np.zeros(K)
    tg = [Counter() for _ in range(K)]
    nt = np.zeros(K)
    tt = [Counter() for _ in range(K)]
    for j, r in enumerate(rows):
        k = kix[j]
        ch = flag.get(ids[j])
        if ch:
            fl_w[k] += w[j]
            fl_n[k] += 1
            ch_w[k][ch] += w[j]
        key = re.sub(r"\W+", " ", (r["item"].get("description") or "")[:80].lower()).strip() or f"__none_{j}"
        tg[k][key] += 1
        nt[k] += ids[j] in notitle
        if ids[j] in ttl:
            tt[k][ttl[ids[j]]] += 1
    cl_w = np.bincount(kix, weights=w, minlength=K)

    # ---- HHI
    codes = sorted({v for v in reg.values() if v})
    ri = {c: i for i, c in enumerate(codes)}
    R = max(len(codes), 1)
    qix_post = qix_day[dix]
    placed = np.array([bool(reg.get(i)) for i in ids])
    rix = np.array([ri[reg[i]] if reg.get(i) else 0 for i in ids])
    Q = len(qs)
    Wreg = np.zeros((K + 1, Q, R))
    Wall = np.zeros((K + 1, Q))
    Npl = np.zeros((K + 1, Q))
    for j in range(len(rows)):
        for kk in (kix[j], K):
            Wall[kk, qix_post[j]] += w[j]
            if placed[j]:
                Wreg[kk, qix_post[j], rix[j]] += w[j]
                Npl[kk, qix_post[j]] += 1
    Rn = REGIONS[a.country]

    def hhi_of(vec):
        t = vec.sum()
        return float((vec / t) ** 2 @ np.ones(len(vec))) if t > 0 else float("nan")

    hrows = []
    for kk in range(K + 1):
        name = "ALL" if kk == K else clusters[kk]
        for qi, q in enumerate(qs + ["all"]):
            if q == "all":
                vec, wa, npl = Wreg[kk].sum(0), Wall[kk].sum(), Npl[kk].sum()
            else:
                vec, wa, npl = Wreg[kk, qi], Wall[kk, qi], Npl[kk, qi]
            h = hhi_of(vec)
            hrows.append({"cluster": name, "quarter": q, "placed_taken": int(npl), "hhi": h,
                          "hhi_norm": (h - 1 / Rn) / (1 - 1 / Rn) if h == h else float("nan"),
                          "unplaced_share": 1 - vec.sum() / wa if wa > 0 else float("nan"),
                          "reliable": int(npl >= a.min_placed)})
    with open(f"data/cluster/hhi_{tag}.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(hrows[0].keys()))
        wr.writeheader()
        wr.writerows(hrows)
    hall = {r["cluster"]: r for r in hrows if r["quarter"] == "all"}

    # ---- summary
    summ = []
    for k, c in enumerate(clusters):
        rs = [by[c][q] for q in fullq]
        pk = max(rs, key=lambda r: r["weighted_adjusted"]) if rs else None
        topg = tg[k].most_common(1)[0][1] / max(sum(tg[k].values()), 1)
        topch = ch_w[k].most_common(1)[0] if ch_w[k] else ("", 0.0)
        tl_share = nt[k] / max(C[k].sum(), 1)
        eligible = c >= 0 and c in first_cross and topg < a.max_template and tl_share <= a.max_titleless
        summ.append({"cluster": c, "taken": int(C[k].sum()), "weighted_total": cl_w[k],
                     "peak_quarter": pk["quarter"] if pk else "", "peak_adjusted": pk["weighted_adjusted"] if pk else 0,
                     "peak_share": pk["share"] if pk else 0, "first_cross": first_cross.get(c, ""),
                     "first_cross_share": first_cross_s.get(c, ""),
                     "flagged_taken": int(fl_n[k]), "flagged_share": fl_w[k] / cl_w[k] if cl_w[k] else 0, "top_channel": topch[0],
                     "top_channel_share_of_flagged": topch[1] / fl_w[k] if fl_w[k] else 0,
                     "top_template_share": topg, "template_groups": len(tg[k]), "titleless_share": tl_share,
                     "hhi_norm": hall[c]["hhi_norm"], "unplaced_share": hall[c]["unplaced_share"],
                     "eligible": int(eligible),
                     "pre": base.get(c, [None] * 6)[0], "post": base.get(c, [None] * 6)[1],
                     "diff": base.get(c, [None] * 6)[2], "ratio": base.get(c, [None] * 6)[3],
                     "diff_lo": base.get(c, [None] * 6)[4], "diff_hi": base.get(c, [None] * 6)[5],
                     "top_titles": " | ".join(t for t, _ in tt[k].most_common(3))})
    with open(f"data/cluster/summary_{tag}.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(summ[0].keys()))
        wr.writeheader()
        wr.writerows(summ)

    # ---- report
    nclu = sum(c >= 0 for c in clusters)
    el = sorted((s for s in summ if s["eligible"]), key=lambda s: -s["peak_adjusted"])
    md = [f"# Cluster series: {a.board}, input {a.input}", "",
          f"{len(rows):,} postings after {dup:,} duplicates; {nclu} clusters plus noise; {unl} postings without a label. "
          f"Noise holds {summ[clusters.index(-1)]['taken'] / len(rows):.1%} of the postings." if -1 in clusters else
          f"{len(rows):,} postings after {dup:,} duplicates; {nclu} clusters.", "",
          f"Threshold: {a.threshold:g} weighted postings a quarter (adjusted to all calendar days of the quarter) and, as a share version, {a.share_threshold:.2%} of the quarter. "
          f"Eligible = crosses the threshold in a quarter with at least {a.min_days} sampled days and its largest template group holds under {a.max_template:.0%} of its postings and at most {a.max_titleless:.0%} of its postings lack a title. "
          f"Eligible clusters: {len(el)} of {nclu}.", "",
          "## Coverage per quarter", "", "| quarter | sampled days | calendar days | weighted postings (sampled days) | usable |", "|---|---|---|---|---|"]
    md += [f"| {q} | {v['days']} | {v['cal']} | {v['pop']:,.0f} | {'yes' if v['full'] else 'no'} |" for q, v in qinfo.items()]
    md += ["", "## Occupation Emergence Rate", "",
           "| quarter | at or above threshold | newly crossing | at or above share threshold | newly crossing (share) | clearly above (interval C) | clearly new (interval C) |",
           "|---|---|---|---|---|---|---|"]
    md += [f"| {q} | {x} | {nw} | {xs} | {ns} | {cl_} | {st} |" for q, x, nw, xs, ns, cl_, st in emerg]
    md += ["", "Clearly above = the lower end of interval C is at or above the threshold. Clearly new = clearly above now and the upper end of interval C was below the threshold in the previous usable quarter. "
           "The count version moves with the weighted population of the board (see the coverage table); the share version does not."]
    md += ["", f"The first usable quarter ({fullq[0] if fullq else '-'}) cannot show new crossings; clusters already above the line then count as present at the start.", "",
           "## Eligible clusters (largest peak first)", "",
           "| cluster | taken | peak quarter | peak adjusted | peak share | first crossing | flagged | top channel | top template | HHI norm | unplaced | change vs event (95% interval) | top titles |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in el[:40]:
        ch = f"{s['diff']:+.2%} ({s['diff_lo']:+.2%} to {s['diff_hi']:+.2%})" if s["diff"] is not None else "-"
        md.append(f"| {s['cluster']} | {s['taken']} | {s['peak_quarter']} | {s['peak_adjusted']:,.0f} | {s['peak_share']:.2%} | {s['first_cross']} | "
                  f"{s['flagged_share']:.0%} | {s['top_channel']} {s['top_channel_share_of_flagged']:.0%} | {s['top_template_share']:.0%} | "
                  f"{s['hhi_norm']:.2f} | {s['unplaced_share']:.0%} | {ch} | {s['top_titles'][:90]} |")
    sm = {x["cluster"]: x for x in summ}

    def srow(c, extra):
        x = sm[c]
        return (f"| {c} | {x['taken']} | {extra} | {x['flagged_share']:.0%} | {x['top_template_share']:.0%} | {x['titleless_share']:.0%} | "
                f"{'eligible' if x['eligible'] else 'not eligible'} | {x['top_titles'][:90]} |")

    md += ["", "## Clearly new clusters (interval C wholly above the threshold now, wholly below it in the previous usable period)", "",
           "Candidates for emerging occupations. Read the share in the next periods too: a real new occupation stays above the line.", "",
           "| cluster | taken | first clearly new | flagged | top template | without title | eligible | top titles |", "|---|---|---|---|---|---|---|---|"]
    seen = set()
    for c, qn, q in sorted(newlist, key=lambda t: (t[1], -sm[t[0]]["peak_adjusted"])):
        if c in seen:
            continue
        seen.add(c)
        later = [r_ for r_ in fullq[qn:] if by[c][r_]["adjusted_lo_C"] >= a.threshold]
        md.append(srow(c, f"{q}; stays clearly above in {len(later)} of {len(fullq) - qn} periods from then on"))
    if not seen:
        md.append("| - | | none | | | | | |")
    if len(fullq) >= 2:
        f0, f1 = fullq[0], fullq[-1]
        rise = []
        for c in clusters:
            if c < 0:
                continue
            r0, r1 = by[c][f0], by[c][f1]
            rise.append((r1["share"] - r0["share"], c, r0, r1))
        rise.sort(key=lambda t: -t[0])
        md += ["", f"## Largest rise in share, first usable period ({f0}) to last ({f1})", "",
               "Both ends are weighted shares of the whole board with interval C. Clear = the lower end at the last period is above the upper end at the first.", "",
               "| cluster | taken | share first (interval C) | share last (interval C) | clear | flagged | top template | without title | eligible | top titles |", "|---|---|---|---|---|---|---|---|---|---|"]
        for d_, c, r0, r1 in rise[:15]:
            x = sm[c]
            md.append(f"| {c} | {x['taken']} | {r0['share']:.2%} ({r0['share_lo_C']:.2%} to {r0['share_hi_C']:.2%}) | {r1['share']:.2%} ({r1['share_lo_C']:.2%} to {r1['share_hi_C']:.2%}) | "
                      f"{'yes' if r1['share_lo_C'] > r0['share_hi_C'] else 'no'} | {x['flagged_share']:.0%} | {x['top_template_share']:.0%} | {x['titleless_share']:.0%} | "
                      f"{'eligible' if x['eligible'] else 'not eligible'} | {x['top_titles'][:80]} |")
    fl_rank = sorted((s for s in summ if s["cluster"] >= 0 and s["flagged_taken"] >= 10 and s["top_template_share"] < a.max_template and s["titleless_share"] <= a.max_titleless),
                     key=lambda s: -s["flagged_share"])
    md += ["", "## Clusters with the largest flagged share (at least 10 flagged postings taken, not template-dominated)", "",
           "| cluster | taken | flagged taken | flagged share (weighted) | top channel | peak share | first crossing | top template | HHI norm | unplaced | change vs event (95% interval) | top titles |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    md += [f"| {s['cluster']} | {s['taken']} | {s['flagged_taken']} | {s['flagged_share']:.0%} | {s['top_channel']} {s['top_channel_share_of_flagged']:.0%} | "
           f"{s['peak_share']:.2%} | {s['first_cross']} | {s['top_template_share']:.0%} | {s['hhi_norm']:.2f} | {s['unplaced_share']:.0%} | "
           + (f"{s['diff']:+.2%} ({s['diff_lo']:+.2%} to {s['diff_hi']:+.2%})" if s["diff"] is not None else "-") + f" | {s['top_titles'][:90]} |"
           for s in fl_rank[:25]]
    tpl = sorted((s for s in summ if s["cluster"] >= 0 and s["cluster"] in first_cross and not s["eligible"]),
                 key=lambda s: -s["peak_adjusted"])
    if tpl:
        md += ["", "## Crossing the threshold but not eligible (one template or mostly title-less)", "",
               "| cluster | taken | peak adjusted | top template | without title | unplaced | top titles |", "|---|---|---|---|---|---|---|"]
        md += [f"| {s['cluster']} | {s['taken']} | {s['peak_adjusted']:,.0f} | {s['top_template_share']:.0%} | {s['titleless_share']:.0%} | {s['unplaced_share']:.0%} | {s['top_titles'][:90]} |" for s in tpl[:20]]
    md += ["", "## Reading notes", "",
           "- Report interval C (weeks redrawn) when judging a change; A is optimistic when postings of a day are clumped.",
           "- Adjusted counts assume unsampled days resemble sampled ones; quarters with few sampled days are not used for crossings.",
           "- HHI uses placed postings only; read it with the unplaced share and the number of placed postings (data/cluster/hhi_*.csv).",
           "- Baseline windows are the --window-days days before and from the event (default 90), the same length on both sides; check the coverage of each window before reading a difference."]
    Path(f"docs/emergence_{tag}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:40]))


if __name__ == "__main__":
    main()
