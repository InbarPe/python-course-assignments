import requests
import json
from pathlib import Path

SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"
ENTRY_URL = "https://rest.uniprot.org/uniprotkb"


def search_uniprot(query: str, limit: int = 100) -> list:
    """Performs a free-text search in UniProt and returns a list of accession IDs."""
    params = {
        "query": query,
        "format": "tsv",
        "fields": "accession,id,protein_name",
        "size": limit
    }
    response = requests.get(SEARCH_URL, params=params)
    response.raise_for_status()

    lines = response.text.strip().split("\n")
    header, *rows = lines
    results = []

    for row in rows:
        acc, gene, pname = row.split("\t")
        results.append({
            "accession": acc,
            "gene": gene,
            "protein_name": pname
        })

    return results


def fetch_uniprot_entry(accession: str) -> dict:
    """Downloads full JSON entry for a given accession ID."""
    url = f"{ENTRY_URL}/{accession}.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def save_json(data: dict, filename: str) -> None:
    """Saves a Python dictionary as a JSON file in UniProt_downloads/."""

    # Create folder path
    folder = Path("UniProt_downloads")
    folder.mkdir(exist_ok=True)

    # Create full file path inside folder
    path = folder / filename

    # Save the JSON
    with path.open("w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
