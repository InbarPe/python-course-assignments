# Submission Analysis Tool
This project provides a reporting tool to track student assignments and project proposals for the WIS Python Programming Course. It parses the course README for deadlines and student names, then analyzes a subjects.txt log (exported from GitHub issues) to determine submission status and timeliness.

## Features
* *Multi-Assignment Support*: Correctly handles titles that submit multiple days at once (e.g., "Day 05 and 06").

* *Fuzzy Name Matching*: Automatically resolves naming inconsistencies (e.g., matching "Israel Israeli Israeli" with the canonical "Israel Israeli-Israeli").

* *Earliest Submission Logic*: If a student submits the same assignment multiple times, the tool only considers the earliest timestamp for deadline analysis.

* *Late Detection*: Compares UTC timestamps from GitHub against course deadlines to calculate exact delay in hours.

* *Visual Reporting*: Generates bar charts to visualize the distribution of submission times (Early vs. Late).

## Project Structure
* subjects_parser.py: Extracts student names and assignment types from issue titles using Regular Expressions and fuzzy matching.

* readme_parser.py: Scrapes the readme_data.md to build a database of canonical student names and assignment deadlines.

* analysis.py: Logic for calculating submission delays, deduplicating records, and identifying missing students.

* report.py: The entry point that aggregates the data and prints the final formatted report.

## Setup and Installation
1. *Prerequisites*: Ensure you have Python 3.10+ installed.

2. *Dependencies*: This project uses standard Python libraries

3. *Data Files*: Ensure the following files are in the root directory:

    - subjects.txt: The export of GitHub issue titles and timestamps.

    - readme_data.md: The course syllabus/README file.

## Usage
To generate the submission report, run:

``` bash
    python report.py
```

## How It Works
### Assignment Normalization
The tool uses a "priority search" to categorize submissions. It first looks for "Day XX" patterns. If the word "proposal" or "final project" is found, it adds a project category. This allows a single submission line to count toward multiple requirements.

### Deadline Calculation
Deadlines are extracted from the README. The tool converts these to timezone-aware objects to ensure accurate comparison with the UTC timestamps provided in subjects.txt.

## Known Edge Cases Handled
* *Inconsistent Delimiters*: Handles names following "by", dashes "-", or trailing space.

* *Missing "Day" Prefix*: Correctly identifies "Day 05 and 06" as two separate assignments.

* *Typo Tolerance*: Normalizes spaces and dashes in student names to ensure matching works even with minor typos.