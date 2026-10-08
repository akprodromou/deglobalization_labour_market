"""
Are there job sources we have not queried?

All our work uses the 16 names returned earlier by GET /api/jobs/sources. This
script (1) fetches that list again and prints anything that is not one of the 16
(tonight's trend run used a hard-coded list because the endpoint timed out), and
(2) probes extra source names you give it, such as kariera.group, by asking for
the posting count with sources=[name] and no date filter.

Reading a probe: a count above 0 means the source exists and holds that many
postings; 0 means no postings under that exact name (a misspelt or unknown name
also gives 0, so 0 is not proof the source does not exist); FAILED is a timeout
or an error, so try again.

Usage, from the repo root (credentials in env vars):
    python -m diagnostics.28_list_job_sources
    python -m diagnostics.28_list_job_sources --try kariera.group kariera.com
    python -m diagnostics.28_list_job_sources --profiles     # also list profile sources
"""

import argparse
import time

from skillab_client import BASE_URL, JOBS_ENDPOINT, SkillabClient

KNOWN = {"OJA", "eures", "eures-escox", "kariera.gr", "jobbland.se", "jobbland", "jobs.de",
         "kariera.fr", "lesjeudis.com", "lesjeudis", "jobmedic.co.uk", "jobmedic",
         "jobscentral", "jobbguru.se", "jobbguru", "brightminds"}


def get_with_retries(client, path, attempts=4, timeout=120):
    last = None
    for i in range(1, attempts + 1):
        try:
            r = client.session.get(f"{BASE_URL}{path}", timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as exc:
            last = exc
            print(f"  attempt {i}/{attempts} failed: {exc}")
            time.sleep(5 * i)
    raise last


def probe(client, name):
    r = client.session.post(f"{BASE_URL}{JOBS_ENDPOINT}", params={"page": 1, "page_size": 100},
                            data={"sources": [name]}, timeout=90)
    r.raise_for_status()
    return r.json().get("count", 0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--try", dest="extra", nargs="*", default=[], help="extra source names to probe")
    parser.add_argument("--profiles", action="store_true")
    args = parser.parse_args()
    client = SkillabClient()

    print("GET /jobs/sources")
    try:
        listed = get_with_retries(client, "/jobs/sources")
    except Exception as exc:
        listed = None
        print(f"  could not fetch the list: {exc}")
    if listed is not None:
        names = [x if isinstance(x, str) else str(x) for x in listed]
        print(f"  {len(names)} sources returned: {sorted(names)}")
        new = sorted(set(names) - KNOWN)
        gone = sorted(KNOWN - set(names))
        print(f"  not among our 16: {new if new else 'none'}")
        print(f"  among our 16 but not listed now: {gone if gone else 'none'}")

    if args.profiles:
        print("\nGET /profiles/sources")
        try:
            print("  " + str(sorted(map(str, get_with_retries(client, "/profiles/sources")))))
        except Exception as exc:
            print(f"  could not fetch the list: {exc}")

    if args.extra:
        print("\nProbing extra names (count with no date filter):")
        for name in args.extra:
            try:
                print(f"  {name}: {probe(client, name):,}")
            except Exception as exc:
                print(f"  {name}: FAILED ({exc})")


if __name__ == "__main__":
    main()
