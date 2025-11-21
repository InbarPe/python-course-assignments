# UniPort search

The (UniPort website)[https://www.uniprot.org/] is used to find information about any protein.

Here, I created a UI (uniprot_ui.py) and business logic (uniprot_scraper,py) scripts that let a user:
1. Search in UniProt with a free-text query (for example glp1\glp1 mouse...).
2. See the first 5 matching proteins.
3. Choose how many of the results to download.
4. Download each selected entry as a full UniProt JSON file.
5. Save them into a folder called UniProt_downloads.

## Notes

* The program retrieves at most 100 results (accession, gene, protein name).
* The program includes a validation loop to ensure:
    Input must be a number.
    Number must be between 1 and len(results).
    User can also type 0 to exit.
* The program uses rich library to make the messages/errors look nicer:
    ```bash
    pip install rich
    ```
---

# AI prompts

I need to write a program that will download some data from the selected web site and save it locally in a file or in multiple files. Separate the "business logic" and the UI (User Interface), the way the program interacts with the user. I want it to be with inputs that the user need to enter to the terminal by the script demand. I want to search and save data from "UniPort". I want it to ask for a word/s to search, then based on the results in the UniPort website to write how many results there are and to save the first n based on the user choice locally in the computer.

