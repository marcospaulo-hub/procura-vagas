import re

POSITIVE_SIGNALS = [
    r"worldwide", r"anywhere", r"globally", r"latam", r"latin america",
    r"brazil", r"brasil", r"remote.{0,20}anywhere",
    r"deel", r"remote\.com", r"oyster", r"remote-first",
    r"open to.{0,30}location", r"no.{0,10}location.{0,10}require"
]

NEGATIVE_SIGNALS = [
    r"must be (authorized|eligible) to work in the (us|uk|eu)",
    r"us.{0,10}only", r"uk.{0,10}only", r"eu.{0,10}only",
    r"must relocate", r"requires? (work )?permit",
    r"w-?2 only", r"must reside in"
]

def classify(job: dict) -> str:
    text = f"{job['title']} {job['location']} {job['content']}".lower()
    for pattern in NEGATIVE_SIGNALS:
        if re.search(pattern, text):
            return "rejected"
    for pattern in POSITIVE_SIGNALS:
        if re.search(pattern, text):
            return "accepted"
    if re.search(r"\bremote\b", text):
        return "review"
    return "rejected"
