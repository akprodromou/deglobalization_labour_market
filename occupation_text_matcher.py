"""
Tier 2 ENHANCEMENT (not the brief's official Tier 3 -- see note below) for
extending occupation-based skill lookup beyond Revelio.

`occupation_uris` is effectively Revelio-exclusive (94.0% complete on
Revelio, 0.0% on all 28 other profile sources, confirmed near-exhaustively).
But the free-text `occupation` field is populated far more broadly across
sources. This module maps that free-text field to an ESCO occupation URI,
so non-Revelio profiles can also reach Tier 2's ESCO-grounded skill lookup
instead of falling straight through to Tier 3's much weaker sector/degree
prior.

CORRECTION, flagged explicitly to the user mid-project: this was originally
built thinking it WAS the brief's official "Tier 3." Re-reading the brief's
exact Table 3 definition showed Tier 3 is actually sector + highest_degree
(see tier3_sector_degree_prior.py), not occupation-text matching. This
module is therefore repositioned as an optional Tier 2 ENHANCEMENT: a way
to reach more profiles via the same ESCO-grounded mechanism as Tier 2,
not a separate, lower-confidence tier of its own.

Two matching strategies:

1. EXACT substring match: profile's free-text `occupation` string contains
   (or is contained by) an ESCO occupation label, case-insensitively.
   Validated against 100 hand-labelled real occupation strings from the
   working sample: 12/12 precision (100%) on the cases where it fired.

2. FUZZY match (TF-IDF cosine similarity over occupation labels):
   validated against the same 100-example set and found to be WORSE than
   chance -- 6/20 precision (30%) on the cases where it fired, and not
   fixable by raising the confidence threshold, since the single
   highest-confidence fuzzy match in the whole set (0.864 cosine
   similarity) was itself wrong. Left in the code (commented path, gated
   by ENABLE_FUZZY_MATCHING) in case a better semantic-matching approach
   replaces it later, but DISABLED by default. Do not re-enable without
   re-validating against a fresh hand-labelled sample.
"""

ENABLE_FUZZY_MATCHING = False  # see validation note above -- do not flip without re-validating
FUZZY_CONFIDENCE_THRESHOLD = 0.75  # unused while ENABLE_FUZZY_MATCHING is False


class OccupationTextMatcher:
    def __init__(self, occupation_labels: dict):
        """
        occupation_labels: {occupation_uri: label}, e.g. from
        OccupationSkillLookup.occupation_labels (occupation_skill_lookup.py),
        so this matcher always stays in sync with whatever ESCO occupations
        Tier 2's lookup table actually covers.
        """
        self.occupation_labels = occupation_labels
        self._label_to_uri = {
            label.lower().strip(): uri
            for uri, label in occupation_labels.items()
            if label
        }
        self._sorted_labels = sorted(self._label_to_uri.keys(), key=len, reverse=True)

        self._fuzzy_vectorizer = None
        self._fuzzy_matrix = None
        self._fuzzy_uris = None
        if ENABLE_FUZZY_MATCHING:
            self._fit_fuzzy()

    def _fit_fuzzy(self):
        from sklearn.feature_extraction.text import TfidfVectorizer

        labels = list(self._label_to_uri.keys())
        self._fuzzy_uris = [self._label_to_uri[label] for label in labels]
        self._fuzzy_vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
        self._fuzzy_matrix = self._fuzzy_vectorizer.fit_transform(labels)

    def match_exact(self, occupation_text: str) -> str:
        """
        Returns an ESCO occupation URI if `occupation_text` contains (or
        is contained by) a known ESCO occupation label, case-insensitively.
        Returns None if no exact match is found.
        """
        if not occupation_text:
            return None
        text = occupation_text.lower().strip()

        if text in self._label_to_uri:
            return self._label_to_uri[text]

        for label in self._sorted_labels:
            if label in text or text in label:
                return self._label_to_uri[label]

        return None

    def match_fuzzy(self, occupation_text: str):
        """
        DISABLED BY DEFAULT -- see module docstring. Calling this while
        ENABLE_FUZZY_MATCHING is False always returns (None, 0.0).
        """
        if not ENABLE_FUZZY_MATCHING or not occupation_text:
            return None, 0.0

        from sklearn.metrics.pairwise import cosine_similarity

        query_vec = self._fuzzy_vectorizer.transform([occupation_text.lower().strip()])
        similarities = cosine_similarity(query_vec, self._fuzzy_matrix)[0]
        best_idx = similarities.argmax()
        best_score = similarities[best_idx]

        if best_score >= FUZZY_CONFIDENCE_THRESHOLD:
            return self._fuzzy_uris[best_idx], float(best_score)
        return None, float(best_score)

    def match(self, occupation_text: str) -> dict:
        """
        Combined entry point: try exact match first, then fuzzy (only if
        enabled). Returns {"occupation_uri": str or None, "method": "exact"
        | "fuzzy" | None, "confidence": float}.
        """
        exact_uri = self.match_exact(occupation_text)
        if exact_uri:
            return {"occupation_uri": exact_uri, "method": "exact", "confidence": 1.0}

        if ENABLE_FUZZY_MATCHING:
            fuzzy_uri, confidence = self.match_fuzzy(occupation_text)
            if fuzzy_uri:
                return {"occupation_uri": fuzzy_uri, "method": "fuzzy", "confidence": confidence}

        return {"occupation_uri": None, "method": None, "confidence": 0.0}


if __name__ == "__main__":
    synthetic_labels = {
        "uri_1": "technical director",
        "uri_2": "software engineer",
        "uri_3": "data scientist",
    }
    matcher = OccupationTextMatcher(synthetic_labels)

    print("Exact match tests:")
    cases = [
        ("Technical Director", "uri_1"),
        ("Senior Software Engineer", "uri_2"),
        ("software engineer", "uri_2"),
        ("nonexistent made-up title", None),
    ]
    for text, expected in cases:
        result = matcher.match(text)
        print(f"  '{text}' -> {result}")
        assert result["occupation_uri"] == expected, f"FAILED on '{text}'"

    print("\nFuzzy matching disabled check:")
    result = matcher.match("softwaer enginer")
    print(f"  '{'softwaer enginer'}' -> {result}")
    assert result["occupation_uri"] is None, "Fuzzy matching should be OFF by default"
    assert ENABLE_FUZZY_MATCHING is False

    print("\nAll smoke-test assertions passed.")
    print(f"\nNote: ENABLE_FUZZY_MATCHING = {ENABLE_FUZZY_MATCHING} "
          "(validated at 30% precision, worse than chance -- kept off).")