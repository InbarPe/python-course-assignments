from collections import Counter
from datetime import datetime

def submission_delay(record, deadlines):
    deadline_list = deadlines.get(record["assignment"])
    if not deadline_list:
        return None

    # Use the record's timezone (likely UTC)
    tz = record["timestamp"].tzinfo

    deadline_times = [
        datetime.strptime(d, "%Y.%m.%d %H:%M").replace(tzinfo=tz)
        for d in deadline_list
    ]

    # Use the specific deadline for that assignment
    deadline = max(deadline_times)
    return (record["timestamp"] - deadline).total_seconds() / 3600

def delay_bucket(hours):
    if hours <= -24:
        return "early (>24h)"
    if -24 < hours <= 0:
        return "early (<24h)"
    if 0 < hours <= 24:
        return "late (<24h)"
    return "late (>24h)"

def analyze_delays(records, deadlines):
    # key: (student, assignment), value: record_with_earliest_timestamp
    earliest_submissions = {}

    for r in records:
        if not r["student"]:
            continue
            
        for assignment_type in r["assignment"]:
            key = (r["student"], assignment_type)
            
            # If we haven't seen this pair, or this one is earlier than the one we have
            if key not in earliest_submissions or r["timestamp"] < earliest_submissions[key]["timestamp"]:
                # Create a specialized copy for this assignment
                temp_r = r.copy()
                temp_r["assignment"] = assignment_type
                earliest_submissions[key] = temp_r

    # Now calculate delays for only the earliest ones
    results = []
    for r in earliest_submissions.values():
        delay = submission_delay(r, deadlines)
        if delay is not None:
            results.append({
                "student": r["student"],
                "assignment": r["assignment"],
                "delay_hours": delay,
                "bucket": delay_bucket(delay)
            })
    return results

def missing_submissions(records, students_map, assignment):
    submitted = set()
    for r in records:
        if r["student"] is not None and assignment in r["assignment"]:
            submitted.add(r["student"])

    return set(students_map.keys()) - submitted

def assignment_popularity(records):
    counts = Counter()
    for r in records:
        for a in r["assignment"]:
            counts[a] += 1
    return counts
