import sys

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

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

if __name__ == "__main__":

    # Get user inputs: current weight and initial weight
    try:
        current_weight = float(input("Please enter the mouse current weight in grams: "))
        initial_weight = float(input("Please enter the mouse initial weight in grams: "))

        # Validate that values are positive
        if current_weight <= 0 or initial_weight <= 0:
            print(f"{RED} Error: Weights must be positive numbers. {RESET}")
            sys.exit(1)
        
        # Calculate percent weight and display
        percent_weight = (current_weight / initial_weight) * 100
        print(f"Mouse percent weight is {round(percent_weight, 2)}%")

        # Calculate food weight
        if current_weight < 25:
            food_weight = 2.5
        else:
            food_weight = (current_weight / 25) * 2.5
        print(f"Mouse food weight is {food_weight}g")

        # Display message about weight
        if percent_weight < 80:
            print(f"{RED} Warning: Mouse weight is below 80%! {RESET}")
        else:
            print(f"{GREEN} Mouse weight is good :) {RESET}")
        
    # If input conversion to float fails - invalid input such as letters or empty input
    except ValueError:
        print(f"{RED} Error: Please enter numbers only for weights. {RESET}")