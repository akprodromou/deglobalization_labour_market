# Collection stability: jobbland.se, 2026-01 to 2026-08

Compares the mix of the saved page samples month by month (see the script's header). A flagged transition means the mix changed by more than sampling alone produces; it does not say why. Samples are about 300 postings a month, taken from pages spread over the month's results.

## Each month

| Month | Sampled | With text (200+) | Median description length | Repeated titles | Distinct upload days | Distinct location codes | Distinct types |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-01 | 1500 | 100% | 3,150 | 10.4% | 18 | 1 | 1 |
| 2026-02 | 1500 | 100% | 3,246 | 3.4% | 16 | 1 | 1 |
| 2026-03 | 1500 | 100% | 3,346 | 2.2% | 17 | 1 | 1 |
| 2026-04 | 1500 | 100% | 3,366 | 2.0% | 14 | 1 | 1 |
| 2026-05 | 1500 | 100% | 3,322 | 1.5% | 14 | 1 | 1 |
| 2026-06 | 1500 | 100% | 3,384 | 1.5% | 17 | 1 | 1 |
| 2026-07 | 1500 | 100% | 3,360 | 1.7% | 17 | 1 | 1 |
| 2026-08 | 1500 | 100% | 3,250 | 4.4% | 19 | 1 | 1 |

**Uninformative fields.** The location code and type take a single value in every sampled month, so their distances are always 0 and say nothing about stability.

## Transitions between consecutive months

Distance between month A and the next month B, and the 95th percentile of the same distance between two random halves of the larger-sample month. `FLAG` = above the noise floor.

| From | To | Title words | Floor | Location mix | Floor | Type mix | Floor | Description length | Floor |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-01 | 2026-02 | 0.231 | 0.286 | 0.000 | 0.000 | 0.000 | 0.000 | 0.033 | 0.072 |
| 2026-02 | 2026-03 | 0.221 | 0.269 | 0.000 | 0.000 | 0.000 | 0.000 | 0.044 | 0.069 |
| 2026-03 | 2026-04 | 0.215 | 0.269 | 0.000 | 0.000 | 0.000 | 0.000 | 0.033 | 0.068 |
| 2026-04 | 2026-05 | 0.222 | 0.270 | 0.000 | 0.000 | 0.000 | 0.000 | 0.043 | 0.071 |
| 2026-05 | 2026-06 | 0.224 | 0.268 | 0.000 | 0.000 | 0.000 | 0.000 | 0.066 | 0.071 |
| 2026-06 | 2026-07 | 0.230 | 0.267 | 0.000 | 0.000 | 0.000 | 0.000 | 0.035 | 0.068 |
| 2026-07 | 2026-08 | 0.256 | 0.271 | 0.000 | 0.000 | 0.000 | 0.000 | 0.055 | 0.067 |

**No transition is above the sampling noise floor** for the location mix, the type mix or the description length.

Reading: a flag in the month of an event does not show a policy effect; it shows that the collected mix changed at that point, so a comparison across that boundary compares different kinds of postings. The mix is checked on four fields only; a change in, for example, the scraped category that these fields do not reflect would not show here.
