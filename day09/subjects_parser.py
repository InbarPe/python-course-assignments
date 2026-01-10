import re
from datetime import datetime
from readme_parser import normalize_assignment
from readme_parser import normalize_name

LINE_RE = re.compile(
    r"(?P<id>\d+)\t"
    r"(?P<status>OPEN|CLOSED)\t"
    r"(?P<title>.+?)\t+"
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)"
)

def extract_student(title: str, known_students: dict = None) -> str | None:
    if not title:
        return None

    # Check for "by [Name]" or "- [Name]" or "Day XX [Name]"
    name_pattern = r"[A-Za-z][A-Za-z\-]*(?:\s+[A-Za-z][A-Za-z\-]*)*"
    
    patterns = [
        rf"\bby\s+({name_pattern})",
        rf"-\s*({name_pattern})\s*$",
        rf"day\s*\d+\s+({name_pattern})\s*$"
    ]

    for pat in patterns:
        match = re.search(pat, title, re.IGNORECASE)
        if match:
            return normalize_name(match.group(1))
        
    if known_students:
        # Normalize the current title to remove dashes for comparison
        clean_title = normalize_name(title) 
        for normalized_key in known_students.keys():
            # normalized_key is already "clean" from our updated normalize_name
            if normalized_key in clean_title:
                return normalized_key

    return None

def parse_subjects(path: str) -> list[dict]:
    records = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            match = LINE_RE.search(line)
            if not match:
                continue

            r = match.groupdict()
            r["timestamp"] = datetime.fromisoformat(
                r["timestamp"].replace("Z", "+00:00")
            )
            r["student"] = extract_student(r["title"])
            r["assignment"] = normalize_assignment(r["title"])
            records.append(r)

    return records
