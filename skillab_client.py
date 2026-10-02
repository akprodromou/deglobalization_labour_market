"""
Reusable client for the Skillab tracker API.

Handles HTTP Basic Authentication and paginated traversal, so that later
scripts (sampling, completeness audits, the Tier 1-4 fallback chain, etc.)
can all import this module instead of re-implementing auth/pagination.

SETUP
-----
Before running anything, set your credentials as environment variables
rather than hardcoding them in this file (avoids accidentally committing
them to git or pasting them into a shared notebook):

    export SKILLAB_USERNAME="your_username"
    export SKILLAB_PASSWORD="your_password"

CORRECTION (2026-09): the brief describes HTTP Basic Authentication, but the
actual API's Swagger docs show a token-based login flow instead:

    POST /api/login
    Body: {"username": "...", "password": "..."}
    200 response body: a bare JSON string (the token)
    403 response body: "Invalid credentials"

This has been flagged to the supervising team to confirm which is correct,
in case the Basic Auth description in the brief refers to a different or
older set of endpoints. In the meantime, this client implements the
token-login flow, since that is what the live Swagger docs show.

TODO (confirm these against the actual API docs / your supervisor):
  - BASE_URL is a placeholder -- replace with the real tracker URL.
  - Endpoint paths (PROFILES_ENDPOINT, POSTINGS_ENDPOINT) are guesses.
  - How the token is attached to subsequent requests is NOT confirmed by
    the /api/login docs alone. This client assumes the common convention,
    an `Authorization: Bearer <token>` header, but check the Swagger docs
    for any OTHER endpoint's "Authorize" / security scheme definition to
    confirm this (look for a padlock icon and a "bearerAuth" or similar
    scheme name in Swagger UI), and adjust `_authenticate()` if it turns
    out to use a different header name, a cookie, or a query parameter.
  - Whether the token expires and needs refreshing is unknown -- check
    the docs for a token lifetime, or watch for 401/403 responses
    mid-session and re-authenticate if the client starts failing partway
    through a long pagination run.
  - Pagination parameter names (page/page_size vs offset/limit) are a guess
    based on common REST conventions -- check the real API's pagination
    scheme and adjust `_paginate()` accordingly.
  - The "source" filter parameter name/values (e.g. "revelio", "lightcast")
    need confirming -- ask your supervisor for the full list of sources.
"""

import os
import time
import logging
from typing import Iterator, Optional

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# --- Configuration (confirmed against the live Swagger endpoint list) ------
BASE_URL = "https://skillab-tracker.csd.auth.gr/api"
LOGIN_ENDPOINT = "/login"
PROFILES_ENDPOINT = "/profiles"
# NOTE: there is no endpoint literally called "postings". The brief's
# "postings" is assumed to map to the "Job" resource (POST /api/jobs),
# since a job posting = a job listing. Confirm this reading with your
# supervisor if the exact terminology matters for your methods section.
JOBS_ENDPOINT = "/jobs"
PROFILES_SOURCES_ENDPOINT = "/profiles/sources"
JOBS_SOURCES_ENDPOINT = "/jobs/sources"
# TODO: exact field names within ProfileSchema/JobSchema (skills,
# occupation_uris, description, location, dates) still need confirming
# from the "Schemas" section at the bottom of the Swagger docs page.

DEFAULT_PAGE_SIZE = 100
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 5


