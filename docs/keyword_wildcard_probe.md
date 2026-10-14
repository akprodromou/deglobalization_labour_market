# Keyword wildcard probe: kariera.gr, 2026-03

| probe | keywords | logic | count | seconds | first 100: stem in title | stem in description | longer word starting with stem | note |
|---|---|---|---:|---:|---:|---:|---:|---|
| software | ['software'] | - | 0 | 2 | - | - | - |  |
| software* | ['software*'] | - | 0 | 0 | - | - | - |  |
| engineer | ['engineer'] | - | 0 | 1 | - | - | - |  |
| engineer* | ['engineer*'] | - | 0 | 5 | - | - | - |  |
| manager | ['manager'] | - | 0 | 1 | - | - | - |  |
| manager* | ['manager*'] | - | 0 | 1 | - | - | - |  |
| nurse | ['nurse'] | - | 0 | 0 | - | - | - |  |
| nurs* | ['nurs*'] | - | 58 | 5 | 22 | 55 | 58 |  |
| energy | ['energy'] | - | 0 | 0 | - | - | - |  |
| energ* | ['energ*'] | - | 12 | 0 | 0 | 12 | 12 |  |
| software engineer (phrase) | ['software engineer'] | - | 0 | 1 | - | - | - |  |
| software engineer* (phrase) | ['software engineer*'] | - | 0 | 0 | - | - | - |  |
| paper query without asterisks, or | ['software engineer', 'software', 'software development', 'software test', 'software automat'] | or | 0 | 1 | - | - | - |  |
| paper query with asterisks, or | ['software engineer*', 'software', 'software development', 'software test*', 'software automat*'] | or | 0 | 0 | - | - | - |  |

Reading: compare each word with its asterisk version. A higher count with the asterisk, together with hits in the last column (words such as 'softwares' or 'engineering' that only a prefix match can return), means the asterisk is a wildcard. The same count means it is ignored. Zero means it is part of the token. The two last rows show whether the paper's query works as written.