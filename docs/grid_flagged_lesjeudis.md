# Clustering settings and the flagged postings: lesjeudis

Flag = Month 3 tag with intensity medium or higher; 2,052 flagged postings with a tag. Flagged cluster = at least 10 flagged postings and a flagged share of at least 30%. Postings taken, not weighted.

| min_cluster_size / min_samples | clusters | flagged postings in a cluster | flagged clusters | flagged postings in flagged clusters | top five clusters by flagged share (size, share) |
|---|---|---|---|---|---|
| 40/10 (baseline) | 144 | 1355 of 2048 (66%) | 14 | 659 (32%) | 33 (73, 92%); 140 (48, 60%); 68 (141, 55%); 61 (54, 52%); 130 (199, 51%) |
| 10/10 | 413 | 1373 of 2048 (67%) | 33 | 662 (32%) | 281 (19, 100%); 397 (23, 96%); 267 (13, 92%); 127 (74, 92%); 359 (19, 89%) |
| 20/10 | 265 | 1323 of 2048 (65%) | 28 | 655 (32%) | 253 (23, 96%); 76 (74, 92%); 183 (20, 85%); 219 (29, 83%); 224 (30, 80%) |
| 20/20 | 227 | 1212 of 2048 (59%) | 21 | 577 (28%) | 78 (73, 92%); 200 (27, 89%); 106 (21, 86%); 177 (44, 70%); 172 (29, 66%) |
| 40/40 | 108 | 1096 of 2048 (54%) | 9 | 400 (20%) | 33 (73, 92%); 64 (142, 55%); 107 (44, 52%); 100 (128, 52%); 62 (54, 50%) |
| 80/20 | 57 | 1305 of 2048 (64%) | 5 | 410 (20%) | 30 (144, 56%); 45 (157, 54%); 44 (390, 48%); 47 (96, 34%); 5 (87, 31%) |
| 80/40 | 51 | 1142 of 2048 (56%) | 4 | 293 (14%) | 36 (142, 55%); 48 (128, 52%); 33 (80, 48%); 49 (256, 43%); 14 (83, 29%) |