class SkillabClient:
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        username = username or os.environ.get("SKILLAB_USERNAME")
        password = password or os.environ.get("SKILLAB_PASSWORD")
        if not username or not password:
            raise ValueError(
                "Missing credentials. Set SKILLAB_USERNAME and SKILLAB_PASSWORD "
                "as environment variables, or pass them directly."
            )
        self.session = requests.Session()
        self._authenticate(username, password)

    def _authenticate(self, username: str, password: str) -> None:
        """
        Log in via POST /api/login and store the returned token for use
        on subsequent requests.

        The Swagger docs confirm the request/response shape (JSON body in,
        bare JSON string out on success, "Invalid credentials" on 403), but
        NOT how the token should be attached afterwards. This assumes a
        standard Bearer-token Authorization header -- verify against the
        docs' security scheme and change this if needed (see module TODOs).
        """
        url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        response = self.session.post(
            url, json={"username": username, "password": password}, timeout=30
        )
        if response.status_code == 403:
            raise PermissionError(f"Login failed: {response.json()}")
        response.raise_for_status()

        token = response.json()  # docs show the 200 response as a bare string
        if not isinstance(token, str) or not token:
            raise ValueError(
                f"Expected a non-empty string token from {LOGIN_ENDPOINT}, "
                f"got: {token!r}"
            )

        # TODO: confirm this is the right header/scheme (see module docstring)
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Authenticated successfully; token stored for session.")

    def _post_with_retries(
        self, url: str, query_params: dict, form_fields: dict
    ) -> requests.Response:
        """
        A single POST with basic retry/backoff on failure.

        query_params go in the URL (?page=1&page_size=100); form_fields go
        in the body as application/x-www-form-urlencoded (via requests'
        `data=` argument, which sets that content-type automatically).
        """
        last_exception = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.session.post(
                    url, params=query_params, data=form_fields, timeout=45
                )
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as exc:
                last_exception = exc
                logger.warning(
                    "Request failed (attempt %d/%d): %s", attempt, MAX_RETRIES, exc
                )
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
        raise last_exception

    def _paginate(
        self, endpoint: str, form_fields: Optional[dict] = None, page_size: int = DEFAULT_PAGE_SIZE
    ) -> Iterator[dict]:
        """
        Generic paginated POST, matching the confirmed house style seen on
        POST /api/skills:
          - "page" and "page_size" are QUERY parameters
          - filter fields (ids, keywords, source, etc.) go in the BODY as
            application/x-www-form-urlencoded, not JSON
          - the response is {"items": [...], "count": N}, not {"results": [...]}

        Stops when a page returns fewer than page_size items, or an empty
        "items" list.

        NOTE: this pattern is confirmed for /api/skills. It is assumed
        (not yet confirmed) that /api/profiles and /api/postings follow
        the same convention -- verify this against their own Swagger
        entries before trusting the fetched data.
        """
        url = f"{BASE_URL}{endpoint}"
        page = 1
        form_fields = form_fields or {}
        records_yielded = 0

        while True:
            query_params = {"page": page, "page_size": page_size}
            response = self._post_with_retries(url, query_params, form_fields)
            payload = response.json()

            records = payload.get("items", [])
            total_count = payload.get("count")

            if not records:
                break

            for record in records:
                yield record
                records_yielded += 1

            logger.info(
                "Fetched page %d (%d/%s records so far)",
                page, records_yielded, total_count if total_count is not None else "?"
            )

            if len(records) < page_size:
                break
            page += 1

    def get_profile_sources(self) -> list:
        """GET /api/profiles/sources -- the real, authoritative list of
        profile sources (no more guessing at ["revelio", "lightcast", ...])."""
        url = f"{BASE_URL}{PROFILES_SOURCES_ENDPOINT}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_job_sources(self) -> list:
        """GET /api/jobs/sources -- the real, authoritative list of job/posting sources."""
        url = f"{BASE_URL}{JOBS_SOURCES_ENDPOINT}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def iter_profiles(self, source: Optional[str] = None, **kwargs) -> Iterator[dict]:
        """
        Yield profile records, optionally filtered by source.

        CONFIRMED against the live ProfileFilter schema (2026-09-29): the
        field is "sources" (plural, array<string>), not "source". A single
        source string is wrapped in a one-item list here for convenience.

        Other confirmed ProfileFilter fields, available via **kwargs if
        needed later: keywords, keywords_logic, ids, skill_ids,
        skill_ids_logic, occupation_uris, occupation_uris_logic, sectors,
        sectors_logic, countries, country_codes.
        """
        form_fields = {"sources": [source]} if source else {}
        form_fields.update(kwargs)
        yield from self._paginate(PROFILES_ENDPOINT, form_fields=form_fields)

    def iter_postings(
        self, source: Optional[str] = None,
        min_upload_date: Optional[str] = None, max_upload_date: Optional[str] = None,
        **kwargs
    ) -> Iterator[dict]:
        """
        Yield job/posting records, optionally filtered by source and/or a
        date range. Maps onto the "Job" resource -- see JOBS_ENDPOINT note.

        CONFIRMED against the live JobFilter schema (2026-09-29): "sources"
        (plural, array<string>); min_upload_date/max_upload_date (string,
        date format -- useful for confirming 2019+ coverage per the brief's
        Week 2 task).

        Other confirmed JobFilter fields, available via **kwargs: keywords,
        keywords_logic, ids, skill_ids, skill_ids_logic, occupation_ids,
        occupation_ids_logic, organization_ids, organization_names,
        sectors, sectors_logic, location_code.
        """
        form_fields = {"sources": [source]} if source else {}
        if min_upload_date:
            form_fields["min_upload_date"] = min_upload_date
        if max_upload_date:
            form_fields["max_upload_date"] = max_upload_date
        form_fields.update(kwargs)
        yield from self._paginate(JOBS_ENDPOINT, form_fields=form_fields)

    def count_postings(self, source: str, min_upload_date: Optional[str] = None,
                        max_upload_date: Optional[str] = None,
                        page_size: int = DEFAULT_PAGE_SIZE) -> int:
        """
        Return the "count" for a filtered /api/jobs query.

        IMPORTANT (2026-10-02): originally used page_size=1 to keep the
        request "lightweight". This turned out to be unreliable -- repeated
        timeouts even on date ranges independently CONFIRMED to have real
        data (eures-escox 2023: confirmed 417 records via the normal
        page_size=100 iterator on one run, then failed twice via a
        page_size=1 count call on a separate run). The one pattern that has
        been reliable across this whole project is page_size=100 through
        the normal paginated request shape, so this now defaults to
        DEFAULT_PAGE_SIZE (100) rather than 1, even though only the count
        is needed, not the records themselves.
        """
        form_fields = {"sources": [source]}
        if min_upload_date:
            form_fields["min_upload_date"] = min_upload_date
        if max_upload_date:
            form_fields["max_upload_date"] = max_upload_date
        url = f"{BASE_URL}{JOBS_ENDPOINT}"
        response = self._post_with_retries(url, {"page": 1, "page_size": page_size}, form_fields)
        return response.json().get("count", 0)

    def iter_skills(self, keywords: Optional[list] = None, **kwargs) -> Iterator[dict]:
        """
        Yield skill records from the CONFIRMED /api/skills endpoint.
        Useful as a working example/sanity-check of the whole client,
        since this endpoint's contract is the one we've actually verified.
        """
        form_fields = {}
        if keywords:
            form_fields["keywords"] = keywords
        form_fields.update(kwargs)
        yield from self._paginate("/skills", form_fields=form_fields)
