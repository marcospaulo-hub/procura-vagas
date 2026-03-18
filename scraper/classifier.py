import re

# Evidências concretas de infraestrutura de contratação global
STRONG_POSITIVE = [
    r"\bdeel\b", r"remote\.com", r"\boyster\b", r"\brippling\b",
    r"employer of record", r"\beor\b",
    r"independent contractor", r"\bcontractor\b",
    r"utc-3", r"utc-5", r"south america", r"latin america", r"\blatam\b",
    r"hire.{0,20}anywhere", r"work.{0,20}anywhere", r"anywhere in the world",
    r"brazil", r"brasil",
]

# Sinais fracos — indicam possibilidade mas não confirmam
WEAK_POSITIVE = [
    r"\bworldwide\b", r"\bglobally\b", r"remote.{0,20}first",
    r"distributed team", r"fully remote", r"work from anywhere",
    r"no.{0,10}location.{0,10}required",
]

NEGATIVE_SIGNALS = [
    r"must be (authorized|eligible) to work in the (us|uk|eu)",
    r"\bus.{0,5}only\b", r"\buk.{0,5}only\b", r"\beu.{0,5}only\b",
    r"must relocate", r"requires? (work )?permit",
    r"w-?2 only", r"must reside in",
    r"\bon.?site\b", r"\bhybrid\b",
    r"authorized to work in",
    r"(new york|san francisco|london|berlin|amsterdam).{0,20}(only|required|office)",
]

def classify(job: dict) -> str:
    text = f"{job['title']} {job['location']} {job['content']}".lower()

    for pattern in NEGATIVE_SIGNALS:
        if re.search(pattern, text):
            return "rejected"

    for pattern in STRONG_POSITIVE:
        if re.search(pattern, text):
            return "accepted"

    for pattern in WEAK_POSITIVE:
        if re.search(pattern, text):
            return "review"

    return "rejected"
