# Field audit and id-as-clock test for undated postings

Script: `diagnostics/31_undated_field_audit.py`. Evenly spaced pages of the unfiltered result set (ordered by id).

## eures

Postings sampled: 920 dated, 480 undated (14 pages).

### A. Fields actually returned (share of postings with a non-empty value)

| Field | Documented | Dated | Undated |
|---|---|---|---|
| description | yes | 98% | 98% |
| experience_level | yes | 0% | 0% |
| id | yes | 100% | 100% |
| location | yes | 93% | 52% |
| location_code | yes | 100% | 100% |
| nuts1 | yes | 92% | 83% |
| nuts2 | yes | 90% | 83% |
| nuts3 | yes | 90% | 83% |
| occupations | yes | 90% | 94% |
| organization | yes | 98% | 82% |
| sectors | yes | 74% | 87% |
| skills | yes | 59% | 11% |
| source | yes | 100% | 100% |
| source_id | yes | 100% | 100% |
| title | yes | 100% | 100% |
| type | yes | 100% | 99% |
| upload_date | yes | 100% | 0% |

No top-level field beyond the documented JobSchema is returned.

Nested fields (first element of organization / skills / occupations / sectors):

none

Fields whose name looks like a date/time, with example values:

- `upload_date`: ['2026-02-09', '2025-11-15', '2026-02-03']

One complete undated record (description truncated, skills/occupations shortened):

```
{
 "organization": "ПРОФЕСИОНАЛНА ГИМНАЗИЯ ПО ТРАНСПОРТ И АГРАРНИ ТЕХНОЛОГИИ \"Н.Й.ВАПЦАРОВ\" - ХАСКОВО Училище",
 "sectors": [],
 "id": 6414172,
 "title": "Teacher, general education subject in high school",
 "description": "Philosophy teacher",
 "experience_level": null,
 "type": "directhire",
 "location": "Хасково, BG",
 "location_code": "BG",
 "nuts1": "Югозападна и Южна централна България",
 "nuts2": "Южен централен",
 "nuts3": "Хасково",
 "upload_date": null,
 "source": "eures",
 "source_id": "MTk2ODU5NyA0",
 "skills": "<0 items>",
 "occupations": []
}
```

### B. Can the id date an undated posting?

Each dated posting (n=920) is predicted from the nearest dated posting in a different page. Absolute error in days:

| median | 75th pct | 90th pct | max | within 7 days | within 31 days |
|---|---|---|---|---|---|
| 13 | 33 | 56 | 482 | 39% | 74% |

Neighbouring dated postings from different pages whose date goes backwards as id increases: 4/13.
