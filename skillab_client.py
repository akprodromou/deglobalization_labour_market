"""
Reusable client for the Skillab tracker API.

Handles token-based authentication and paginated traversal, so that later
scripts (sampling, completeness audits, the Tier 1-4 fallback chain, etc.)
can all import this module instead of re-implementing auth/pagination.

SETUP
-----
Before running anything, set your credentials as environment variables
rather than hardcoding them in this file:

    export SKILLAB_USERNAME="your_username"
    export SKILLAB_PASSWORD="your_password"

CONFIRMED (2026-09-29): auth is a token-based login flow, not HTTP Basic
Auth as the brief originally described:

    POST /api/login
    Body: {"username": "...", "password": "..."}
    200 response body: a bare JSON string (the token)
    403 response body: "Invalid credentials"

Token is attached as: Authorization: Bearer <token>

CONFIRMED endpoint list (from live Swagger docs, 2026-09-29):
  - PROFILES_ENDPOINT = /profiles
  - JOBS_ENDPOINT = /jobs (brief's "postings" maps to this)
  - Filter field for source is "sources" (plural, array), not "source"

KNOWN SERVER-SIDE ISSUE (as of 2026-09-29, reported to supervising team):
  POST /api/profiles, GET /api/profiles/sources, and GET /api/jobs/sources
  all hang indefinitely with zero bytes received -- confirmed independently
  with curl and Python's requests. POST /api/skills works correctly (200 OK)
  using an identical request pattern, so this looks like a server-side issue
  specific to the profiles/jobs endpoints, not a client-side problem.
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
JOBS_ENDPOINT = "/jobs"
PROFILES_SOURCES_ENDPOINT = "/profiles/sources"
JOBS_SOURCES_ENDPOINT = "/jobs/sources"

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
        """Log in via POST /api/login and store the returned Bearer token."""
        url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        response = self.session.post(
            url, json={"username": username, "password": password}, timeout=45
        )
        if response.status_code == 403:
            raise PermissionError(f"Login failed: {response.json()}")
        response.raise_for_status()

        token = response.json()
        if not isinstance(token, str) or not token:
            raise ValueError(
                f"Expected a non-empty string token from {LOGIN_ENDPOINT}, "
                f"got: {token!r}"
            )

        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Authenticated successfully; token stored for session.")

    def _post_with_retries(
        self, url: str, query_params: dict, form_fields: dict
    ) -> requests.Response:
        """A single POST with basic retry/backoff on failure."""
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
        Generic paginated POST, matching the confirmed house style:
          - "page"/"page_size" are query parameters
          - filter fields go in the body as application/x-www-form-urlencoded
          - the response is {"items": [...], "count": N}
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
        """GET /api/profiles/sources -- KNOWN TO HANG server-side as of 2026-09-29."""
        url = f"{BASE_URL}{PROFILES_SOURCES_ENDPOINT}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_job_sources(self) -> list:
        """GET /api/jobs/sources -- KNOWN TO HANG server-side as of 2026-09-29."""
        url = f"{BASE_URL}{JOBS_SOURCES_ENDPOINT}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def iter_profiles(self, source: Optional[str] = None, **kwargs) -> Iterator[dict]:
        """
        Yield profile records, optionally filtered by source.
        CONFIRMED: filter field is "sources" (plural, array<string>).

        Other confirmed ProfileFilter fields, via **kwargs: keywords,
        keywords_logic, ids, skill_ids, skill_ids_logic, occupation_uris,
        occupation_uris_logic, sectors, sectors_logic, countries, country_codes.
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
        Yield job/posting records, optionally filtered by source and/or date range.
        CONFIRMED: filter field is "sources" (plural, array<string>);
        min_upload_date/max_upload_date confirm 2019+ coverage per brief's Week 2 task.

        Other confirmed JobFilter fields, via **kwargs: keywords, keywords_logic,
        ids, skill_ids, skill_ids_logic, occupation_ids, occupation_ids_logic,
        organization_ids, organization_names, sectors, sectors_logic, location_code.
        """
        form_fields = {"sources": [source]} if source else {}
        if min_upload_date:
            form_fields["min_upload_date"] = min_upload_date
        if max_upload_date:
            form_fields["max_upload_date"] = max_upload_date
        form_fields.update(kwargs)
        yield from self._paginate(JOBS_ENDPOINT, form_fields=form_fields)

    def count_postings(self, source: str, min_upload_date=None, max_upload_date=None) -> int:
        """
        Return just the "count" for a filtered /api/jobs query, using
        page_size=1 so the request stays lightweight -- used for binary
        searching a source's true min/max upload_date without pulling
        full pages of records.
        """
        form_fields = {"sources": [source]}
        if min_upload_date:
            form_fields["min_upload_date"] = min_upload_date
        if max_upload_date:
            form_fields["max_upload_date"] = max_upload_date
        url = f"{BASE_URL}{JOBS_ENDPOINT}"
        response = self._post_with_retries(url, {"page": 1, "page_size": 1}, form_fields)
        return response.json().get("count", 0)

    def iter_skills(self, keywords: Optional[list] = None, **kwargs) -> Iterator[dict]:
        """Yield skill records from the CONFIRMED WORKING /api/skills endpoint."""
        form_fields = {}
        if keywords:
            form_fields["keywords"] = keywords
        form_fields.update(kwargs)
        yield from self._paginate("/skills", form_fields=form_fields)
