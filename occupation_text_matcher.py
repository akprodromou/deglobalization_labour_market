"""
Extends Tier 2 of the fallback chain to sources beyond Revelio.

Revelio is the only source with a populated occupation_uris field
(confirmed on 30,389 real records -- see Week 2 report). Every other
source has only a free-text `occupation` field, which is far more
commonly populated but not already linked to an ESCO URI. This module
maps that free text to an ESCO occupation URI, so occupation_skill_lookup.py
can be used on it the same way it already is for Revelio.

VALIDATED (2026-10-02) against 100 real occupation strings, hand-labeled:
  - EXACT substring match: 12/12 correct (100% precision).
  - TF-IDF FUZZY match: 6/20 correct (30% precision) -- WORSE than a coin
    flip, and NOT fixable by raising the confidence threshold: the single
    HIGHEST-confidence fuzzy match in the validation set (0.864) was
    WRONG, while correct and incorrect matches were interleaved across
    the entire confidence range with no clean separating threshold.
    CONCLUSION: fuzzy matching is disabled by default (see
    ENABLE_FUZZY_MATCHING below). This is not a tuning problem -- TF-IDF
    surface-level word overlap does not capture what an informal job
    title actually MEANS well enough for this task. A real fix would
    need genuine semantic matching (e.g. sentence embeddings), not a
    threshold adjustment on this method.

Only EXACT substring matching is used by default. This gives a smaller
but TRUSTWORTHY coverage gain over Revelio-only Tier 2 (roughly 12% of
sampled profiles with occupation text got a confident exact match in the
validation sample -- a real, bounded contribution, not a complete fix for
the "occupation_uris is Revelio-only" gap documented in the Week 2 report).

The label index is built directly from occupationSkillRelations_en.csv
(already in this repo for the Tier 2 skill lookup itself) -- no separate
download needed, since that file already has one occupationLabel per
occupationUri.
"""

import csv
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_RELATIONS_PATH = Path("occupationSkillRelations_en.csv")
MIN_FUZZY_SIMILARITY = 0.45
ENABLE_FUZZY_MATCHING = False  # disabled -- validated at only 30% precision, see module docstring


class OccupationTextMatcher:
    def __init__(self, csv_path: Path = DEFAULT_RELATIONS_PATH):
        self.uri_to_label = {}
        self._load_labels(csv_path)

        self.uris = list(self.uri_to_label.keys())
        self.labels = [self.uri_to_label[u] for u in self.uris]
        self.labels_lower = [lbl.lower() for lbl in self.labels]

        # Fit TF-IDF over the label corpus once, up front, so matching a
        # single free-text string later is cheap (one transform + one
        # similarity computation, not a refit).
        self._vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
        self._label_matrix = self._vectorizer.fit_transform(self.labels)

    def _load_labels(self, csv_path: Path):
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                uri = row["occupationUri"]
                label = row["occupationLabel"]
                if uri and label and uri not in self.uri_to_label:
                    self.uri_to_label[uri] = label

    def match(self, free_text: str):
        """
        Returns a dict: {uri, label, method, confidence} or None if no
        match is found by either method. method is "exact" or "fuzzy".
        confidence is 1.0 for exact matches, the cosine similarity score
        (0-1) for fuzzy matches.
        """
        if not free_text or not free_text.strip():
            return None

        text_lower = free_text.lower()

        # Stage 1: exact substring match. Check longer labels first, so a
        # more specific label (e.g. "senior software developer") wins over
        # a shorter one that might also happen to appear (e.g. "developer").
        candidates = sorted(
            zip(self.labels_lower, self.uris, self.labels),
            key=lambda x: len(x[0]), reverse=True,
        )
        for label_lower, uri, label in candidates:
            if len(label_lower) < 4:
                continue  # skip very short labels, too prone to false positives
            # word-boundary check, not a bare substring, to avoid matching
            # inside an unrelated longer word
            if re.search(r"(?<!\w)" + re.escape(label_lower) + r"(?!\w)", text_lower):
                return {"uri": uri, "label": label, "method": "exact", "confidence": 1.0}

        # Stage 2: TF-IDF fuzzy match -- DISABLED BY DEFAULT.
        # Validated at only 30% precision (6/20) with no usable confidence
        # threshold (see module docstring). Left in the code, gated behind
        # ENABLE_FUZZY_MATCHING, in case a future semantic-matching
        # replacement wants to reuse the surrounding structure -- but
        # should not be turned on as-is.
        if ENABLE_FUZZY_MATCHING:
            text_vector = self._vectorizer.transform([free_text])
            similarities = cosine_similarity(text_vector, self._label_matrix)[0]
            best_idx = similarities.argmax()
            best_score = similarities[best_idx]
            if best_score >= MIN_FUZZY_SIMILARITY:
                return {
                    "uri": self.uris[best_idx], "label": self.labels[best_idx],
                    "method": "fuzzy", "confidence": round(float(best_score), 3),
                }

        return None
