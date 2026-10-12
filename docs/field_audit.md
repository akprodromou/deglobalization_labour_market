# Field audit and id-as-clock test for undated postings

Script: `diagnostics/31_undated_field_audit.py`. Evenly spaced pages of the unfiltered result set (ordered by id).

## eures-escox

Postings sampled: 92 dated, 108 undated (8 pages).

### A. Fields actually returned (share of postings with a non-empty value)

| Field | Documented | Dated | Undated |
|---|---|---|---|
| description | yes | 100% | 100% |
| id | yes | 100% | 100% |
| location | yes | 76% | 51% |
| location_code | yes | 100% | 100% |
| nuts1 | yes | 84% | 75% |
| nuts2 | yes | 84% | 75% |
| nuts3 | yes | 84% | 75% |
| occupations | yes | 42% | 98% |
| organization | yes | 86% | 66% |
| sectors | yes | 40% | 89% |
| skills | yes | 100% | 100% |
| source | yes | 100% | 100% |
| source_id | yes | 100% | 100% |
| title | yes | 100% | 100% |
| type | yes | 100% | 100% |
| upload_date | yes | 100% | 0% |

Keys present in the raw JSON (even when the value is always null), 8 of 8 pages recorded:

- No top-level key beyond the documented JobSchema is returned.
- Every documented key is returned.

Nested fields (first element of organization / skills / occupations / sectors):

none

Fields whose name looks like a date/time, with example values:

- `upload_date`: ['2025-10-14', '2026-02-10', '2026-01-30']

One complete undated record (description truncated, skills/occupations shortened):

```
{
 "organization": "ΚΥΡΙΑΚΟΣ ΚΑΨΟΥΛΗΣ & ΑΝΔΡΕΑΣ ΑΝΔΡΕΟΥ",
 "sectors": [
  "Machining of metals",
  "Manufacture of other general-purpose machinery n.e.c.",
  "Manufacture of machinery for food, beverage and tobacco processing"
 ],
 "id": 6515428,
 "title": "WELDER",
 "description": "EXECUTION OF METAL WELDING ACCORDING TO THE TECHNICAL DRAWINGS AND PROJECT SPECIFICATIONS. MAINTENANCE, INSPECTION AND ADJUSTMENT OF WELDING EQUIPMENT. COMPLIAN",
 "experience_level": null,
 "type": "contracttohire",
 "location": "ORMIDEIA-LARNAKA, CY",
 "location_code": "CY",
 "nuts1": "Κύπρος",
 "nuts2": "Κύπρος",
 "nuts3": "Κύπρος",
 "upload_date": null,
 "source": "eures-escox",
 "source_id": "MzI4ODE4IDU",
 "skills": "<6 items>",
 "occupations": [
  "http://data.europa.eu/esco/occupation/17b29190-6746-4b81-a1d1-8053a5bbc0e9"
 ]
}
```

### B. Can the id date an undated posting?

Each dated posting (n=92) is predicted from the nearest dated posting in a different page. Absolute error in days:

| median | 75th pct | 90th pct | max | within 7 days | within 31 days |
|---|---|---|---|---|---|
| 14 | 54 | 89 | 119 | 45% | 67% |

Neighbouring dated postings from different pages whose date goes backwards as id increases: 1/5.
