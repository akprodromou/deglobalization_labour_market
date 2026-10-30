# Month 3 methodology: deglobalization lexicon and posting classifier

Oct 28, 2026 · @anton

## Purpose and deliverables

Month 3 builds a lexicon of deglobalization terms, uses it to find relevant postings, has an LLM tag each by channel and intensity, and measures the result on 300 hand-annotated postings. This document fixes the order of work and the assumptions behind it, so the thesis can state them.

The brief asks for four deliverables:

- A final lexicon of 300 to 500 terms, grown from 30 to 50 seed terms with TF-IDF (uni-, bi- and tri-grams) and multilingual-e5 embedding similarity. The supervisor accepted a lexicon of 150 terms instead (27 October 2026).
- A tagged posting dataset: channel and intensity (low, medium, high) for each flagged posting.
- A classifier evaluation report: precision, recall and F1 on 300 annotated postings.
- A prompt template library for the LLM classification.

The method follows the brief's methodological reference, Kavargyris et al. (2025), Algorithms 18(9), 554: an LLM tags the postings, a human-annotated sample validates it, and several models are compared on that sample.

## Status and decisions, 28 October 2026

The tagger is Claude Haiku 4.5 with prompt v8, chosen because it matches the agreed definitions and scores the same as its predecessors within noise. All results below are round-1 development results; the round-2 test is being annotated.

**Decisions since 20 October**

- **Lexicon:** 150 terms, English only, six channels; accepted by the supervisor on 27 October 2026 in place of 300 to 500.
- **Channel definitions:** strategic-sector view, accepted by the supervisor (27 October). Total-defence and security-check boilerplate is removed before matching.
- **Reshoring** (author, 28 October): firms moving production back from abroad. A posting cannot show the earlier offshoring, so the sectors are fixed in advance: space, aerospace, semiconductors and electronic components, and battery production. Wind and solar equipment manufacturing is energy security, never reshoring.
- **Trade compliance** (author, 28 October): routine customs and shipping paperwork, "exports" in a company description and a skill listed as "a plus" are none. Customs-authority staff count only when the duties involve declarations, origin, sanctions or export control.
- **Intensity** (author, 28 October): stays at three levels as defined, not collapsed; channel is the main measure.
- **Models:** Qwen 2.5 7B (Ollama) and Claude Haiku 4.5 (API). Mistral 7B was not run, and a Sonnet run was cancelled to limit cost.
- **Prompt versions:** v6 (customs-authority rule, strategic sectors), v7 (stricter on reshoring, trade compliance and intensity), v8 (reshoring and energy security boundary, 28 October). The annotation guide carries the same wording as the prompt.

**Evaluation design**

Round 1 has 472 annotated postings: 322 lexicon-flagged postings drawn in strata by Qwen's predicted channel, and 150 postings without a lexicon term to measure what the lexicon misses. Its labels were made under the v6 guide and were used to develop the prompts, so its scores are optimistic. Round 2 is a fresh sample of 300 flagged postings, drawn from Haiku v7's strata with every round-1 posting left out, and annotated under the v8 guide. Round 1 used up nearly all rare-channel postings, so round 2 holds only 9 reshoring, 3 trade compliance and no critical materials postings: it tests defense, energy security and the overall relevant-or-not decision, not the rare channels.

**Round-1 results** (F1 per channel; intensity as quadratic-weighted kappa)

| Run | Macro-F1 | Any vs none | Reshoring | Defense | Critical materials | Energy security | Trade compliance | Intensity kappa |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen 2.5 7B, v6 | 0.57 | 0.84 | 0.52 | 0.87 | 0.82 | 0.82 | 0.36 | 0.55 |
| Qwen 2.5 7B, v7 | 0.53 | 0.82 | 0.43 | 0.85 | 0.72 | 0.73 | 0.45 | 0.61 |
| Haiku 4.5, v6 | 0.65 | 0.89 | 0.81 | 0.92 | 0.90 | 0.84 | 0.43 | 0.64 |
| Haiku 4.5, v7 | 0.66 | 0.88 | 0.84 | 0.92 | 0.89 | 0.79 | 0.53 | 0.58 |
| Haiku 4.5, v8 | 0.64 | 0.88 | 0.80 | 0.90 | 0.82 | 0.82 | 0.51 | 0.58 |

Haiku is clearly ahead of Qwen. Among the Haiku prompts the differences are inside the intervals and inside the run-to-run noise (21 of 622 postings changed channel between v7 and v8, against 3% between two runs of the same prompt).

**How to read it**

