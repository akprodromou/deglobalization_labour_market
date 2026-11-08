# Deglobalization lexicon: change log (v1 to v7)

Final lexicon: `deglobalization_lexicon_final.csv`. It holds 188 active terms (English, six channels) and 4 terms removed in October 2026, which stay in the file with status `removed 2026-10-31`. The column `version_added` says in which version each term entered, and `origin` says where it came from.

A lexicon match only flags a posting for the tagger. The channel and the intensity come from the tagger (Qwen 2.5 7B, prompt v12) and from the post-tagging rules listed at the end of this file.

## Versions

| Version | Date | Terms | Change |
|---|---|---:|---|
| v1 | October 2026 | 150 | 49 seed terms (the brief's list and approved additions), 58 terms from the TF-IDF expansion (script 55) and 43 from the sentence-embedding expansion (script 56). Candidates entered only through the author's approval list (`lexicon_additions_approved.csv`). |
| v2 | October 2026 | 158 | Added 8 terms. Energy security: wind power, solar power, hydrogen, electrolyser, carbon capture, energy storage. Reshoring: battery manufacturing. Critical materials: battery recycling. "Smart grid", "solar cell manufacturing" and "wind turbine manufacturing" were considered and dropped. |
| v2.1 | 31 October 2026 | 154 | Removed "secure electricity", "safe electricity", "stable electricity" and "safe and stable electricity" (energy security). In the 155-row human round-2 sample they produced 9 of the 12 energy-security false positives (grid-operator ads at Vattenfall Eldistribution and Skanska describing ordinary network operation). The decision used the scored rows, so the evaluation report says that the 300-row score includes them. |
| v3 | November 2026 | 169 | Added 15 diversification terms for the redefined channel (sovereign digital capacity): `sovereign cloud`, `digital sovereignty`, `sovereign ai`, `ai gigafactory` (InvestAI and EuroHPC seeds); `sovereign solutions`, `sovereign capabilities`, `sovereign capacities`, `sovereign and sustainable`, `guarantee the sovereignty`, `challenges of sovereignty`, `national sovereignty`, `alternative to american`, `european cloud`, `secure sovereign cloud security` (embedding candidates from the lesjeudis.com board); `data sovereignty` (Lightcast skill review). These are recall terms: many hits are defense or cybersecurity employer boilerplate, and the tagger decides. |
| v4 | November 2026 | 182 | Added 13 named sovereign-cloud operators, standards and initiatives (provider review): `s3ns`, `eucs`, `secnumcloud`, `numspot`, `scaleway`, `bleu`, `stackit`, `cloud temple`, `delos cloud`, `gaia-x`, `cloud de confiance`, `eurostack`, `aleph alpha`. `bleu` matches only capitalised "Bleu" with a cloud context within 60 characters, so the colour and French names are excluded. |
| v5 | November 2026 | 184 | Added `outscale` and `ovhcloud` (European-owned cloud providers). A posting at these employers is coded at employer level when the provider is the employer (author's coding decision, prompt v12). |
| v6 | November 2026 | 187 | Named-project terms: `stegra` and `hybrit` (energy security; Stegra counts together with Boden, every HYBRIT mention counts) and `northvolt` (battery cell production, a fixed reshoring sector). In jobbland the added terms flag 151 (Stegra) and 48 (Northvolt) postings and none for HYBRIT. |
| v7 | November 2026 | 188 | Added `iris²` (variants `iris2`, `iris squared`; reshoring, because space is a fixed reshoring sector). It matches "IRIS²" and "IRIS2" but not the word "iris". It flags postings on lesjeudis.com only. |

## Terms by channel

| Channel | v2.1 | v3 | v4 | v5 | v6 | v7 |
|---|---:|---:|---:|---:|---:|---:|
| defense | 68 | 68 | 68 | 68 | 68 | 68 |
| trade compliance | 36 | 36 | 36 | 36 | 36 | 36 |
| diversification | 3 | 18 | 31 | 33 | 33 | 33 |
| reshoring | 20 | 20 | 20 | 20 | 21 | 22 |
| energy security | 14 | 14 | 14 | 14 | 16 | 16 |
| critical materials | 13 | 13 | 13 | 13 | 13 | 13 |
| **Total** | **154** | **169** | **182** | **184** | **187** | **188** |

## Candidates that were not added
- `lexicon_candidates_projects.csv` and `lexicon_candidates_swedish_projects.csv`: project and firm names considered for named-project rules. Only Stegra, HYBRIT and Northvolt entered (v6). The firm watchlist (`firm_watchlist_candidates.csv`) is not part of the lexicon; it is used only as an upper-bound sensitivity indicator.
- `lexicon_candidates_trade_rules.csv`: 7 terms for postings that name the new trade rules themselves (tariffs, sanctions, export controls and similar). They were probed on the full corpora and none was added. A deterministic "needs a new-rules term" filter for trade compliance was also rejected because it would have removed postings the author wants kept.
- No Swedish terms were added for the sovereignty-wording indicator; the lexicon is English only. The Swedish terms of the first draft were dropped when the corpus slice was restricted to English.
- The brief asks for 300 to 500 terms. The lexicon has 188 because only candidates approved by the author entered; the unapproved expansion candidates are in `proposals/`.

## Rules that are not lexicon edits
Each rule keeps the model's own answer next to the corrected one (`*_model` columns or `model_*`), so every change can be undone.

| Rule | Script | What it does |
|---|---|---|
| EU-anchored critical materials | 71 | A `critical materials` tag stays only if a matched term is tied to the EU lists (critical raw materials, rare earths, strategic raw materials, battery materials, lithium, raw materials security, critical metals, strategic resource, battery recycling). Otherwise it becomes none. Applied to the v9 run and, as a separate step after R0 to R3, to the v12 tags (jobbland.se: 27 of 35 critical-materials tags became none, mostly on "mining and mineral"; output files `*.r71.post.jsonl`). A removed tag becomes none, not reshoring. |
| Manual review | 86, 87 | The 4 jobbland.se postings with a Northvolt or battery-manufacturing term that script 71 had set to none were read by the author and labelled reshoring, high (battery-factory roles). Script 87 applies the labels; the earlier tag stays in `channel_before_manual` and the rule field reads `no_eu_anchored_term; manual_review`. |
| Doctoral defense | 75 | The term `defense` is ignored when every occurrence in the posting belongs to the defense of a doctoral thesis ("public defense", "thesis defense"). 27 postings affected in jobbland, all reviewed. |
| R0 | 82 | An invalid answer whose raw text names `sovereign-cloud` becomes diversification, subtype sovereign-tech, with the stated intensity. The parser in script 58 also maps the strings "sovereign-tech", "supply-side" and "sovereign-cloud" to diversification with the right subtype. |
| R1 | 82 | A supply-side diversification tag is kept only if the evidence or the posting text has explicit diversification wording (dual or multiple sourcing, alternative suppliers, reduced dependence, nearshoring, free trade agreement, new export markets, single or sole source). Ordinary purchasing becomes none. It removed 20 postings in jobbland (19 with subtype supply-side, 1 with no subtype), 1 in jobs.de. |
| R2 | 82 | A posting that names SecNumCloud or EUCS and that the model tagged none or trade compliance becomes diversification (sovereign-tech). Intensity is high when the sentence naming the standard holds a duty verb (ensure, obtain, audit, maintain, implement and similar) and the standard is one of at most two items; a company paragraph keeps the model's intensity; everything else is low. The high rule is the author's definition (the work is making sure the company is in line with the standard). The list-size condition is the analyst's and was not tested separately. |
| R3 | 82 | A sovereign-tech tag whose evidence is a tool list (three or more items, no work verb) and whose terms are only providers becomes none. |

## Notes on use
- Lexicon precision (the share of flagged postings that are about a channel) was 0.71 on round 2 and 0.62 on round 1. Most errors come from words that the lexicon matches in postings about something else (see the evaluation report).
- Terms with a note starting "ambiguous" are recall terms: the tagger decides whether the posting is about the channel.

Note on R1: it also checks a diversification tag with no subtype, unless the posting shows sovereign-sector wording (added 8 November 2026 after one such tag on jobbland.se, a purchasing role).
