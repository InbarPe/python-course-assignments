"""
This function calculates the mouse's weight (in percent) and food weight (in grams) based on 
the mouse current weight and initial weight (before food restriction started).

Inputs:
1. Mouse current weight in grams
2. Mouse initial weight in grams

Outputs:
1. Weight in percent
2. Food wieght in grams

Weight in percent calculation:
Mouse current weight / Mouse initial weight * 100

Food wieght calculation:
2.5g of food per 25g of mouse weight. At least 2.5g of food per day
(if the mouse weight < 25g --> still gets 2.5g of food)
"""

def percent_and_food_weight(current_weight, initial_weight):
    # Calculate percent weight
    percent_weight = (current_weight / initial_weight) * 100
    # Calculate food weight
    if current_weight < 25:
        food_weight = 2.5
    else:
        food_weight = (current_weight / 25) * 2.5

    return percent_weight, food_weight