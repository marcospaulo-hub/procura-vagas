import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sources.greenhouse import fetch_jobs as gh_fetch
from sources.lever import fetch_jobs as lever_fetch
from sources.careers_page import fetch_jobs as careers_fetch
from classifier import classify
from dedup import load_seen, save_seen, filter_new, mark_seen
from notifier import send

COMPANIES_FILE = Path(__file__).parent.parent / "data/companies.json"

SRE_KEYWORDS = [
    "sre", "site reliability", "devops", "platform engineer",
    "infrastructure", "cloud engineer", "devsecops"
]

def is_relevant(job: dict) -> bool:
    return any(kw in job["title"].lower() for kw in SRE_KEYWORDS)

def run():
    companies = json.loads(COMPANIES_FILE.read_text())
    all_jobs = []

    for company in companies:
        if company.get("greenhouse_id"):
            all_jobs += gh_fetch(company["greenhouse_id"])
        if company.get("lever_id"):
            all_jobs += lever_fetch(company["lever_id"])
        if company.get("domain"):
            all_jobs += careers_fetch(company["name"], company["domain"])

    relevant = [j for j in all_jobs if is_relevant(j)]

    for job in relevant:
        job["latam_status"] = classify(job)

    candidates = [j for j in relevant if job["latam_status"] != "rejected"]
    seen = load_seen()
    new_jobs = filter_new(candidates, seen)

    print(f"Total scrapeado: {len(all_jobs)}")
    print(f"Vagas relevantes: {len(relevant)}")
    print(f"Aprovadas pelo filtro LATAM: {len(candidates)}")
    print(f"Novas para notificar: {len(new_jobs)}")

    send(new_jobs)
    save_seen(mark_seen(new_jobs, seen))

if __name__ == "__main__":
    run()
