import httpx

BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{board_id}/jobs?content=true"

def fetch_jobs(board_id: str) -> list[dict]:
    try:
        response = httpx.get(BASE_URL.format(board_id=board_id), timeout=10)
        response.raise_for_status()
        jobs = response.json().get("jobs", [])
        return [_parse(job, board_id) for job in jobs]
    except Exception as e:
        print(f"[Greenhouse] Error fetching {board_id}: {e}")
        return []

def _parse(job: dict, board_id: str) -> dict:
    return {
        "id": f"greenhouse_{job['id']}",
        "title": job.get("title", ""),
        "company": board_id,
        "location": job.get("location", {}).get("name", ""),
        "url": job.get("absolute_url", ""),
        "content": job.get("content", ""),
        "source": "greenhouse"
    }
