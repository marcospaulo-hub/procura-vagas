import json
from pathlib import Path

CACHE_FILE = Path(__file__).parent.parent / "data/seen_jobs.json"

def load_seen() -> set:
    if CACHE_FILE.exists():
        return set(json.loads(CACHE_FILE.read_text()))
    return set()

def save_seen(seen: set):
    CACHE_FILE.parent.mkdir(exist_ok=True)
    CACHE_FILE.write_text(json.dumps(list(seen)))

def filter_new(jobs: list[dict], seen: set) -> list[dict]:
    return [j for j in jobs if j["id"] not in seen]

def mark_seen(jobs: list[dict], seen: set) -> set:
    return seen | {j["id"] for j in jobs}
