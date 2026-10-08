"""
Source normalisation, decided from the Week 2 completeness-by-source audit.

Two distinct patterns were found among the apparently-duplicate source
names, and they get different treatment:

1. STACK profile sources (e.g. "stack-math" vs "STACK-Mathematics"):
   completeness differs meaningfully between each pair (e.g. 60.4% vs
   96.8% skills completeness), which is NOT what you'd expect from a pure
   casing duplicate of the same data. The more likely explanation is two
   separate ingestion/processing passes over the same underlying forum
   content. DECISION: kept as distinct source values (not merged), but
   flagged via STACK_DUPLICATE_GROUPS below so analyses can choose to
   treat them as one logical source if that fits better, without losing
   the information that they differ in practice.

2. Job-board country-suffixed sources (e.g. "jobbguru" vs "jobbguru.se",
   "kariera.fr" vs "kariera.gr"): these have different posting volumes and
   plausibly represent genuinely different national markets of the same
   platform, not duplicates. DECISION: kept fully distinct. The suffix is
   extracted as a derived `source_country` signal instead of being
   discarded or merged away.
"""

import re

# Pairs of STACK sources believed to be two ingestion passes of the same
# underlying forum, not independent sources. Grouped for optional merging;
# NOT merged by default (see normalize_source below).
STACK_DUPLICATE_GROUPS = {
    "stack-biology": "STACK-Biology",
    "stack-chemistry": "STACK-Chemistry",
    "stack-earthscience": "STACK-Earth Science",
    "stack-interpersonal": "STACK-Interpersonal Skills",
    "stack-law": "STACK-Law",
    "stack-linguistics": "STACK-Linguistics",
    "stack-literature": "STACK-Literature",
    "stack-math": "STACK-Mathematics",
    "stack-philosophy": "STACK-Philosophy",
    "stack-physics": "STACK-Physics",
    "stack-politics": "STACK-Politics",
    "stack-sports": "STACK-Sports",
    "stack-stackoverflow": "STACK-Stack Overflow",
}
# "STACK-Electrical Engineering" and "stack-electronics" are NOT included
# above -- they're topically related but not an obvious casing pair, and
# were not confirmed as duplicates. Treated as genuinely distinct.

# Job-board sources with a country/locale suffix. Maps the raw source
# value to (base_platform, country_code_guess). Country codes here are a
# best-effort guess from the suffix/TLD, NOT independently confirmed
# against the API's own country_codes field -- cross-check before relying
# on this for anything beyond descriptive labeling.
JOB_BOARD_COUNTRY_SUFFIXES = {
    "jobbguru": ("jobbguru", None),       # no suffix = presumed primary/default market
    "jobbguru.se": ("jobbguru", "SE"),
    "jobbland": ("jobbland", None),
    "jobbland.se": ("jobbland", "SE"),
    "jobmedic": ("jobmedic", None),
    "jobmedic.co.uk": ("jobmedic", "GB"),
    "kariera.fr": ("kariera", "FR"),
    "kariera.gr": ("kariera", "GR"),
    "lesjeudis": ("lesjeudis", None),
    "lesjeudis.com": ("lesjeudis", None),  # ".com" is not a country signal; likely the primary domain
}


def normalize_source(raw_source: str, merge_stack_duplicates: bool = False) -> str:
    """
    Returns a normalized source label.

    merge_stack_duplicates=False (default): returns raw_source unchanged
    for STACK sources -- preserves the real, observed difference in data
    quality between the two ingestion passes.

    merge_stack_duplicates=True: collapses each STACK pair to a single
    canonical label (the "STACK-Xxx" form), for analyses where you want
    one row per logical source rather than per ingestion pass. Use this
    only if you've also decided how to merge/dedupe the underlying
    records themselves -- this function only affects the label.
    """
    if merge_stack_duplicates and raw_source in STACK_DUPLICATE_GROUPS:
        return STACK_DUPLICATE_GROUPS[raw_source]
    return raw_source


def get_source_country(raw_source: str) -> str | None:
    """
    Returns a best-effort country code guess for job-board sources with a
    locale suffix, or None if not applicable/unknown. NOT a substitute for
    the API's own `country_codes` filter on profiles -- postings don't
    have an equivalent confirmed field, so this is a label-based proxy.
    """
    if raw_source in JOB_BOARD_COUNTRY_SUFFIXES:
        return JOB_BOARD_COUNTRY_SUFFIXES[raw_source][1]
    return None


def get_base_platform(raw_source: str) -> str:
    """Returns the base platform name, stripping any country suffix."""
    if raw_source in JOB_BOARD_COUNTRY_SUFFIXES:
        return JOB_BOARD_COUNTRY_SUFFIXES[raw_source][0]
    return raw_source
