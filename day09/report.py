from readme_parser import parse_students, parse_deadlines
from subjects_parser import parse_subjects
from analysis import analyze_delays, missing_submissions, assignment_popularity
from plot import plot_delay_buckets
from pathlib import Path

BASE_PATH = Path(__file__).parent

def main():
    students = parse_students(BASE_PATH / "readme_data.md")
    deadlines = parse_deadlines(BASE_PATH / "readme_data.md")
    records = parse_subjects(BASE_PATH / "subjects.txt")

    delays = analyze_delays(records, deadlines)
    popularity = assignment_popularity(records)

    print("=" * 60)
    print("DATA-DRIVEN SUBMISSION REPORT")
    print("=" * 60)

    for assignment in sorted(popularity):
        print(f"\nAssignment: {assignment}")
        print("-" * 40)

        relevant = [d for d in delays if d["assignment"] == assignment]
        late = [d for d in relevant if d["delay_hours"] > 0]

        print(f"Total submissions: {len(relevant)}")
        print(f"Late submissions: {len(late)}")

        for d in late:
            name = students.get(d["student"], "UNKNOWN")
            print(f"  - {name}: {d['delay_hours']:.2f} hours late")


        missing = missing_submissions(records, students, assignment)
        if missing:
            print("\nMissing submissions:")
            for name in sorted(missing):
                print(f"  - {name}")

    plot_delay_buckets(delays)

if __name__ == "__main__":
    main()
