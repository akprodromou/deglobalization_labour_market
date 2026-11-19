# Clustering settings and the flagged postings: jobsde

Flag = Month 3 tag with intensity medium or higher; 44 flagged postings with a tag. Flagged cluster = at least 10 flagged postings and a flagged share of at least 30%. Postings taken, not weighted.

| min_cluster_size / min_samples | clusters | flagged postings in a cluster | flagged clusters | flagged postings in flagged clusters | top five clusters by flagged share (size, share) |
|---|---|---|---|---|---|
| 40/10 (baseline) | 71 | 37 of 44 (84%) | 0 | 0 (0%) | 27 (876, 2%) |
| 10/10 | 251 | 22 of 44 (50%) | 0 | 0 (0%) |  |
| 20/10 | 154 | 25 of 44 (57%) | 0 | 0 (0%) |  |
| 20/20 | 132 | 25 of 44 (57%) | 0 | 0 (0%) |  |
| 40/40 | 42 | 31 of 44 (70%) | 0 | 0 (0%) | 12 (3564, 0%) |
| 80/20 | 34 | 31 of 44 (70%) | 0 | 0 (0%) | 14 (920, 1%) |
| 80/40 | 21 | 31 of 44 (70%) | 0 | 0 (0%) | 5 (3564, 0%) |