- Defense, energy security and critical materials are usable. Energy security loses mostly low-intensity sales, recruiting and admin roles at solar and battery firms (17 of 20 missed), which the guide rates low and the model rates none.
- Reshoring is precise (0.93 under v8) with lower recall.
- Trade compliance stays weak: precision about 0.35, recall about 0.89. The model reads "responsible for customs procedures" as compliance work; the guide does not. Report it as a candidate flag.
- Diversification has one annotated posting and cannot be evaluated.
- Intensity is exploratory. The annotator agreed with himself on channel for 43 of 50 postings (86%, Cohen's kappa 0.76), but on intensity only weighted kappa 0.11 (15 postings), below the model-annotator kappa of 0.58.
- Lexicon precision is 0.62; 2% of postings without a lexicon term were judged relevant (interval 0.00 to 0.04).

**Limits to state**

**Round-2 results** (Haiku v8, weighted F1 with 95% bootstrap intervals; 28 October)

| Labels used | Defense | Energy security | Any channel vs none | Intensity (weighted kappa) |
| --- | --- | --- | --- | --- |
| All 300 rows | 0.86 (0.81 to 0.91) | 0.64 (0.50 to 0.79) | 0.84 (0.79 to 0.88) | 0.39 |
| Human rows only (1 to 59) | 0.85 (0.72 to 0.95) | 0.71 (0.41 to 0.99) | 0.84 (0.72 to 0.93) | 0.18 |

Rows 1 to 59 were annotated by the author; rows 60 to 300 were labelled by Claude under the v8 guide, at the author's request, and are marked in the `source` column of the completed sheet. Labeller and tagger belong to the same model family, so the 241 Claude rows are a consistency check, not independent validation, and the thesis must report them as such. The 59 human rows alone are too few for narrow intervals.

Defense is stable across both label sets. Energy security has lower recall (about 0.60): the misses are mostly low-intensity sales, recruiting and administrative roles. Lexicon precision is 0.59 on all rows and 0.66 on the human rows: about 40% of flagged postings are not about any channel. Reshoring (8 postings), trade compliance (1), critical materials (0) and diversification (0) cannot be assessed on this sample. Intensity stays exploratory: Haiku rates most postings medium where the annotator rated them high.

**Tagger for the full corpus: Qwen 2.5 7B with the v8 prompt** (29 October)

Claude Haiku 4.5 scored higher but costs about $3.50 per 1,000 postings, so the author chose Qwen, which runs free on a Colab GPU. Haiku stays in the thesis as the benchmark and as future work if funding allows. Weighted F1 on the 618 annotated postings both models tagged:

| Measure | Qwen v8 | Haiku v8 |
| --- | --- | --- |
| Round 1, defense | 0.87 | 0.90 |
| Round 1, energy security | 0.76 | 0.82 |
| Round 1, reshoring | 0.44 | 0.80 |
| Round 1, macro-F1 | 0.53 | 0.64 |
| Round 2, defense (all rows) | 0.84 | 0.86 |
| Round 2, energy security (all rows) | 0.68 | 0.64 |
| Round 2, reshoring (all rows) | 0.03 | 0.23 |
| Any channel vs none, rounds 1 and 2 | 0.82 and 0.82 | 0.88 and 0.84 |

Qwen is usable for defense, energy security and the relevant-or-not decision. It misses most reshoring postings in round 2 and over-flags trade compliance (precision about 0.25), so reshoring, trade compliance and critical materials are reported as noisy candidate flags, not as measured quantities. Five of 618 answers on the annotated postings, and 9 of 2,792 in the full run, were invalid and are counted as none.

**Full-corpus result** (merged jobbland.se corpus, January 2024 to September 2026)

The corpus holds 53,959 postings after exact duplicates are removed; 2,792 (5.2%) contain a lexicon term and were tagged. Defense is the largest channel, at about 2 to 3% of all postings from September 2024 on, and energy security is about 0.5%. Change in the weighted share of all postings, 90 days before to 90 days after each event, in percentage points with 95% intervals:

| Channel | Critical Raw Materials Act (23 May 2024) | AccelerateEU (22 April 2026) |
| --- | --- | --- |
| Defense | -0.35 (-1.37 to +0.59) | +0.32 (-0.26 to +0.86) |
| Energy security | -0.29 (-0.99 to +0.23) | +0.04 (-0.21 to +0.29) |
| Reshoring | -0.21 (-0.61 to +0.17) | +0.01 (-0.08 to +0.12) |
| Trade compliance | -0.15 (-0.38 to +0.02) | -0.03 (-0.19 to +0.13) |
| Critical materials | -0.13 (-0.33 to +0.05) | -0.08 (-0.15 to -0.02) |

No change is distinguishable from zero except critical materials around AccelerateEU, which moves from 0.08% to 0.00% of postings. That is a handful of postings tagged by the least validated channel, and one interval in 60 excluding zero is what chance would give, so it is not evidence of an effect. The window before the Critical Raw Materials Act is thin (1,447 postings taken, about 2,100 in the population), which is why those intervals are wide. The result is that this tagger and this sample show no measurable shift in any channel around either event; the intervals on defense (about half a percentage point on a 2% share) would show a change of roughly a quarter or more of the share, and smaller changes cannot be ruled out. December 2025 stands out for defense (6.4%, interval 4.9 to 8.2), outside both event windows, and its postings should be checked for a single employer or campaign before the monthly series is described.

- One annotator; round-1 labels precede the final definitions.
- Claude Haiku ran with default sampling, not temperature 0.
- Rare channels have 15 to 20 annotated postings, so their intervals are wide.
- The corpus is an English-language slice of jobbland.se and the lexicon is English only.

**Next**

1. Round 2 is annotated and scored (59 human rows, 241 Claude rows); a further human pass on the Claude rows would remove the circularity
2. Full corpus tagged with Qwen v8 and channel shares computed (script 64); next, check the December 2025 defense spike and choose the sector split, if the thesis needs one
3. Sector classifier (manufacturing, metals) for the steel regulation and AccelerateEU events, from the 400-posting validation sheet.
4. ESCOX at 0.45 as an outage diagnostic only if needed.

## Data and what it supports

Every step uses one corpus: the day-stratified download of jobbland.se postings for January to August 2026 (script 52), 22,638 postings before de-duplication. The skill, occupation and sector tags are empty in 2026, so everything rests on the title and description text.

Exact duplicate descriptions are dropped (5.5% of the sample), and each posting carries a day weight (the day's total postings divided by the postings taken that day) that scales sample counts to the month's population.

The corpus is an English-language slice, not the Swedish labour market. About 98% of the postings are in English, and titles are dominated by municipality, region, nurse, teacher and manager roles. Results describe that slice. The 2024 sources from Months 1 and 2 (other boards and countries) are not used in this step.

## Ordered steps

Sixteen steps, in this order. Steps 1 to 14 are done for the first annotation round; the second round, on a fresh sample, is being annotated (see Status and decisions). The lexicon is frozen at step 7 and the prompt at step 8, before any posting is annotated, because the annotation sample depends on both.

| # | Action | Who or script | Where | Output |
| --- | --- | --- | --- | --- |
| 1 | Download the day-stratified corpus and check that its composition is stable month to month | scripts 52, 51 | laptop (done) | data/raw/corpus\_jobbland.se\_2026-01\_2026-08.jsonl |
| 2 | De-duplicate and attach day weights (automatic in every later script) | corpus\_io.py | any | none: done on load |
| 3 | Review the seed list: 51 terms after the author's revision of 20 October, 13 of them the brief's examples. Keep, cut or add; decide whether to add task-language terms | author | by hand | lexicon/seed\_lexicon.csv |
| 4 | Count how often each seed term occurs and surface TF-IDF n-grams that co-occur with them. Stop point: if fewer than 50 postings contain a seed term, widen the seeds or the corpus before step 5 | script 55 | Colab or laptop | docs/lexicon\_seed\_coverage.md, data/lexicon/candidates\_tfidf.csv |
| 5 | Find phrases close to the seeds with multilingual-e5-base embeddings and FAISS | script 56 | Colab, GPU | data/lexicon/candidates\_embedding.csv |
| 6 | Review both candidate sheets: put 1 under keep and one channel for each term to add | author (hours) | by hand | reviewed sheets |
| 7 | Build the lexicon (150 terms, accepted by the supervisor on 27 October 2026) and freeze it with a date | script 57 | any | lexicon/lexicon.csv, docs/lexicon\_summary.md |
| 8 | Fix the channel and intensity definitions. Pilot: annotate 20 postings that are not in the 300, revise the definitions once, then freeze | author, supervisor | by hand | prompts/tagging\_v1 (or v2), docs/tagging\_annotation\_guide.md |
| 9 | Flag postings with the frozen lexicon and tag them with each model: Qwen 2.5 7B (Ollama, temperature 0) and Claude Haiku 4.5 (API, default sampling); Mistral 7B was not run | script 58 | Colab, GPU | data/tagged/tags\_\<model>\_\<prompt>.jsonl |
| 10 | Second detector for the residual error: tag a random subsample of the unflagged postings with the same model, so the sample can reach relevant postings the lexicon missed | script 58 (extension needed) | Colab, GPU | tags for the unflagged subsample |
| 11 | Draw the 300 postings: strata by predicted channel among flagged postings, plus strata from step 10 | script 59 (extension needed) | any | annotation sheet, hidden key |
| 12 | Annotate blind, text only, in sittings of up to about 100, with the date of each sitting in the first row's note | author (3 to 4 hours) | by hand | filled sheet |
| 13 | After at least three days, annotate 50 of them again | author | by hand | pass-2 sheet |
| 14 | Score each model: precision, recall and F1 per channel with intervals, intensity agreement, lexicon precision, residual error, your consistency | script 60 | any | docs/tagging\_results.md |
| 15 | Choose the model with the best macro-F1 and keep its tags as the tagged dataset | author | by hand | tagged posting dataset |
| 16 | Write up: lexicon completeness paragraph (residual error from step 14), limits, supervisor note | author | by hand | report section |

A parallel track is on hold: the 400-posting sector validation (manufacturing, metals) is annotated, but the sector classifier waits until Month 3 is finished. It does not feed steps 1 to 16.

## Assumptions

Thirteen assumptions underlie the steps. Two are untested (A2 and A7), one is still a draft (A8), and step 4 tests the most consequential one, A2.

| # | Assumption | Status | Checked at |
| --- | --- | --- | --- |
| A1 | The corpus is an English-language slice of jobbland.se, dominated by public-sector and care roles; results describe that slice | Known (98% English) | Profiling, done |
| A2 | Postings describe deglobalization-related work in task and skill terms (customs declarations, export licences, sanctions screening) more than in policy terms (friend-shoring, strategic autonomy, China plus one) | Untested | Step 4 |
| A3 | A posting is tagged only if it contains a lexicon term; what the lexicon misses is the residual error named in the brief's lexicon-completeness limitation | By design | Steps 10 to 14 |
| A4 | De-duplication and day weights make the sample representative of each month; only exact duplicates are removed and the population is treated as distinct texts | Partly checked (no stability flags, Jan to Aug) | Stability check, done |
| A5 | The author's annotation is the reference; there is one annotator, whose consistency is measured by repeating 50 postings | By design | Steps 13, 14 |
| A6 | Annotation and models use the posting text only. Outside knowledge of an employer is not used, and is marked in the note when it was | Rule | Step 12 |
| A7 | LLM answers are repeatable at temperature 0 with a fixed seed, and the model version is pinned (record the Ollama model digest). This was not possible for Claude Haiku: the installed API package rejected the temperature argument, so it ran with default sampling; two runs of the same prompt gave the same channel for 97% of postings | Untested | Re-run a sample at step 9 |
| A8 | The channels come from the author's event timeline. The three intensity levels come from the brief; their definitions are the author's draft | Draft | Step 8 |
| A9 | No pass/fail threshold: models are compared and reported with intervals, as in Kavargyris et al. The 0.80 and 0.70 thresholds in the earlier sector protocol were not in the brief and are dropped | Decided | Step 14 |
| A10 | Strata of the annotation sample are defined by one model's predictions; weights come from the sampling design, so the other models can be scored on the same sample | By design | Step 14 |
| A11 | Embedding similarity only proposes candidate terms; the author decides membership and channel | Rule | Step 6 |
| A12 | The lexicon is English only; the Swedish postings (about 2% of the corpus), and Greek and other languages, are out of scope in this step | Scope | n/a |
| A13 | Everything runs on Google Colab with data on Google Drive; employer text is kept out of git | Decided | All steps |

## What the evaluation measures

Every measure is computed against the author's annotation, on weighted postings, with 95% bootstrap intervals that resample inside each stratum. The population matters for each one, so each row names it.

| Measure | Population | Definition |
| --- | --- | --- |
| Channel precision | Lexicon-flagged postings | Of the postings the model put in a channel, the weighted share the annotator also put there |
| Channel recall | Lexicon-flagged postings | Of the postings the annotator put in a channel, the weighted share the model found |
| F1, macro-F1 | Lexicon-flagged postings | Harmonic mean of precision and recall; macro-F1 averages it over the channels present in the annotation, and is the rule for choosing a model at step 15 |
| Any channel against none | Lexicon-flagged postings | The same measures after merging all channels: does the posting relate to deglobalization at all |
| Lexicon precision | Lexicon-flagged postings | Share the annotator judges relevant (not none): how often a lexicon match is a false match |
| Residual lexicon error | All postings, from the unflagged strata of steps 10 and 11 | Share of relevant postings that contain no lexicon term. This is the error the brief's limitation text says the 300 postings measure; a sample of flagged postings alone cannot show it |
| Pipeline recall | All postings | Lexicon recall combined with classifier recall |
| Intensity agreement | Postings where model and annotator agree on a channel other than none | Exact agreement and quadratic-weighted kappa on low, medium, high |
| Annotator consistency | 50 postings annotated twice | Cohen's kappa for channel, weighted kappa for intensity |

Postings the annotator marks unclear are left out and their share is reported. A posting the model answers with invalid output counts as a wrong prediction.

## Open decisions and differences from the brief

These were the open decisions on 20 October. The section Status and decisions records how each was settled; the table keeps the original options for the record.

| Decision | Options | Recommendation |
| --- | --- | --- |
| Design of the residual-error check (step 10) | (a) Tag every unflagged posting with the LLM: complete, but about 20,000 postings. (b) Tag a random subsample (for example 4,000) of the unflagged postings and sample from its strata: cheaper, weighted back. (c) Annotate a random unflagged sample only: cheapest, but if relevant postings are rare it can only bound their rate | (b), decided after step 4 shows how many postings are flagged |
| Seed list (step 3) | Keep as drafted (policy terms from the brief and the timeline), or add task-language seeds | Decide after the coverage report of step 4 |
| Intensity definitions (step 8) | The draft in the annotation guide: high is the main subject of the role, medium is one of several duties, low is a passing mention | Confirm with the supervisor, then pilot on 20 postings |
| Models (step 9) | Qwen 2.5 7B and Mistral 7B (named in the brief), plus optionally Llama 3 8B, the model the paper used | The two from the brief; add the third only if time allows |

Where this document goes beyond or differs from the brief:

- The brief fixes the three intensity levels but does not define them; the definitions are the author's.
- The categories none and unclear are additions, needed to measure false lexicon matches and undecidable postings.
- The brief evaluates on 300 annotated postings. Here they are drawn in strata and weighted, so that rare channels have enough postings, and they include unflagged postings, so that the lexicon-completeness limitation is measured and not only stated.
- The brief lists spaCy for lemmatization. Matching here uses regular expressions with plural, hyphen and spelling variants instead, which is simpler but less general.
- The sector classifier (manufacturing, metals) is outside the brief and on hold.

## Running on Google Colab

A GPU runtime is needed only for steps 5, 9 and 10; the others run on any runtime. Choose Runtime, Change runtime type, GPU.

- **GPU:** a T4 (16 GB) is enough for the e5 embeddings and for 7B models in 4-bit form through Ollama (about 5 GB). An L4 (24 GB) or A100 (40 GB) tags faster. Colab does not guarantee a given GPU, so availability depends on the plan and on demand. The paper used an A100 with high RAM.
- **RAM:** if steps 4 or 5 stop with a memory error (they count phrases over about 22,000 postings), switch on the High-RAM option.
- **Storage:** Colab's disk is erased when the session ends. Keep the project folder on Google Drive, mount it, and run from it, so every output survives a disconnect. The corpus holds employer text: keep it on Drive, out of git.

Setup cell, run once per session:

```bash
from google.colab import drive
drive.mount('/content/drive')
%cd /content/drive/MyDrive/<project folder>
!pip install -q scikit-learn sentence-transformers faiss-cpu requests
```

Ollama cell, before steps 9 and 10:

```bash
!apt-get -qq install -y zstd
!curl -fsSL https://ollama.com/install.sh | sh
import subprocess; subprocess.Popen(["ollama", "serve"])
!ollama pull qwen2.5:7b
!ollama pull mistral
```

This install recipe is the usual one but has not been run for this project. If it fails, the tagger also has a Claude API backend (the brief allows it).

| Step | Command |
| --- | --- |
| 4 | python -m diagnostics.55\_lexicon\_seed\_coverage\_tfidf |
| 5 | python -m diagnostics.56\_lexicon\_embedding\_expansion |
| 7 | python -m diagnostics.57\_build\_lexicon |
| 9 | python -m diagnostics.58\_tag\_postings --backend ollama --model qwen2.5:7b (then --model mistral) |
| 11 | python -m diagnostics.59\_make\_tagging\_sheet --tags data/tagged/tags\_qwen2.5\_7b\_tagging\_v1.jsonl |
| 13 | python -m diagnostics.59\_make\_tagging\_sheet --pass2 50 |
| 14 | python -m diagnostics.60\_score\_tagging --tags \<tags file> (repeat --tags per model) |

Step 9 saves after every posting. If the session disconnects, run the same command again and it continues where it stopped.
