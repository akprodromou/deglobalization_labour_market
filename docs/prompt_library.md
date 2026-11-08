# Prompt template library: LLM classification of deglobalization postings

All prompts are in `prompts/tagging_v1.txt` to `tagging_v12.txt`. Every file has two parts, `### SYSTEM` (the instructions) and `### USER` (the template filled for each posting). Version 12 is the production prompt; v9 was the production prompt of the first full run on jobbland.se.

## How a prompt is used
- **Flagging first.** A posting is sent to the model only if it contains at least one term of the lexicon (188 terms in lexicon v7). A term is a reason to look, never a reason to assign a channel.
- **User template (all versions):**
  `Job title: {title}` / `Terms from the lexicon found in the posting: {terms}` / `Posting text (may be shortened): {text}`
- **Text sent:** the title, the first 3,000 characters of the description (employment boilerplate about total defence, security checks and similar is removed first) and, when a matched term lies further in, up to three passages of about 500 characters around it.
- **Answer:** JSON with `channel` (reshoring, defense, critical materials, energy security, trade compliance, diversification, none), `intensity` (high, medium, low, none), `evidence` (a short quote) and, from v12, `subtype` (`supply-side` or `sovereign-tech`, only for diversification). Temperature 0, fixed seed. An invalid answer is retried once, then stored as invalid and scored as wrong.
- **Rules after the model.** Script 71, critical materials: a critical-materials tag is kept only if the posting contains a term tied to the EU lists (critical raw materials, rare earths, strategic raw materials, battery materials, lithium, raw materials security, critical metals, strategic resource, battery recycling); otherwise it becomes none (applied to the v9 run and to the v12 tags as a separate step after R0 to R3; on jobbland.se it removed 27 of 35 tags). Script 75 ignores the term "defense" when it only means the defense of a doctoral thesis. Script 82 (rules R0 to R3) corrects four failures of the 7B model on the v12 diversification rules: invalid answers naming `sovereign-cloud` (R0), ordinary purchasing tagged supply-side diversification (R1), SecNumCloud or EUCS mentions tagged none or trade compliance, with intensity set by the sentence that names the standard (R2), and providers named only in a tool list (R3). The model's own answer is kept beside each corrected one. The details are in `lexicon_change_log.md`.
- **Models:** Qwen 2.5 7B through Ollama (production; scored on v6, v8, v9 and v12; jobbland.se was first tagged with v9 and re-tagged with v12, lesjeudis.com and jobs.de with v12). Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) through the API as a benchmark on v6 and v7 only.

## Versions: what changed and why

| Version | Change | Purpose (read from the change itself) |
|---|---|---|
| v1 | Six channels with short definitions, intensity high, medium, low by how central the channel is, JSON answer with evidence. | Starting point from the brief's channels. |
| v2 | Specific cases that decide intensity: a sector named in the company description is low at most; support work at an armed-forces body or defence company is low; routine customs and shipping paperwork is trade compliance, low; staffing firms are judged by the client's role; a word in another sense is none. "When unsure choose the lower intensity." | Stop high intensity for any defence or logistics employer and stop general words from triggering a channel. |
| v3 | Only the subjects named in the channel definitions count (an energy, aerospace or mining employer is not enough); mission statements count as company description; Swedish "total defence" notices are none; routine freight and customs work is none, trade compliance only when compliance duties are explicit; routine purchasing is none. | Reduce false positives from the employer's sector and from boilerplate. |
| v4 | Power-plant building and selling electronic components are none; "arms and legs"; the model must check that its quote is about the channel's subject. | Reduce false positives in energy and semiconductor roles. |
| v5 | Channels reworked: reshoring is production or sourcing nationally in strategically important sectors (space, aerospace, semiconductors and electronic components, batteries); energy security includes building and operating generation capacity, storage and the grid; critical materials includes mining and processing; defense includes armed-forces bodies; intensity by the role's own work (core work high, supporting work medium, corporate functions low). | Channel definitions reworked to the sectors and roles the project cares about. |
| v6 | Customs authority work counts as trade compliance only when the duties involve trade rules. | Keep border enforcement and general customs administration out of trade compliance. |
| v7 | Added a decision order (duties first, then channel conditions, then intensity); trade compliance means the role is responsible for compliance, with a list of things that are none; "a lexicon term is only a reason to look"; high intensity only when most duties are the core work. | Reduce over-tagging: most flagged postings should be none. |
| v8 | Reshoring defined as firms moving production back from abroad, with the sectors fixed in advance; manufacturing of wind and solar equipment is energy security, never reshoring. | Reshoring as defined by the author; separate reshoring from energy security. |
| v9 | Critical materials defined by the EU lists of Regulation (EU) 2024/1252 (strategic and critical raw materials); iron ore, steel, gold, silver, zinc, lead and general mining are none; platinum-group metals count. | Supervisor-approved EU definition; with v8 the model labelled iron-ore mining as critical materials. |
| v10 | Diversification redefined: reducing dependence on a single supplier, country or technology provider (diversified supplier base, dual sourcing, free trade agreements, new export markets) or building domestic or European capacity in strategic digital technology (sovereign AI, sovereign cloud, AI compute, European supercomputing). Cybersecurity work is never diversification. Reshoring excludes diversifying suppliers without moving production. | Cover the sovereign-technology initiatives (InvestAI, EuroHPC) and the lesjeudis.com board; before v10 the channel was only trade-market opening. |
| v11 | "Pure cybersecurity" (SOC, pentesting, vulnerability management, CISO duties) replaces "cybersecurity" as the exclusion. Building, running, securing or selling a sovereign cloud or AI platform is diversification, and so is any role at an employer whose service is sovereign or European cloud or AI; intensity by how close the duties are to the service. A sentence about "sovereign solutions" in a security, IT-services or defence company paragraph does not count. | Count developers and engineers at sovereign-cloud providers, keep general security roles out. On the 620 annotated jobbland postings v11 tagged seven ordinary purchasing postings as diversification. |
| v12 | Diversification split into two subtypes, `supply-side` and `sovereign-tech`, with a `subtype` field in the answer. Named sovereignty-first operators (S3NS, Bleu, NumSpot, STACKIT, Cloud Temple, Delos Cloud, Be Ys Cloud) and the European providers Outscale, Scaleway and OVHcloud count at employer level when they are the employer; a provider inside a tool list is none; a public body counts when digital sovereignty is its stated mission. A SecNumCloud or EUCS mention in a role is diversification, low, and never trade compliance; security and hosting standards (ISO 27001, HDS) and third-party data-protection due diligence are not trade compliance. Supply-side needs explicit dual or multiple sourcing, alternative suppliers, a single source replaced or a move away from one country; ordinary supplier management is none. Named-project rule for energy security: HYBRIT, or Stegra together with Boden. | Fix the 7B model's over-tagging of purchasing (v11), count European-cloud employers, separate the two kinds of diversification so they can be reported separately. The 7B model did not follow three written rules, so R0 to R3 apply them after the model. |

