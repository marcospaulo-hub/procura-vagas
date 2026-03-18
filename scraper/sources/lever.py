import httpx

BASE_URL = "https://api.lever.co/v0/postings/{company_id}?mode=json"

def fetch_jobs(company_id: str) -> list[dict]:
    try:
        response = httpx.get(BASE_URL.format(company_id=company_id), timeout=10)
        response.raise_for_status()
        jobs = response.json()
        return [_parse(job, company_id) for job in jobs]
    except Exception as e:
        print(f"[Lever] Error fetching {company_id}: {e}")
        return []

def _parse(job: dict, company_id: str) -> dict:
    return {
        "id": f"lever_{job['id']}",
        "title": job.get("text", ""),
        "company": company_id,
        "location": job.get("categories", {}).get("location", ""),
        "url": job.get("hostedUrl", ""),
        "content": job.get("descriptionPlain", ""),
        "source": "lever"
    }
