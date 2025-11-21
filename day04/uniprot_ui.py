from uniprot_scraper import search_uniprot, fetch_uniprot_entry, save_json
from rich.console import Console

console = Console()


def main():
    query = input("Enter free-text search for UniProt: ").strip()

    print(f"\n{'=' * 60}")
    print("Searching...")
    print(f"{'=' * 60}")
    results = search_uniprot(query)

    if not results:
        console.print("\nNo results found.", style="bold red")
        return

    if len(results) >= 100:
        print("There are 100 results or more.\n")
    else:
        print(f"\nFound {len(results)} results.\n")

    print("First 5 results:")
    for i, r in enumerate(results[:5], start=1):
        print(f"{i}. {r['accession']} | {r['gene']} | {r['protein_name']}")
        
    while True:
        try:
            num = int(input("\nHow many of the first results to save? ").strip())

            if 1 <= num <= len(results):
                break  # valid → exit the loop
            elif num == 1:
                console.print("\nNo files to save. Exiting.", style="bold yellow")
                return
            else:
                console.print(f"\nPlease enter a number between 0 and {len(results)}", style="yellow")

        except ValueError:
            console.print("\nInvalid input. Please enter a number.", style="red")

    print(f"\n{'=' * 60}")
    print(f"Downloading and saving {num} results...")
    print(f"{'=' * 60}\n")

    for r in results[:num]:
        acc = r["accession"]
        console.print(f"Downloading {acc}", style="green")
        data = fetch_uniprot_entry(acc)
        save_json(data, f"{acc}.json")

    console.print("\nDone! All files saved succesfuly", style="bold green")


if __name__ == "__main__":
    main()
