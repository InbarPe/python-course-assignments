# Dependencies:

For my mice_weight_and_food_calculator script, there are limited opportunities to use 3rd-party libraries because the core logic is simple arithmetic. 

I asked GitHub Copilot to suggest some dependencies I can use.

Just for fun, to play with dependencies, I added a **rich** library to make the messages/errors look nicer.

In addition, I have the **pytest** library for the test file.
To run the test, write in the terminal:
```bash
pytest test_mice_weight_and_food_calculator.py -v
```

## Dependencies installation:

### rich

```bash
pip install rich
```

### pytest

```bash
pip install pytest
```

# AI prompts

## For dependencies:

* I don't know any 3rd-party libraries that can help me with this code, can you suggest something?
* In this line console.print("Warning: Mouse weight is below 80%!", style="bold red") the 80 is in light blue. How can I fix it?

## For tests:

* I need to create a test file to test my code, that it functions properly, does the calculations right
