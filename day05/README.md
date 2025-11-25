# Word Scramble — Food Edition

A small terminal game that presents a scrambled food-related word and asks the player to guess it.

## Requirements
- Tested with Python 3.8+.
- No external dependencies are required (the game uses only the Python standard library).
- Ensure the `word_list.py` module exists in the same folder and exposes a `words` variable (a list of strings).

## How to Play the Game
In the terminal run:
``` bash
python Word_Scramble.py
```

Yot will get a scrable food-related word.
You will be able to guess the correct word until you succsess/quit.


## Tests
To run the test, write in the terminal:
``` bash
pytest test_word_scramble.py -v   
```

For this you need to install *pytest*:
``` bash
pip install pytest
```