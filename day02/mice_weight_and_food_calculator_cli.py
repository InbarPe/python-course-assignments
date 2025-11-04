import argparse
import sys

# Color codes for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

"""
This script calculates wellbeing parameter for a daily weighting and feeding of food restricted mice.
It calculates the mouse's weight (in percent) and food weight (in grams) based on 
the mouse current weight and initial weight (before food restriction started).
If the weight in percent is below 80%, a warning message is displayed.

Input is received via command line arguments.
Input formats: 
1. python mice_weight_and_food_calculator_cli.py 26 28.2
2. python mice_weight_and_food_calculator_cli.py --current 26 --initial 28.2

User inputs:
1. Mouse current weight in grams
2. Mouse initial weight in grams

Function outputs:
1. Weight in percent
2. Food wieght in grams
3. Message about weight in percent (good or bad)

Weight in percent calculation:
Mouse current weight / Mouse initial weight * 100

Food wieght calculation:
2.5g of food per 25g of mouse weight. At least 2.5g of food per day
(if the mouse weight < 25g --> still gets 2.5g of food)
"""

# Custom parser to make argparse custome error messages
class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        """Override default error handler for friendly colored output."""
        print(f"{RED}Error: Please enter numbers only for weights.{RESET}\n")
        self.print_help()
        sys.exit(2)

# Core calculation function
def percent_and_food_weight(current_weight, initial_weight):
    # Calculate percent weight
    percent_weight = (current_weight / initial_weight) * 100
    # Calculate food weight
    if current_weight < 25:
        food_weight = 2.5
    else:
        food_weight = (current_weight / 25) * 2.5

    return percent_weight, food_weight

# Main function
def main():
    parser = CustomParser(
        description="Calculate mouse percent weight and recommended daily food (grams)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mice_weight_and_food_calculator_cli.py 26 28.2
  python mice_weight_and_food_calculator_cli.py --current 26 --initial 28.2
"""
    )

    # Add positional and optional arguments for current weight and initial weight
    parser.add_argument('current_weight', nargs='?', type=float, help='Mouse current weight in grams')
    parser.add_argument('initial_weight', nargs='?', type=float, help='Mouse initial weight in grams')
    parser.add_argument('--current', dest='current_weight_opt', type=float, help='Mouse current weight in grams')
    parser.add_argument('--initial', dest='initial_weight_opt', type=float, help='Mouse initial weight in grams')

    args = parser.parse_args()

    # Determine numeric values for current and initial weights (if positional args not provided, use optional args)
    current_weight = args.current_weight if args.current_weight is not None else args.current_weight_opt
    initial_weight = args.initial_weight if args.initial_weight is not None else args.initial_weight_opt

    # Ensure both weights were provided
    if current_weight is None or initial_weight is None:
        print(f"{RED}Error: Both current and initial weights are required.{RESET}")
        print("\nUsage examples:")
        print("  python mice_weight_and_food_calculator_cli.py 26 28.2")
        print("  python mice_weight_and_food_calculator_cli.py --current 26 --initial 28.2")
        sys.exit(1)

    # Validate that values are positive
    if current_weight <= 0 or initial_weight <= 0:
        print(f"{RED}Error: Weights must be positive numbers.{RESET}")
        sys.exit(1)

    # Calculate percent weight and food weight
    percent_weight, food_weight = percent_and_food_weight(current_weight, initial_weight)

     # Display result for percent weight and food weight
    print(f"For a mouse of {current_weight}g with initial weight of {initial_weight}g:")
    print(f"Percent weight is {round(percent_weight, 2)}%")
    print(f"Food weight is {round(food_weight, 2)}g")

    
    if percent_weight < 80:
        print(f"{RED}Warning: Mouse weight is below 80%!{RESET}")
    else:
        print(f"{GREEN}Mouse weight is good :) {RESET}")

if __name__ == "__main__":
    main()
