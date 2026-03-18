import httpx
import os
import json
import re
from google import genai
from bs4 import BeautifulSoup

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

CAREERS_SLUGS = [
    "/careers", "/jobs", "/work-with-us", "/join-us",
    "/about/careers", "/company/careers", "/en/careers",
    "/hiring", "/open-roles", "/positions"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def find_careers_url(domain: str) -> str | None:
    for slug in CAREERS_SLUGS:
        url = f"https://{domain}{slug}"
        try:
            r = httpx.get(url, headers=HEADERS, timeout=8, follow_redirects=True)
            if r.status_code == 200 and len(r.text) > 500:
                return url
        except Exception:
            continue
    return None

def extract_jobs_with_llm(html: str, company: str, source_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    clean_text = soup.get_text(separator="\n", strip=True)[:12000]

    prompt = (
        "Below is text extracted from the careers page of the company " + repr(company) + ".\n"
        "Extract all job openings and return ONLY a valid JSON array.\n"
        "Each item must have:\n"
        "- \"title\": job title (string)\n"
        "- \"location\": location or \"Not specified\" (string)\n"
        "- \"url\": full URL if found, otherwise " + repr(source_url) + " (string)\n\n"
        "If no jobs are found, return an empty array [].\n\n"
        "Text:\n" + clean_text
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        raw = response.text.strip()
        raw = re.sub(r"^```json\s*|^```\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()
        jobs_data = json.loads(raw)
        result = []
        for job in jobs_data:
            title = job.get("title", "").strip()
            if not title:
                continue
            result.append({
                "id": f"custom_{company}_{abs(hash(title))}",
                "title": title,
                "company": company,
                "location": job.get("location", "Not specified"),
                "url": job.get("url", source_url),
                "content": f"{title} {job.get('location', '')}",
                "source": "careers_page"
            })
        return result
    except Exception as e:
        print(f"[LLM] Error parsing {company}: {e}")
        return []

def fetch_jobs(company_name: str, domain: str) -> list[dict]:
    careers_url = find_careers_url(domain)
    if not careers_url:
        print(f"[Careers] No careers page found for {domain}")
        return []

    print(f"[Careers] Found: {careers_url}")
    try:
        r = httpx.get(careers_url, headers=HEADERS, timeout=10, follow_redirects=True)
        r.raise_for_status()
        return extract_jobs_with_llm(r.text, company_name, careers_url)
    except Exception as e:
        print(f"[Careers] Error fetching {careers_url}: {e}")
        return []
