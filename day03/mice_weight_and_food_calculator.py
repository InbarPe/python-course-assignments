import sys
from mice_weight_and_food_calculator_core import percent_and_food_weight
from rich.console import Console
from rich.text import Text

console = Console()

"""
    This script calculates wellbeing parameter for a daily weghting and feeding of food restricted mice.
    It calculates the mouse's weight (in percent) and food wieght (in grams) based on 
    the mouse current weight and initial weight (before food restriction started).
    If the weight in percent is below 80%, a warning message is displayed.

    Input is requested via standard input (console).

    User inputs:
    1. Mouse current weight in grams
    2. Mouse initial weight in grams

    Script outputs:
    1. Weight in percent
    2. Food wieght in grams
    3. Message about weight in percent (good or bad)

    Weight in percent calculation:
    Mouse current weight / Mouse initial weight * 100

    Food wieght calculation:
    2.5g of food per 25g of mouse weight. At least 2.5g of food per day
    (if the mouse weight < 25g --> still gets 2.5g of food)
    """


def main():
    try:
        # Get user inputs: current weight and initial weight
        current_weight = float(input("Please enter the mouse current weight in grams: "))
        initial_weight = float(input("Please enter the mouse initial weight in grams: "))

        # Validate that values are positive
        if current_weight <= 0 or initial_weight <= 0:
            console.print("Error: Weights must be positive numbers.", style="bold red")
            sys.exit(1)

        # Calculate percent weight and food weight
        percent_weight, food_weight = percent_and_food_weight(current_weight, initial_weight)

        # Display result for percent weight and food weight
        print(f"For a mouse of {current_weight}g with initial weight of {initial_weight}g:")
        print(f"Percent weight is {round(percent_weight, 2)}%")
        print(f"Food weight is {round(food_weight, 2)}g")

        # Display message about weight
        if percent_weight < 80:
            text = Text("Warning: Mouse weight is below 80%!", style="bold red")
            console.print(text)
        elif percent_weight > 100:
            text = Text("Pay attention: Mouse weight is above initial weight", style="bold yellow")
            console.print(text)
        else:
            console.print("Mouse weight is good :)", style="bold green")
        
    # If input conversion to float fails - invalid input such as letters or empty input
    except ValueError:
        console.print("Error: Please enter numbers only for weights.", style="bold red")


if __name__ == "__main__":
    main()
    