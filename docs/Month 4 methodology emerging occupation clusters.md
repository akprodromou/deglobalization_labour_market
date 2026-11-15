# Month 4 methodology: emerging occupation clusters

Nov 10, 2026 · @anton

Month 4 clusters job titles, and titles plus skills, to find emerging occupations in the three boards, then measures their volume and regional concentration. This page records the method and the decisions taken so far; it is a working draft.

## Status and decisions

Month 3 is finished and the supervisor approved moving to Month 4. The brief: embed job titles (multilingual-e5), cluster them (HDBSCAN, with UMAP for validation and a k-means ablation), check the clusters against seven named occupations, then build quarterly volume series, regional Herfindahl Hirschman Index (HHI)[^bignote] and an Occupation Emergence Rate per cluster.

[^bignote]: The HHI (Herfindahl–Hirschman index) is a number between 0 and 1 that shows how concentrated postings are. For each region (or employer), it takes its share of the cluster’s postings, squares each share, and adds them up. It is near 0 when postings are spread over many regions and equals 1 when they all sit in one. For example, if 3 regions hold 50%, 30% and 20% of a cluster’s postings, the HHI is 0.25 + 0.09 + 0.04 = 0.38; if all postings were in one region it would be 1.


**Deliverables.** A validated set of 6 to 10 emerging occupation clusters (they need not be the seven named), quarterly volume series, HHI per cluster and region, and the emergence-rate series.

**Named occupations to look for:** trade compliance officer, supply chain resilience analyst, semiconductor process engineer, battery cell technician, critical materials specialist, export control specialist, reshoring program manager. We report which are found and do not force them.

**Decisions taken in Month 4**

