# Keyword filter probe 2: kariera.gr, 2026-03

## A. Is the title searched?

Words taken from a posting's title that do not occur in its description (case-insensitive). 'returned' = the posting is among the first 100 results for that word.

| word | posting id | count | returned | note |
|---|---:|---:|---|---|
| saleswomen | 2430 | 54 | yes |  |
| postgraduate | 5291141 | 0 | NO |  |
| experienced | 5294187 | 0 | NO |  |
| scientist | 5294190 | 27 | yes |  |
| consultant | 5303536 | 0 | NO |  |
| assistants | 5352913 | 0 | NO |  |

## B. case

| probe | keywords | logic | count | seconds | note |
|---|---|---|---:|---:|---|
| hotel | ['hotel'] | - | 1,748 | 0 |  |
| Hotel | ['Hotel'] | - | 1,748 | 0 |  |
| HOTEL | ['HOTEL'] | - | 1,748 | 0 |  |

## C. logic

| probe | keywords | logic | count | seconds | note |
|---|---|---|---:|---:|---|
| hotel | ['hotel'] | - | 1,748 | 0 |  |
| driver | ['driver'] | - | 525 | 0 |  |
| hotel or driver | ['hotel', 'driver'] | or | 2,210 | 1 |  |
| hotel and driver | ['hotel', 'driver'] | and | 63 | 1 |  |

## D. plural and stem

| probe | keywords | logic | count | seconds | note |
|---|---|---|---:|---:|---|
| hotel | ['hotel'] | - | 1,748 | 0 |  |
| hotels | ['hotels'] | - | 0 | 0 |  |
| hote | ['hote'] | - | 0 | 0 |  |

## E. phrase

| probe | keywords | logic | count | seconds | note |
|---|---|---|---:|---:|---|
| 'hotel manager' as one keyword | ['hotel manager'] | - | 0 | 2 |  |
| hotel and manager | ['hotel', 'manager'] | and | 0 | 0 |  |
| manager | ['manager'] | - | 0 | 0 |  |