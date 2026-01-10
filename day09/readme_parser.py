import re
from pathlib import Path
from collections import defaultdict

DAY_RE = re.compile(r"^## Day (\d+)")
DEADLINE_RE = re.compile(r"dead-line:\s*([\d\.]+\s+\d{2}:\d{2})", re.IGNORECASE)

STUDENT_ROW_RE = re.compile(r"^\|\s*\[([^\]]+)\]\(")

def normalize_assignment(name: str) -> list[str]:
    name = name.lower()
    assignments = []
    
    # 1. Check for Day XX
    if "day" in name:
        # Find ALL numbers in the string that appear after or near the word "day"
        # This will catch cases "05" and "06" in "Day 05 and 06"
        numbers = re.findall(r"(\d+)", name)
        for num in numbers:
            # Only treat it as a day if it's a reasonable day number (1-10)
            if 1 <= int(num) <= 10:
                assignments.append(f"day{num.zfill(2)}")

    # 2. Check for Project Proposal
    if "proposal" in name or ("final" in name and "project" in name):
        assignments.append("final_project_proposal")

    return assignments if assignments else ["unknown"]

def parse_deadlines(readme_path: Path) -> dict[str, list[str]]:
    deadlines = defaultdict(list)
    current_key = None

    with readme_path.open(encoding="utf-8") as f:
        for line in f:
            line_lower = line.lower()

            # Check for Day headers
            day_match = DAY_RE.match(line)
            if day_match:
                current_key = f"day{int(day_match.group(1)):02d}"
                continue # Move to next line to avoid double-matching
            
            # Check for Project Proposal section
            if "project proposal dead-line" in line_lower:
                current_key = "final_project_proposal"

            # Extract the date using the current_key (either dayXX or proposal)
            deadline_match = DEADLINE_RE.search(line)
            if deadline_match and current_key:
                deadlines[current_key].append(deadline_match.group(1))

    return dict(deadlines)


def parse_students(readme_path: Path) -> dict[str, str]:
    students = {}
    with readme_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Skip headers, separators, and empty/commented rows
            if not line.startswith("|") or "---" in line or "Home page" in line or "[]()" in line:
                continue

            match = STUDENT_ROW_RE.search(line)
            if match:
                canonical = match.group(1).strip()
                # Ensure we didn't capture a placeholder or empty string
                if canonical and canonical != "repo":
                    students[normalize_name(canonical)] = canonical
    return students


def normalize_name(name: str) -> str:
    if not name: return ""
    name = name.strip().lower()
    # Replace dashes and multiple spaces with a single space
    name = re.sub(r"[\-\s]+", " ", name)
    return name