- Baselines are defined as the periods preceeding specific events, for two boards: AccelerateEU (22 April 2026) for jobbland.se, InvestAI (11 February 2025) for lesjeudis.com,.
- Weighted shares only; the boards are never merged.
- Postings are mapped to NUTS-2 using a script, where the NUTS-2 field is not provided in postings; vague locations are dropped from HHI and their share is reported.
- All postings are clustered first. The flagged share (of emergent occupations) and channel mix come afterwards from the Month 3 tags.
- For the emergence threshold, we tried 100 and 40 postings per quarter per board, plus a share-based version. Quarters rather than a full year suffice.
- We cluster all postings of each board with two different inputs and compared them. Both use multilingual-e5 embeddings, UMAP and HDBSCAN, with a k-means ablation and three seeds per run.
    - Input A: It only uses the job ad title. We run script 90 (`90_prepare_titles.py`) to clear any gender markers, reference codes, employer and place suffixes, so that the posting title refers only to the role.
    - Input D: We use the same (cleaned) title embedding plus (i) ESCO skills extracted from the full posting text; skills are extracted using ESCOX at a threshold of 0.6, and (ii) a Lightcast phrase block of 135 terms, which were selected from the online [Lightcast Skills Taxonomy](https://lightcast.io/taxonomies/skills-taxonomy/categories). The reason is that, by examining the job titles, it was evident that alone they do not define the actual role of an ad, so a way to add the actual skills was deemed a valuable alternative. Duties usually appear further down in postings, so e.g. truncated views are not enough. Running script 69b (`69b_extract_skills_full.py`), we added ESCOX skills to 98% of jobbland.se postings. For Lightcast terms, we ran script 91 (`91_lightcast_phrase_block.py`) and added skills to 2.1%, 5.4% and 1.2% of postings to lesjeudis, jobbland and jobs.de postings, respectively.

## Update of 13 November: results, candidates and conclusion

**Where Month 4 stands.** No validated emerging occupation cluster has been found on the three boards. The 6 to 10 clusters chosen by size and flagged share, the selection step (c) in the plan sent to the supervisor, can still be delivered with their series, HHI and a verdict on emergence; none of them shows validated emergence. Two lesjeudis candidates (clusters 68 and 139) were tested against employer mix and coverage and do not hold. What the data do support is a defence-flagged engineering and cybersecurity core on lesjeudis that nvertheless results from postings of three or four employers, a flagged footprint that moves between employers over time, and the seven named occupations as counts below ten postings each. The numbers under "Results so far" and in the first cluster series below come from the first clustering, before title cleaning and title inference, and are superseded by this section.

**Titles.** Title cleaning (script 90) has a second stage: lead-in sentences, contract, hours and date fillers, references and addresses, trailing places and, on boards where capitalised words are under 55% of title words, an employer tail ("for", "to", "at", "till", "för", "hos", "chez" followed by a proper name). The first stage had left place and employer words in many titles, and the first clusters formed around them. The 1,389 title-less jobbland postings (December 2025 to January 2026) got an inferred title from the description with Qwen 2.5 7B (script 99). On a manual check (i.e. human classifier on a sample), 88% of inferred titles named the same occupation as the real one (Wilson 95% interval 80% to 93%). 1,385 postings got a title and 4 stay without one (UNKNOWN). Clusters 171 and 168 of the first run no longer exist.

**Reclustering.** Input A was rerun on the cleaned and inferred titles: jobbland.se 357 clusters (34.3% noise), lesjeudis.com 144 (30.9%), jobs.de 71 (27.6%). Input D gave 358, 139 and 80 clusters (35.2%, 28.9% and 29.5% noise) but is not used for selection, because D v1 is withdrawn.

**Named occupations, checked directly on jobbland (script 101).** The regexes were corrected after the first check produced false matches: solar-cell sellers matched "battery cell technician" (11 of 17 hits), "individual users" matched "dual use", and "Raw Material Manager" matched critical materials. After the correction, jobbland holds 5 trade compliance titles, 7 genuine export control titles (a further hit is a customs course code), 6 battery cell titles, 1 supply chain resilience hit (a doctoral student post, not an occupation) and none for semiconductor process engineer, critical materials specialist and reshoring program manager. A cluster needs 40 postings, so none of these can form one; they are reported as counts by quarter. The earlier check of lesjeudis and jobs.de found 0 to 1 per occupation and was not rerun after the pattern fix.

**Named occupations, second route: seed skills (script 108).** To test whether the seven occupations are better found through skills than through titles, we took, for each occupation, the ESCO skills that describe it (found in `lexicon/skills.csv`) and the matching Lightcast terms, and counted the postings that carry any of them. Four occupations have specific ESCO skills: trade compliance (customs compliance, customs law, import-export regulations and licences), export control (export control principles, export regulations of dual-use goods, embargo regulations), semiconductor process (wafer cleaning and polishing, photolithography, semiconductor testing) and battery cell (battery formation and conditioning, battery chemistry, battery components, battery test equipment). Supply chain resilience has only generic supply chain skills, critical materials only "materials engineering (battery material)" and "implement mineral processes", and reshoring program manager has no ESCO skill. The idea follows the seed-skill indicator of Dawson, Williams and Rizoiu (2021), who start from a few seed skills and follow the skills that co-occur with them.

| Occupation | By title regex (jobbland / lesjeudis / jobs.de) | By seed skills or Lightcast terms | Of these, titles that hold the occupation (reading of titles) |
| --- | --- | --- | --- |
| Trade compliance officer | 5 / 0 / 0 | 41 / 4 / 10 | about 18 / 0 / 5 |
| Export control specialist | 8 / 3 / 1 | 5 / 4 / 0 | 0 / 0 / 0 |
| Semiconductor process engineer | 0 / 1 / 2 | 18 / 2 / 7 | 0 / 0 / 4 (optoelectronics and semiconductor development) |
| Battery cell technician | 6 / 0 / 0 | 51 / 1 / 2 | about 8 / 0 / 1 |
| Supply chain resilience analyst | 1 / 0 / 0 | 456 / 517 / 21 (generic skills) | not meaningful |
| Critical materials specialist | 0 / 0 / 0 | 82 / 14 / 13 | seed unusable |
| Reshoring program manager | 0 / 0 / 0 | no seed | none |

Skills find more postings than titles do, but most are false matches or topic mentions, not the occupation. Reading the titles of the carriers, only trade compliance has a group of real role-holders (about 18 on jobbland and 5 on jobs.de), and these are mostly customs clearance and freight forwarding, an established occupation; three jobbland titles are trade-governance roles (Global Trade Program and Systems Governance Manager, Trade Compliance Officer, Export Control Manager), all dated September 2025 or later, which is too few to read as a trend. The export control skills produced no title of an export control role. The semiconductor carriers on jobbland include none that is a process role and half share the skill "monitor satellites", which suggests a space or optics employer's template; on jobs.de four of seven are in optoelectronics or semiconductor development. Battery carriers include about eight engineering or production roles on jobbland, seven research posts and several salespeople and electricians. The seeds for supply chain and critical materials give false matches (for example "implement mineral processes" on IT and finance roles) and are not used. A seed marks a topic, not a role, and the extraction has false matches, so these counts are upper bounds. The skill-seeded variant is not pursued as a series; the counts are reported as a second check on the named occupations, which agrees with the title search: the occupations are present only in handfuls.

**Emergence by board.**

- **jobbland.se.** Weighted postings per quarter swing from 727 to 166,360, so quarterly crossings follow coverage. For example, assuming a cluster that is always 0.1% of the board’s postings:
    - In a quarter that has 727 weighted postings, its postings are 0.1% × 727 = 0.7 postings. That is below the threshold of 100.
    - In a quarter with 166,360 weighted postings, it counts are 0.1% × 166,360 = 166 postings. That is above 100, so it “crosses”.

The monthly run from 2026-02-01 to 2026-08-31 around AccelerateEU (22 April 2026) lists "clearly new" clusters that are cleaners, preschool staff, concrete workers and doctors, none flagged. Samples of the flagged clusters with a rise (291 quality engineer, 263, 232 production technician, 350 systems engineer) show consultancy staffing patterns that exist from 2024, or 6 postings in total (263). No candidate.
- **jobs.de.** Three usable quarters. The 28 "new" crossings in 2024-Q4 are the board starting up, and the rise of the electronics cluster from 1.01% to 11.75% compares a partial first quarter with a thin last one. No emergence evidence; the board is used for validation only.
- **lesjeudis.com.** Clusters 68 (embedded software, aeronautics and defence) and 139 (cybersecurity) are "clearly new" [^2] in 2025-Q2 (monthly: 2025-05), with 57% and 38% of postings flagged at medium intensity or higher and event changes of +0.63% (+0.20 to +1.21) and +0.96% (+0.42 to +1.79) around InvestAI. The monthly series shows both already above the line in 2024-08, and cluster 139 peaks in 2024-08 (2.29%). Flagged postings per quarter (2024-Q3 to 2025-Q3) are 22, 5, 2, 15, 15 for cluster 68 and 13, 5, 1, 12, 8 for cluster 139. The "new" status comes from comparing with 2025-02 (16 sampled days), the last usable month before a coverage gap (2025-03, 2025-04 and 2025-07 are unusable). In reality, the clusters had been above the threshold before; they didn’t appear for the first time. The largest clear rises (Product Owner 0.59% to 4.52%, data analysts) are not flagged and reflect IT and data roles gaining share on the board.

[^2]: A cluster is “clearly new” in a month if its whole interval is above the threshold now, and its whole interval was below the threshold in the previous usable month.

**Flag intensity.** The flagged share counted every tag, including `low`, which the annotation guide gives to a role whose duties are outside the sector and where the sector appears only in the company text. However, since we are examining emerging occupations with respect to their role and duties in the context of deglobalization, they should be disregarded. For this reason Script 93 was adjusted to only filter `--min-intensity medium` and `high`. Cluster 117 (head of IT project) falls from 34% to 11% flagged and drops out; clusters 68 (60% to 57%) and 139 (43% to 28%) hold. Script 98 now prints the intensity of each flagged posting.

**Employer concentration (script 103).** The employer field is empty on lesjeudis, so we used a script to take the employer namen from known names in the first 1,500 characters of the description (Thales, Sopra Steria and CS, Safran, Alten and about 35 more; 1 to 19 of 19 to 78 postings per cluster are unmatched). Flagged postings at medium intensity or higher:

| Cluster | Title | Flagged postings | Effective employers | Largest employer share |
| --- | --- | --- | --- | --- |
| 99 | Program manager | 27 | 1.1 | Thales 96% |
| 33 | IVVQ engineer | 67 | 1.2 | Thales 92% |
| 61 | Software architect | 28 | 1.3 | Thales 88% |
| 107 | Engineering manager | 43 | 1.3 | Thales 86% |
| 127 | Systems engineer | 34 | 1.8 | Thales 72% |
| 56 | Software architect, defence and security | 27 | 2.3 | Sopra Steria 58% |
| 133 | AI engineer | 19 | 2.3 | Thales 62% |
| 67 | Software validation engineer | 36 | 2.6 | Thales 54% |
| 130 | Electronics engineer | 102 | 2.8 | Thales 56% |
| 68 | Embedded software engineer | 78 | 3.3 | Thales 42% |
| 139 | Cybersecurity engineer | 48 | 3.9 | Thales 41% |

To discuss the findings on employers, we will use the concept of ``Effective employers''. This is a standard transformation of the Herfindahl–Hirschman Index and is equal to 1 divided by the sum of squared employer shares. For example, if one employer holds 96% of a cluster’s postings and the rest is spread thinly, Σs² is ~0.92, so the effective number is about 1/0.92=1.09. That can be interpreted as “the cluster behaves as if it had one employer”.. Over the whole board, Thales rises from 3.5% of all postings taken in 2025-Q1 to 7.0% in 2025-Q2 and 9.0% in 2025-Q3, and its flagged postings from 95 to 198 and 257, while Sopra Steria and CS flagged postings fall from 129 (2024-Q3) to 33 (2025-Q3):

| Quarter | Thales share of postings taken | Thales flagged postings | Share of all flagged postings |
| --- | --- | --- | --- |
| 2024-Q3 | 4.7% | 134 | 30% |
| 2024-Q4 | 4.0% | 201 | 44% |
| 2025-Q1 | 3.5% | 95 | 34% |
| 2025-Q2 | 7.0% | 198 | 49% |
| 2025-Q3 | 9.0% | 257 | 56% |

The clusters that first cross the line in 2025-05 to 2025-08 (33, 67, 99, 107) are the Thales-dominated ones. Counts are postings taken, not weighted, so shares are compared and not counts. The data cannot say whether Thales posted more or the board covered it better from 2025-Q2.

**Conclusion.** Under the criteria used (clearly new or a clear rise in share, at least 25% flagged at medium intensity or higher, coherent content, not an employer pattern), no cluster is validated as an emerging occupation. Reported instead: (1) the named occupations as counts; (2) a lesjeudis defence-flagged core that is concentrated in a few employers, with five clusters that are employer patterns (33, 61, 99, 107, 127) and the rest of the core (56, 67, 68, 130, 133, 139) too concentrated or too flat to call emerging; (3) declines of defence-flagged IT and systems clusters after InvestAI (137, 126, 136, 116), read with the coverage gap; (4) the negative results for jobbland.se and jobs.de; (5) the intensity filter and the employer check as methods. The thesis calls the flagged clusters "concentrated in a few employers" and does not call them emerging.

**Options for Month 5, to agree with the supervisor.** Cluster only the flagged postings with a smaller minimum cluster size (about 20), which can separate small occupations but depends on the tagger by construction. A series that caps any single employer's share. Ask Skillab, through the supervisor, whether sources or employer coverage changed in 2025.

**Supervisor guidance not yet applied.** From the earlier exchange on weights, clustering and HHI:

- **Weights.** Normalise the weights to \[0, 1\], possibly with a logarithm, so that very large weights (for example 200 on a high-volume day) do not dominate. The inverse-probability weight is the unbiased estimator of the population share, so it stays the main estimate. Script 93 now has `--weight-mode log` and `--weight-mode cap` to rerun the shares and intervals as a sensitivity check; the verdicts on the candidate clusters are then compared across the three modes.
- **Number of clusters.** The supervisor found 256, 141 and 79 clusters too many and asked for 3 to 4 clustering algorithms compared by silhouette score. The current runs give 357, 144 and 71 clusters on input A and no algorithm comparison by silhouette has been made. The silhouette is computed on the non-noise points of each method, and HDBSCAN noise has to be reported next to it.
- **Preserving specific clusters.** The supervisor suggested intervening in the clustering to keep chosen clusters, based on the distances between them. A seeded variant (titles of the seven named occupations and of the flagged clusters as fixed centres, postings assigned within a cosine distance) would also catch occupations with fewer than 40 postings, which HDBSCAN cannot form.
- **Lightcast weight.** The Lightcast block should have the same weight as the ESCO block; D v1 used 0.5 and 0.3. D is withdrawn and is not used for selection, and D v2 should use equal weights.
- **HHI and the thesis question.** The supervisor reads the index as a measure of how far specific domains dominate a market, and the aim as quantifying how far larger markets are more or less similar to smaller ones in the composition and concentration of their skill sets. The employer concentration reported above fits this reading; what "larger and smaller markets" refers to (boards, countries or clusters) is to be confirmed.

## Supervisor answers of 14 November, and what each decision means

The supervisor answered the four questions of the email. Option A is adopted: the 6 to 10 clusters are described as concentrated, flagged occupation clusters, and emergence is reported as a finding for each cluster. The notes below explain each decision in plain words, with the example used in the discussion.

**1. Option A or Option B (how the 6 to 10 clusters are chosen).** Option A selects clusters by size and flagged share (step (c) of the plan the supervisor approved) and then reports for each one whether it is emerging. Option B makes emergence the selection rule, so only clusters that pass the emergence test are delivered. Example: lesjeudis cluster 33 (embedded software, Thales at about 42% of its postings) is large and strongly flagged, so it is selected under A, with the finding "present since 2024-08, concentrated in 3 to 4 employers, not emerging". Under B it is dropped, and since no cluster passes both the emergence test and the flag test, B delivers zero clusters. The only cluster with a clear rise on lesjeudis is cluster 3 (Product Owner), which is not flagged, so under B it would be the only cluster "in", although it has nothing to do with deglobalization. A keeps the deliverable and keeps the negative result visible.

**2. Inverse-probability weights as the main estimate.** The collection takes about 100 postings from one page per calendar day, so a posting stands for (day total / postings taken that day) postings. Example: a day with 1,000 postings of which 100 are taken gives each posting weight 10; a day with 200 postings of which 100 are taken gives weight 2. Without weights the quiet day counts as much as the busy day. The weights are the only way the sample is unbiased for the whole board, so they stay the main estimate. They also make the quarterly totals swing (jobbland 727 to 166,360 weighted postings), because a few days carry very large weights. Two sensitivity runs test this: log-scaled weights (log(1+w), so a weight of 1,000 counts about 3 times a weight of 10, not 100 times) and capped weights (cut at the 95th percentile). They trade some bias for lower variance. If a verdict (new, rising, flat) is the same under all three, it does not depend on the weighting; the counts and the 100-postings threshold lose their meaning under log and cap, so only shares and verdicts are compared. The supervisor agreed to re-run and decide from the results.

**3. Silhouette comparison and the seeded variant.** The silhouette of a posting is (distance to the nearest other cluster minus distance to its own cluster) divided by the larger of the two, from -1 to 1. Example: a posting 0.2 from its own cluster centre and 0.6 from the nearest other cluster scores (0.6 - 0.2) / 0.6 = 0.67 (well placed); a posting at 0.4 and 0.45 scores 0.11 (on the boundary). The mean silhouette over the postings of a clustering allows 3 to 4 algorithms (for example HDBSCAN, k-means, agglomerative, HDBSCAN on UMAP) to be compared on the same input, reporting the share of noise next to it, since an algorithm that drops a third of the postings as noise can score high on the rest. The cluster counts (357, 144 and 71) are only a result of one setting and should be fixed by this comparison before the remaining analysis is built on it. The supervisor also notes that titles alone are unlikely to give clusters of emerging occupations, because employers use a general title and put the detail in the description; input D (titles with ESCO and Lightcast skills) addresses this and is compared in the same way. The seeded (constrained) variant is a complementary method: it fixes centres from postings of chosen occupations (for example the titles that contain "export control"), lets a posting join a centre when its cosine distance is under a threshold, and clusters the rest freely. A named occupation then cannot dissolve into a larger cluster, and the question becomes whether the seed grows over time.

**4. "Larger and smaller markets".** The supervisor confirms that markets are the boards or countries: Sweden (jobbland, 53,959 postings), France (lesjeudis, 18,625) and Germany (jobs.de, 12,243). The question is whether the larger board is more or less similar to the smaller ones in the composition (which skills and sectors make up the postings) and the concentration (how much a few of them dominate) of its skill sets. HHI falls as a sample grows, so a large board looks less concentrated for no real reason; the comparison therefore uses equal-size subsamples next to the whole-board value. Composition is compared with a similarity score (Jensen-Shannon, 1 = identical) on the skill and sector labels the boards share. The boards are never merged. This is built in script 104 (docs/boards\_concentration.md): HHI and top-10 share over skills, sectors, clusters, NUTS-2 regions and employers per board, and the same by quarter. The organisation field is empty on all three boards, so employer concentration cannot be computed across whole boards; it is reported only for the clusters checked with script 103.

**Result for question 2 (lesjeudis, monthly, flag intensity medium or higher, log and capped weights; weights rescaled to the same board total).** No verdict changes in a way that matters. The clusters with the largest flagged share are the same under both transformations and under the default weights, and their flagged shares move by at most 2 points (cluster 33: 93% and 94%; 68: 57% and 57%; 137: 49% and 48%; 130: 49% and 48%; 139: 28% and 29%). The clear rise of cluster 3 (Product Owner, unflagged) is the same: 0.82% to 3.65% under log weights, 0.83% to 4.12% under capped weights, clear in both. The “clearly new” lists overlap in five of seven clusters (1, 12, 68, 75, 137). The two that differ are borderline: 139 is clearly new under capped weights only, and 125 (log) and 65 (capped) appear in one transformation only. The count of clearly new clusters per month is the same under both transformations in 2024-11 and 2025-05 (2 and 3). Clusters 68 and 139 are clearly new in 2025-05 under both weightings, but they already crossed the threshold in 2024-08, so this is the effect of the missing March and April 2025 data, not weighting; weighting does not resolve that. The inverse-probability weights stay the main estimate.

**Result for question 4 (script 104, common window 2024-08-01 to 2025-04-09).** The largest board (Sweden) is not the most different from the smaller ones, and concentration does not fall or rise steadily with board size. Skills are the ESCOX skills extracted from the full text (script 69b), the same method for every board and month; the tracker (API) tags are not used, because they are missing on jobbland from mid-2025.

| Board | Skills: effective number (HHI) | Sectors: effective number (HHI) | Regions: normalised HHI |
| --- | --- | --- | --- |
| Sweden (jobbland, largest) | 200 (0.0050) | 62 (0.0162) | 0.052 |
| France (lesjeudis) | 311 (0.0032) | 45 (0.0222) | 0.199 |
| Germany (jobs.de, smallest) | 296 (0.0034) | 91 (0.0110) | 0.019 |

Similarity of composition (Jensen-Shannon, 1 = identical):

| Pair | Skills | Sectors |
| --- | --- | --- |
| Sweden and Germany | 0.79 | 0.89 |
| Sweden and France | 0.71 | 0.85 |
| France and Germany | 0.64 | 0.80 |

Sweden is the most concentrated in skills, France in sectors and regions (Île-de-France), and Germany the most diffuse in sectors and regions. The largest board is the most similar to both others, and the two smaller boards are the least similar to each other. With three boards, size cannot be separated from country, language and platform, so these are descriptions of the boards, not an estimate of an effect of size. The values are stable across quarters within each board (Sweden skills HHI 0.0044 to 0.0057 over eleven quarters), so the differences between boards are structural, not caused by one period. Equal-size subsamples give the same values as the whole boards, so sample size is not behind the differences. Limits: the sector labels come from the tracker and are filled for about 90% of jobbland postings only up to 2025-05, which is why the comparison uses the common window; the cluster HHI is not compared across boards, because the same minimum cluster size gives 357, 144 and 71 clusters; jobs.de 2025-Q2 rests on 349 postings.

**Order of work.** (1) The log and capped weight runs and the board comparison (script 104). (2) The silhouette comparison of the algorithms for inputs A and D v2, and the seeded variant, on Colab. (3) Fix the final clustering setup, then rebuild the series, HHI and the verdict per cluster.

Re-clustering lesjeudis on D v3 (102 clusters; title coherence comparable to A, ARI 0.53) leaves the emergence picture unchanged: 0 to 2 clearly new clusters per quarter against 0 to 4 in A. The Java cluster is clearly new in both. The DevOps verdict (clearly new in A) disappears because D v3 merges the French and English clusters, which were already above the threshold at the start. The two flagged clusters that are clearly new in A (cybersecurity, embedded software) are not clearly new in D v3. The cybersecurity cluster still rises around the event (+0.86 points, 95% interval +0.23 to +2.12, against +0.96 in A). The embedded software rise is smaller and its interval includes zero (+0.29, -0.07 to +0.85). “Clearly new” for these two clusters is therefore reported as sensitive to the clustering input.

Under the original rule (“wholly below the threshold in the previous quarter”), lesjeudis showed five clearly new clusters (DevOps, Java, sysadmin, cybersecurity, embedded software). Four of them (all except DevOps) were above the threshold in 2024-Q3, dropped wholly below it in 2025-Q1 (5 to 11 postings taken, against 36 to 73 in 2024-Q3) and returned in 2025-Q2. The rule counted that return as emergence. With the stricter rule (wholly below in every earlier quarter) only DevOps remains, and its series is itself a hump: 9, 80 and 91 postings taken in 2024-Q3 to 2025-Q1, then 12 and 12. After the stricter rule, the single remaining clearly new cluster on lesjeudis (DevOps, French-language titles) is explained by one employer: Sopra Steria accounts for 35 of its 91 postings with an identified employer, all of them in 2024-Q4 and 2025-Q1. The cluster has 12 postings a quarter before and after. We therefore find no new occupation cluster on lesjeudis under the methodology as specified.

An employer check (script 103) shows that the 2025-Q1 drop in the Java, sysadmin, cybersecurity and embedded-software clusters is not carried by one employer: the clusters draw on 5 to 10 effective employers, and the drop appears in all of them. The two defence-flagged clusters are the exception in the opposite direction: Thales accounts for 61% of the identified postings of the embedded-software cluster in 2025-Q3 and for 43% of the cybersecurity cluster in 2025-Q2. Their rise reflects one employer’s posting activity as much as a market-wide change. Employer names were found in only 41% to 55% of the postings, so these shares are lower bounds.

## Pipeline

The pipeline runs per board (jobbland.se 53,959 postings, lesjeudis.com 18,625, jobs.de 12,243). Embedding, UMAP and HDBSCAN run on Colab (T4); shares, NUTS-2 mapping and HHI run on the Mac.

1. **Title cleaning** (script 90). Strips employer names, locations, gender markers such as (m/w/d) and trailing reference codes (for example IRC207099 or 2024-112135), and removes frequent trailing segments found by counting suffixes (25 or more occurrences). Segments starting with a digit are never dropped. Changed titles: jobs.de 11,814; lesjeudis 14,535 (78.0%); jobbland 24,625 (46.8%).
2. **Embedding.** Each cleaned title gets the prefix "query: " and goes through multilingual-e5-large (1024 dimensions, L2-normalised). A posting without a title uses the first 150 characters of its description.
3. **Input A** is the title embedding alone.
4. **Input D** concatenates three blocks, each L2-normalised and weighted, then renormalised: the title embedding (weight 1), an ESCO skills block (tf-idf over ESCO skills extracted from the full text, reduced to 100 dimensions with TruncatedSVD, weight 0.5) and a pruned Lightcast block (tf-idf, 20 dimensions, weight 0.3). Postings with no skills get zeros in those blocks, so they are clustered on the title only. The weights are untested defaults; v1 used 1.0 and 0.5.
5. **Clustering.** UMAP to 10 dimensions (cosine, min\_dist 0, n\_neighbors 30), then HDBSCAN (min\_cluster\_size 40, min\_samples 10, eom). Three seeds. A k-means run with the same k is the ablation.
6. **Skills source.** ESCO skills come from script 69b: sentence-embedding matching (all-MiniLM-L6-v2, similarity at least 0.6) over windows of up to 3,000 characters, so duties that appear late in a posting are covered. Lightcast terms come from script 91 and lexicon/lightcast\_block\_terms.csv (629 rows, 135 selected, 16 pruned).

## Results so far

**Cluster counts.** jobs.de gave 79 clusters on A and 109 on D; lesjeudis gave 141 on A and 122 on D. Between 31% and 40% of postings end as noise. Noise is HDBSCAN label -1: a posting that is not in a dense region of at least 40 similar postings. Rare emerging occupations may sit in noise, so the noise share is reported with every result.

**D v1 withdrawn.** An earlier reading that D beats A on internal metrics (relative validity, stability, k-means agreement) was wrong. Those metrics rewarded clusters formed around a single skill, which are artefacts. After reading the cluster reports, D v1 was withdrawn. One cause is false ESCO matches: sentence-embedding similarity above 0.6 can link generic template sentences to unrelated skills, which is how a skill such as "feed concrete mixer" appeared on IT consultant postings (hypothesis; a diagnostic cell was supplied and its output is pending). Another is the Lightcast term "Supply Chain", which is boilerplate on lesjeudis: 351 of 352 postings in one cluster.

**Coherence filter (v3).** Before building the skill blocks, each skill is kept only if the postings carrying it have similar title embeddings. The embeddings are first centred on the board mean, because e5 scores cluster in a narrow high band (the model card says this is expected, from the 0.01 InfoNCE temperature) and without centring every skill looked equally coherent. Coherence is the norm of the mean of unit vectors, compared with five random sets of the same size; the skill is kept when the lift is at least 0.15. This is my own heuristic, not a published method. It was tested on mock and synthetic data only, and the 0.15 threshold and the 0.5/0.3 weights are untested on real data. A published, citable alternative is document-frequency pruning (max\_df) or taking skills from the description only.

**Named occupations.** The seven named occupations are nearly absent from the A and D outputs. The regex matches for "battery" are unverified. We report which are found without forcing any of them into a cluster.

**Status.** Inputs A for all three boards and D v1 are done. The `--coherence-only` reports are the next step (see open items), then D reruns with tag v2.

**First cluster series on input A (script 93, 12 November).**

- **The count threshold follows the board's size, not the labour market.** jobbland's weighted postings per quarter run 727, 5,389, 16,278, 145,266, 87,115, 10,481, 7,493, 33,777, 166,360, 147,642 and 72,636 (2024-Q1 to 2026-Q3). So 174 clusters "newly cross" 100 postings in 2024-Q4 only because the board is 9 times larger than in 2024-Q3. The cause of the 10-fold drop in 2025-Q2 and Q3 is not known. The share version (0.1% of the quarter) is the metric to use; interval-based crossings (the whole interval C above or below the line) are reported next to it.
- **Volume does not select emerging occupations.** 238 of 256 jobbland clusters, 61 of 141 lesjeudis clusters and 53 of 79 jobs.de clusters pass the threshold. The largest are ordinary occupations: nurses, service technicians, teachers, helpdesk technicians, Java developers. None of the seven named occupations appears among them.
- **Candidates must come from flagged share and change.** On lesjeudis the clusters with the highest flagged shares are defense-flavoured IT roles: cybersecurity engineer (62% flagged), embedded software engineer (60%), systems engineer (45% and 42%), AI engineer (28%), information systems security manager (22%). These are candidates, not validated occupations, and their flags rest mostly on the defense channel, whose precision limits are in the Month 3 report.
- **jobs.de cannot support an emergence series.** Three usable quarters, the last with 76 of 90 days, and flagged shares near zero in every large cluster.
- **Two jobbland clusters are not occupations.** Clusters 171 and 168 (peak shares of 16.1% and 5.4% in 2025-Q4) have empty titles, 99% to 100% unplaced locations and recruiting-ad or church-election text. They passed the template check, so a title-less share is now part of eligibility.
- **Change around an event** now compares equal windows (90 days before and from the event) instead of the whole board.

## Thresholds: 40 and 100

Two different thresholds do two different jobs, and they apply at different moments.

- **40 postings (min\_cluster\_size)** decides whether a cluster exists at all. It counts collected postings over the whole period and is applied inside HDBSCAN.
- **100 postings per quarter** decides whether an existing cluster has emerged. It counts weighted, estimated postings in a quarter (not collected ones) and is applied afterwards, per board. A share-based version is run alongside it.

Example: a cluster of 45 collected postings spread over six quarters exists (45 is at least 40). If its weights scale those up to an estimated 130 postings in the latest quarter, it crosses the emergence line in that quarter. A cluster of 30 collected postings is never formed, so it cannot be counted, even if its weighted size would exceed 100.

The Occupation Emergence Rate is the number of clusters crossing the 100-per-quarter line, per quarter and board.

## Time series, weighted shares and uncertainty

**Collection design.** Script 52 does not download every posting. For each calendar day it reads the day's total from the Skillab API, then fetches one random page (about 100 postings; `--per-day`, default 100) of that day. Each record keeps the day total. Requests take 20 to 70 seconds (script 38 docstring), so the sample is probably a cost and speed choice; no line in the scripts states this, so it is my inference.

**Weighted shares.** A posting's weight is the day total divided by the postings taken that day. The share of a unit (a cluster, a tag, a skill) is the sum of the weights of its postings divided by the sum of the day totals. Example: on a day with 1,000 postings of which 100 were taken, each taken posting stands for 10. If 5 of the 100 are in a cluster, the cluster's estimated size that day is 50 and its share is 5%. Without weights, busy days would count the same as quiet days.

**Literature.** This is standard survey-sampling practice: weighting each unit by the inverse of its inclusion probability is the Horvitz-Thompson estimator (Horvitz and Thompson 1952, JASA), and sampling within strata (here days) is covered in Cochran, *Sampling Techniques*, and Lohr, *Sampling: Design and Analysis*. I verified that these references exist; the two textbooks I cite from memory. The scheme assumes the day total is the full population for that day, which holds only if the API count is complete for the day.

**The sample is not the population.** Random sampling within a day is valid only because the day total is known. The weighted population jumps from about 10,000 (September 2024) to about 48,000 (October 2024) on jobbland.se, so early 2024 is not comparable and is flagged. Date coverage from the file names: jobbland.se 2024-01 to 2026-09; lesjeudis.com 2024-08 to 2025-09; jobs.de 2024-08 to 2025-04. Two boards therefore have few quarters.

**Uncertainty.** A bootstrap within each day gives intervals for the shares (Efron 1979; Rao and Wu 1988 for resampling in complex surveys). It treats postings on a page as independent. They are probably not: a page holds adjacent postings in server order and script 52 notes that postings from one day share employers and batches. The within-day bootstrap may therefore understate the variance.

**Is resampling whole days safer?** Not unconditionally; an earlier draft said so too strongly. Resampling days (better, week blocks, because of the weekday cycle) does not rely on independence inside a page, because page clumping shows up in the day-to-day differences, so it is more conservative. But every day is in the sample in a stratified design, so between-day variation is not sampling error in the design-based sense. Day resampling answers a different question (is the change larger than ordinary day-to-day variability, which includes real fluctuation) and may overstate sampling error. Plan: report both intervals, and check employer concentration per page and overdispersion against a binomial. Overdispersion alone cannot separate clumping from real variation.

**Sampling check, first results (script 94, 11 November).** The indicator is the share of postings with any Month 3 flag. Three interval widths are compared per quarter: A redraws postings inside each day, B redraws employers inside each day, C redraws whole ISO weeks.

- **The employer test could not be run.** The employer field is empty on all three boards (jobbland 100%, lesjeudis 100%, jobs.de 99.8% of postings), so B equals A by construction there. On jobbland a proxy was used instead: postings whose first 80 description characters match count as one template. B/A then ranged from 0.96 to 1.33 and was mostly 1.0 to 1.2, so template clumping adds little, with one exception (2025-Q2, 1.33). A proxy catches only template clumping, not employers who write each ad differently. On a few days one template supplies a third of the page (90th percentile 33%).
- **Week-to-week variation is much larger than within-day noise on lesjeudis.** C/A is 2.2 to 2.8 in all five quarters. On jobbland C/A is 0.8 to 1.9 in most quarters, with an outlier of 3.9 in 2025-Q2 (2,010 postings). On jobs.de C/A is 0.7 to 1.2, but the flagged share is only 0.7% to 1.4%.
- **Reading.** The within-day interval alone is too narrow for lesjeudis. The data cannot say whether the cause is clumping or genuine week-to-week change in the flagged share. Week-block intervals also count any trend inside a quarter as noise, so they are conservative for trend detection, and C rests on only 9 to 14 weeks per quarter. Decision for now: report A and C side by side, and use C when judging whether a quarter-to-quarter change is real.

**Sampling check, follow-up on the spikes and gaps (11 November).**

- **jobbland, 14 to 20 April 2025.** 56 of 382 sampled postings are flagged (14.7%), 47 of them energy security. Of the 56, 41 (73%) open with the same sentence of a diversity statement, so they come from one template, probably one employer. The spike behind the wide 2025-Q2 interval is clumping, not a broad rise. The employer is not identified here.
- **lesjeudis has missing days.** Quarters hold 44 to 52 sampled days instead of about 91, and several weeks hold 1 or 2 days. Week-block intervals therefore also mix weekday composition, and the earlier assumption that every day is in the sample holds only for the days collected.
- **lesjeudis, July 2025.** The flagged postings come from many defense employers (Thales, Safran and naval firms among the description openings); the largest template group holds 12%. Late September to early October 2025 has 3.4% flagged (11 of 323), with no group above 9%. The titles give no explanation for the drop; whether those employers stopped posting on the board or the board's mix changed is not known. The lesjeudis flagged-share series is not read as a labour-market trend until this is checked.
- **Template proxy on lesjeudis.** B/A is 1.11 to 1.90 (design effect (B/A) squared, about 1.2 to 3.6), against about 1.0 with the employer field. The proxy is a lower bound: the Thales openings start with a place name that varies, so the 80-character keys split one employer into many groups.
- **Consequence for the method.** Report A and C intervals. Add a template-capped sensitivity: the share recomputed with each template group counted at most a fixed number of times per day. Do not call a one-week jump a trend when one template accounts for most of it.

**Trend method.** For each unit: presence in a posting (not frequency), weighted quarterly share, bootstrap interval, comparison with the baseline as an absolute change and a ratio, a simple slope or before-and-after test, and a read of sample postings. Guards: employer concentration, template text, seasonality, coverage jumps and multiple comparisons.

## Stability of the Skillab database (checks of 12 November)

**Three stages.** The data comes from the Skillab API, not directly from the boards. A posting reaches our sample through three stages: (1) the employer posts it on a board, (2) Skillab ingests it into its database, (3) our script 52 draws one random page of about 100 postings for each calendar day and weights each posting by day total divided by postings taken. Only stage 3 is random and under our control. The weights treat the API's day total as the true population of the day. A weighted share is therefore a valid estimate for what the database holds. It describes the labour market only if stages 1 and 2 are unrelated to the kind of job, and for change over time it is enough that they do not change in a way that depends on the kind of job. The supervisor has told us that the day is the posting's publication date; an ingestion that starts, stops or backfills a source would still change the day totals.

**Coverage regimes.** The weekly weighted population of jobbland (population\_jobbland.csv) is stable in two stretches: 2024-W41 to 2025-W07 and 2025-W50 to 2026-W35, roughly 6,000 to 15,000 postings a week outside holiday weeks. Between them (2025-W08 to 2025-W49) it is mostly under 2,000 a week, with a few spikes up to about 7,000, and before 2024-W19 it is under 700. lesjeudis has no jump of 3 times or more but only 286 of about 415 calendar days sampled, with the gap in 2025-Q1 and Q2. jobs.de has 221 sampled days up to 2025-04-09. A share is compared only inside one stretch of one board.

**Composition-stability test (script 97).** If ingestion changes, the mix of postings should change when the day total jumps. The mix is measured over clusters (script 92), Month 3 channels (six channels and none) and the posting's sector field. The distance is the Jensen-Shannon divergence between two pooled mixes, and both groups are cut at random to the same number of postings before every distance, because the distance grows when a sample is small and groups of unequal size would differ by size alone. The noise floor comes from shuffling whole days between the two groups (a page clumps postings of the same employers, so single postings are never shuffled). Comparisons: (i) low-volume against high-volume days, also inside the same quarter and weekday; (ii) 14 sampled days before against 14 after every jump of the day total of 3 times or more; (iii) the same comparison for stretches with no jump as placebo. 97b prints the cluster-by-cluster difference around one date, and 98 prints sample postings of named clusters.

**Results.**

- jobbland, low against high volume: before controlling for weekday the cluster mix differs (excess 0.106); inside the same quarter and weekday it hardly does (distance 0.016 against 0.011 expected by chance, excess 0.005, p=0.008) and the channel mix does not differ at all (excess 0.000, p=0.10). Weekdays against weekends explain most of the earlier difference. The sector mix still differs (excess 0.028), which fits the change of the sector field below.
- jobbland, jumps: the clearly significant cluster shifts are at 2024-12-23 (the Christmas dip, +0.032), and at 2025-12-09, 2025-12-23 and 2026-01-06 (+0.18, +0.04, +0.04). The last three are produced by two clusters (171 and 168) that exist only because title-less postings are embedded from their opening text (see below); they vanish when title-less postings are left out. Other jumps are borderline and moved between runs, so they are not reported as findings.
- jobbland, sector field: filled for 82 to 91% of postings until 2025-Q2, 52% in 2025-Q3 and 0% from 2025-Q4. The sector mix shifts strongly at the 2025-07-16 and 2025-09-17 jumps (excess +0.33 and +0.29). We do not use the field, so this matters only as a sign that Skillab's output for this board changed in 2025.
- lesjeudis: day totals stable (mean 126 to 251 a day by quarter), no jump to test, sector field filled for 94 to 97%, no difference in channel mix between low and high days and a very small one in cluster mix (excess 0.004 inside quarters).
- jobs.de: two jumps (2024-12-25, 2025-02-05), neither significant (p=0.09, 0.08); no difference between low and high days. Only 221 sampled days, so the test has little power.

**What we can claim.** Within what the database holds, the kinds of job do not depend on how many ads came in. This is consistent with ingestion being unrelated to occupation. It is not a proof that ingestion is random. A bias that never changes (an employer or sector the database never ingests) cannot show up in a comparison of mixes. The test compares the whole mix, so it has little power for small clusters, and emerging occupations are small. lesjeudis and jobs.de give weak evidence because there are few jumps to test. The thesis states the result in these terms and the checks as a limitation.

**The title-less block (jobbland).** No posting taken before 2025-12-09 lacks a title. In the 14 days from 2025-12-09, 61% of postings taken have none. By month the share is 44% in December 2025 (54% weighted) and 13% in January 2026 (10% weighted), and 0% in every other month; 1,389 of 53,959 postings in all. Samples of clusters 171 and 168 show that these postings are ordinary jobs: cluster 171 holds varied occupations (GIS engineer, software tester, team leader, compliance specialist, quality technician, a head of department), and cluster 168 holds introductions of municipalities and regions. The two clusters exist because the first 150 characters of a description are mostly employer boilerplate or a recruiter's opening line, not a description of the job. So the shift of the cluster mix at 2025-12-09 is an artefact of how title-less postings are embedded, not a change in the occupations. What changed is that the postings arrive without a title. The channel flags are not affected: the Month 3 tagger reads title and description, so title-less postings were tagged from the description. Title-less postings are therefore kept in the channel analysis. For occupation clusters, the title lens is not valid for them, and a way to give them an occupation is needed (Open items).

**Consequences for the design.** Event analyses are done inside one board and one stable stretch. For jobbland the AccelerateEU (2026-04-22) window runs from 2026-02-01, after the title-less block, with 80 days on each side and monthly periods; it contains no title-less posting, so it does not wait for the title question. The jobbland data before 2025-12-09 form a separate regime. For lesjeudis, the InvestAI baseline (2025-02-11) falls in a thin stretch of sampled days and its coverage per window is checked first. jobs.de has no event baseline. The sector field is not used.

## HHI across NUTS-2 regions

For each cluster and quarter, the Herfindahl-Hirschman Index measures how concentrated the cluster's postings are across regions:

```latex
HHI = \sum_r s_r^2
```

where s\_r is region r's weighted share of the cluster's postings. It runs from 1/R (spread evenly over R regions) to 1 (all in one region). Example: three regions with shares 0.5, 0.3 and 0.2 give 0.25 + 0.09 + 0.04 = 0.38.

- Postings are mapped to NUTS-2 regions of the 2021 classification (Eurostat GISCO polygons): Sweden 8 and Germany 38 regions were all found; for France the polygon file holds 27 regions and 22 received postings. The 22 are the older pre-2016 regions, not the 13 current ones. The 5 without postings are presumably overseas (not checked). The regional mapping uses the posting's own nuts2 field where it exists (jobbland only, 36% of postings), then Swedish counties, then place names learned from those postings, then a GeoNames lookup with the polygons (script 96).
- Postings with a vague location (for example a country name only) are dropped from the HHI and their share is reported next to it, so the reader sees how much was left out.
- HHI is not comparable across countries without normalisation, because the number of regions differs, and it is noisy for small clusters.

**Mapping results (script 96, 11 November).** Shares are of the raw sampled items, duplicates not removed.

| Board | Placed in a NUTS-2 region | Vague or outside, dropped | Unmatched | Regions found |
| --- | --- | --- | --- | --- |
| jobbland.se | 75.7% | 23.5% vague, 0.5% outside | 0.4% | 8 of 8 |
| lesjeudis.com | 99.8% | under 0.1% | 0.2% | 22 mainland regions |
| jobs.de | 98.7% | 0.8% outside, under 0.1% vague | 0.5% | 38 of 38 |

- **jobbland.se.** Only postings whose location names a county carry their own region (36.1%); the county table agrees with that field in all 20,767 postings checked. Towns written without a county are placed from the same town seen with a county (38.8%). The gazetteer route agreed with the own field in only 20 of 51 postings, so it is switched off for Sweden. The 23.5% dropped are bare country names and Nordic-area names; whether this share changes over time or by cluster has not been checked.
- **lesjeudis.com and jobs.de.** Placement relies on the GeoNames gazetteer and the NUTS 2021 polygons. 45.6% of lesjeudis postings and 29.0% of jobs.de postings sit in place names that exist in more than one region; the largest place is taken. I read the 40 busiest such names for each board and found no wrong choice, which is my own reading, not an independent check.
- **Two errors found and fixed.** A shared manual file dropped 665 Berlin postings as outside Germany; manual rows now name their country. Bracket qualifiers such as (Oder) are kept when the qualified name exists, and otherwise an ambiguous bare name is left unmatched instead of guessed.
- **Concentration.** Île-de-France holds 46.4% of placed lesjeudis postings, so HHI is only comparable within a board.

## Why skill dictionaries, not TF-IDF alone

TF-IDF has no time dimension, so it cannot say which terms are growing. It also surfaces words that are not skills, and it does not map Swedish, French and German terms to one concept. ESCO and Lightcast supply a filtered, multilingual vocabulary of skills, so the same skill is counted the same way across languages. Their importance in a posting is still measured by us, by presence per posting and the trend method above. Lightcast API access is needed for the Lightcast skill list (Tracker skills are never mixed with local skills).

**Caveat: ESCO false positives.** The extractor matches sentences to skills at similarity 0.6 or above, and generic or template sentences can match unrelated skills. This can distort the Month 3 skills-per-channel tables. The check has not been run: the diagnostic cell output is pending, and the effect on those tables is untested.

## Open items

**Status on 13 November.** Items 1 to 3 are unchanged. Item 4 is settled: the rule is in the update above. Item 5 is done: the patterns were corrected and checked on jobbland. Item 7 is done: titles were inferred and checked (88%). Item 8 is done for the clusters read (lesjeudis 68, 139, 117, 67, 33, 107, 141; jobbland 291, 263, 232, 350); the cluster numbers listed in item 8 belong to the first clustering and no longer apply. Item 9 is done for jobbland; for lesjeudis the sampled days around InvestAI were not checked per window (49 sampled days in 2025-Q1 and 44 in 2025-Q2). Items 6 and 10 are only partly answered: the monthly lesjeudis series shows the gap months, but the late-September 2025 collapse was not checked on its own. Item 11 is open.

1. Run `--coherence-only` for the three boards, read `docs/skill_coherence_<board>.md`, choose the threshold, then rerun D with tag v2.
2. Sensitivity check of the ESCO weight (0.25, 0.5, 1.0) with ARI between runs.
3. Diagnostic for false ESCO matches; if confirmed, remove boilerplate sentences before extraction and check the Month 3 skills-per-channel tables.
4. Fix the rule for selecting 6 to 10 clusters: eligible clusters (share crossing, template and title-less filters), flagged share and its change around the event, and manual reading of the postings (script 98).
5. Verify the named-occupation regex matches (battery in particular).
6. Look at the weekly flagged share for jobbland 2025-Q2 and for lesjeudis to see whether spikes or a few weeks drive the wide week-block intervals.
7. Give title-less postings an occupation for the clusters. The opening 150 characters are mostly boilerplate, so they cannot be used. Proposal: infer a title from the description with the Qwen 7B model on Colab (about 1,400 postings) and validate it on titled postings with the title hidden (agreement with the true title); cluster with the inferred titles and report results with and without them. Decision pending.
8. Read the candidate clusters with script 98 and `--only-flagged` (jobbland 237, 16, 138, 15, 234, 69; lesjeudis 34, 125, 139, 88, 71, 121, 117, 126, 115) to check flag false positives before choosing the 6 to 10.
9. Run script 93 for jobbland from 2026-02-01, monthly, 80-day windows around AccelerateEU. For lesjeudis, check the sampled days per window around InvestAI first (population\_lesjeudis.csv).
10. Time-based check of the late-September 2025 collapse of the lesjeudis flagged share (script 97 compares mix with volume, not with time).
11. Ask Skillab, through the supervisor, how ingestion works and whether sources or fields changed between 2024 and 2026 (sector field in 2025, title-less postings in December 2025).

**New items from 13 November**

12. Send the supervisor the Month 4 finding (no validated emerging clusters, and why) with the method results, and agree the Month 5 options.
13. Check the employers of lesjeudis cluster 137 (systems engineer: clearly new in 2024-11 with 49% flagged, then falling) with script 103.
14. Rerun script 101 for lesjeudis and jobs.de with the corrected patterns.
15. Run script 103 for jobs.de and, with `--employer-from text`, for jobbland.
16. Decide whether to cluster the flagged postings only (minimum cluster size about 20) and, if so, prepare the Colab run.
