# Clustering settings and the flagged postings: jobbland

Flag = Month 3 tag with intensity medium or higher; 1,123 flagged postings with a tag. Flagged cluster = at least 10 flagged postings and a flagged share of at least 30%. Postings taken, not weighted.

| min_cluster_size / min_samples | clusters | flagged postings in a cluster | flagged clusters | flagged postings in flagged clusters | top five clusters by flagged share (size, share) |
|---|---|---|---|---|---|
| 40/10 (baseline) | 357 | 628 of 1123 (56%) | 1 | 26 (2%) | 266 (82, 32%); 350 (193, 30%); 356 (60, 27%); 138 (41, 24%); 253 (76, 18%) |
| 20/10 | 636 | 669 of 1123 (60%) | 3 | 94 (8%) | 402 (29, 34%); 491 (83, 33%); 603 (190, 30%); 610 (60, 27%); 502 (171, 24%) |
| 40/40 | 275 | 566 of 1123 (50%) | 1 | 54 (5%) | 273 (149, 36%); 229 (63, 27%); 191 (51, 25%); 231 (51, 22%); 212 (255, 18%) |
| 80/20 | 133 | 594 of 1123 (53%) | 1 | 25 (2%) | 95 (81, 31%); 132 (235, 27%); 129 (81, 25%); 130 (226, 12%); 51 (126, 10%) |
