# Month 3 methodology: deglobalization lexicon and posting classifier

Oct 20, 2026 · @anton

## Purpose and deliverables

Month 3 builds a lexicon of deglobalization terms, uses it to find relevant postings, has an LLM tag each by channel and intensity, and measures the result on 300 hand-annotated postings. This document fixes the order of work and the assumptions behind it, so the thesis can state them.

The brief asks for four deliverables:

- A final lexicon of 300 to 500 terms, grown from 30 to 50 seed terms with TF-IDF (uni-, bi- and tri-grams) and multilingual-e5 embedding similarity.
- A tagged posting dataset: channel and intensity (low, medium, high) for each flagged posting.
- A classifier evaluation report: precision, recall and F1 on 300 annotated postings.
- A prompt template library for the LLM classification.

The method follows the brief's methodological reference, Kavargyris et al. (2025), Algorithms 18(9), 554: an LLM tags the postings, a human-annotated sample validates it, and several models are compared on that sample.

## Data and what it supports

Every step uses one corpus: the day-stratified download of jobbland.se postings for January to August 2026 (script 52), 22,638 postings before de-duplication. The skill, occupation and sector tags are empty in 2026, so everything rests on the title and description text.

Exact duplicate descriptions are dropped (5.5% of the sample), and each posting carries a day weight (the day's total postings divided by the postings taken that day) that scales sample counts to the month's population.

The corpus is an English-language slice, not the Swedish labour market. About 98% of the postings are in English, and titles are dominated by municipality, region, nurse, teacher and manager roles. Results describe that slice. The 2024 sources from Months 1 and 2 (other boards and countries) are not used in this step.

## Ordered steps

Sixteen steps, in this order. Steps 1 and 2 are done; step 10 waits for a decision (see Open decisions). The lexicon is frozen at step 7 and the prompt at step 8, before any posting is annotated, because the annotation sample depends on both.

| # | Action | Who or script | Where | Output |
| --- | --- | --- | --- | --- |
| 1 | Download the day-stratified corpus and check that its composition is stable month to month | scripts 52, 51 | laptop (done) | data/raw/corpus\_jobbland.se\_2026-01\_2026-08.jsonl |
| 2 | De-duplicate and attach day weights (automatic in every later script) | corpus\_io.py | any | none: done on load |
| 3 | Review the seed list: 51 terms after the author's revision of 20 October, 13 of them the brief's examples. Keep, cut or add; decide whether to add task-language terms | author | by hand | lexicon/seed\_lexicon.csv |
| 4 | Count how often each seed term occurs and surface TF-IDF n-grams that co-occur with them. Stop point: if fewer than 50 postings contain a seed term, widen the seeds or the corpus before step 5 | script 55 | Colab or laptop | docs/lexicon\_seed\_coverage.md, data/lexicon/candidates\_tfidf.csv |
| 5 | Find phrases close to the seeds with multilingual-e5-base embeddings and FAISS | script 56 | Colab, GPU | data/lexicon/candidates\_embedding.csv |
| 6 | Review both candidate sheets: put 1 under keep and one channel for each term to add | author (hours) | by hand | reviewed sheets |
| 7 | Build the lexicon (target 300 to 500 terms) and freeze it with a date | script 57 | any | lexicon/lexicon.csv, docs/lexicon\_summary.md |
| 8 | Fix the channel and intensity definitions. Pilot: annotate 20 postings that are not in the 300, revise the definitions once, then freeze | author, supervisor | by hand | prompts/tagging\_v1 (or v2), docs/tagging\_annotation\_guide.md |
| 9 | Flag postings with the frozen lexicon and tag them with each model: Qwen 2.5 7B and Mistral 7B, same prompt, temperature 0 | script 58 | Colab, GPU | data/tagged/tags\_\<model>\_\<prompt>.jsonl |
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
| A7 | LLM answers are repeatable at temperature 0 with a fixed seed, and the model version is pinned (record the Ollama model digest) | Untested | Re-run a sample at step 9 |
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

Four decisions are open, and the first one changes the code. The scripts for steps 10 and 11 are not written yet: script 59 currently draws the 300 postings from flagged postings only, which cannot measure the residual lexicon error.

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