## Scores by version
Round 1 is 472 postings labelled by the author under annotation guide v6 and lexicon v1; weighted F1. Round 2 is 300 postings, human-labelled, scored with the full-text check. Scores for v1 to v5 were not kept in the result files.

| Prompt and model | Sample | Defense | Energy security | Reshoring | Critical materials | Macro-F1 |
|---|---|---:|---:|---:|---:|---:|
| v6, Qwen 2.5 7B | Round 1 | 0.87 | 0.82 | 0.50 | 0.82 | 0.56 |
| v6, Claude Haiku 4.5 | Round 1 | 0.92 | 0.84 | 0.81 | 0.90 | 0.65 |
| v7, Claude Haiku 4.5 | Round 1 | 0.92 | 0.79 | 0.84 | 0.89 | 0.66 |
| v8, Qwen 2.5 7B | Round 1 | 0.87 | 0.76 | 0.44 | 0.72 | 0.53 |
| v9 + rule, Qwen 2.5 7B (158-term lexicon) | Round 1 | 0.85 | 0.68 | 0.52 | 0.18 | 0.44 |
| v9 + rule, Qwen 2.5 7B (154 terms, PhD rule) | Round 1 | 0.85 | 0.61 | 0.52 | 0.18 | 0.43 |
| v9 + rule, Qwen 2.5 7B (154 terms, PhD rule) | Round 2, 300 rows | 0.88 | 0.62 | 0.03 | n=1 | 0.30 (artifact, see below) |

Reading the table
- **Round 1 versus round 2.** Round 1 was labelled under guide v6 and drawn under lexicon v1, round 2 under the current guide. Scores of the two rounds are not comparable channel by channel.
- **Haiku against Qwen.** Haiku 4.5 scored higher than Qwen on prompts v6 and v7 (macro-F1 0.65 and 0.66 against 0.56). Qwen is the production tagger because it runs locally at no cost; Haiku on the final prompt is future work.
- **Stricter prompts lowered recall.** From v6 to v9 Qwen's energy-security F1 on round 1 falls from 0.82 to 0.68, and to 0.61 after the removal of four electricity terms. The prompts became stricter about what counts; probably the round-1 labels, made under guide v6, count more roles as energy security. This was not checked.
- **Critical materials after v9.** The fall from 0.72 to 0.18 is most likely due to the EU definition, which excludes most of the mining postings that round 1 had labelled critical materials; only 11 postings in the corpus are tagged with it.
- **Macro-F1 of round 2** is an artifact of channels with one to eleven postings and is not a result.
- **Intensity** is the weakest part: quadratic-weighted kappa 0.61 on round 1 and 0.31 on round 2.

## Scores of the final prompt (v12)
- **620 annotated jobbland.se postings** (round 1 and the labelled part of round 2; labelled under earlier guides), F1 per channel, one channel against the rest. No channel falls by more than 0.03 against v9. Exact channel agreement 480 of 620 for v12 against 466 for v9; invalid answers fall from 3 to 0.

| Channel | F1 v9 | F1 v12 |
|---|---:|---:|
| Defense | 0.80 | 0.85 |
| Energy security | 0.71 | 0.69 |
| Reshoring | 0.47 | 0.51 |
| Critical materials | 0.69 | 0.74 |
| Trade compliance | 0.51 | 0.50 |

- **Diversification, 79 labelled lesjeudis.com postings, with rules R0 to R3:** precision 20 of 21 (0.95), recall 20 of 24 (0.83), exact channel agreement 65 of 79, intensity exact on 15 of 20. Optimistic: the rules were designed on these postings. The 620 jobbland postings hold only 2 diversification labels.
- **Defense on lesjeudis.com:** weighted precision 0.54 (95% interval 0.41 to 0.67) on a blind sample of 58 postings: 0.70 for high intensity, 0.42 for medium, 0.21 for low. Defense counts on that board are read for high and medium intensity only. No defense precision sample was labelled for jobbland.se (v9 F1 0.88 on round 2) or jobs.de (13 postings).
- Intensity remains the weakest part of the output (kappa 0.31 on round 2).

## Reusing the prompts
- Keep the SYSTEM part unchanged and fill the three USER fields. Change the channel definitions only together with the annotation guide (`tagging_annotation_guide.md`), because the labels were made against it.
- Re-score with script 60 after any change to a prompt. A change that helps one channel has lowered another in this project (v8 to v9). After a change to the diversification or trade-compliance wording, run script 82 again on the saved answers: its rules depend on the wording of the prompt.
