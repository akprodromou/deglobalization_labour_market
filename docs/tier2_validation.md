# Tier 2 validation

Tier 2 infers a skill set from an occupation (ESCO essential + optional skills). Part A checks the skill sets against profiles that report their own skills; part B checks the free-text link that extends Tier 2 beyond Revelio. Aggregate numbers only.

## A. Do the inferred skill sets resemble the profiles' own skills?

- Profiles with an ESCO occupation URI and self-reported skills: **31**; occupation found in the ESCO table: **31**.
- Own skills matched to an ESCO skill (URI or preferred label): 89 of 89 entries (100%). Skills that are free text and not an ESCO label cannot be scored.
- Profiles with at least one matchable own skill (used below): **31**.

Profiles scored: **31**. Mean size of the inferred set: 57 skills.

| Measure | Own occupation | Random other occupation | Difference (95% bootstrap interval) |
|---|---:|---:|---|
| Recall, essential + optional (mean) | 8.9% | 1.5% | +7.5% (-0.0% to +17.5%) |
| Recall, essential only (mean) | 1.1% | 0.0% | |
| Precision, essential + optional (mean) | 0.3% | 0.1% | +0.2% (-0.1% to +0.5%) |
| Recall (median) | 0.0% | 0.0% | |

The own occupation has the higher recall in 5 of 31 profiles (16%).

How to read it: recall says how much of what a person reports is covered by the default set; precision says how much of the default set the person reports (low by construction, since an ESCO occupation lists many optional skills). The result is informative only if the own-occupation values clearly exceed the random-occupation values and the interval excludes zero. With few profiles the interval is wide, and a profile that reports skills is not a typical Tier 2 profile (Tier 2 is for profiles without skills).

## B. Free-text occupation matcher: hand-labelled precision

The sheet could not be read (openpyxl missing, or columns 'method' and 'correct_y_n' not found).

