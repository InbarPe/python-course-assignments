import math
import tkinter as tk
from tkinter import messagebox

"""
This script creates a GUI for calculating wellbeing parameter for a daily weighting and feeding of food restricted mice.
It calculates the mouse's weight (in percent) and food weight (in grams) based on 
the mouse current weight and initial weight (before food restriction started).
If the weight in percent is below 80%, a warning message is displayed.

Input is received via the GUI.

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

# Input validation and calculation function
def validate_and_calculate(event=None):
    try:
        current_weight = float(entry_current.get())
        initial_weight = float(entry_initial.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for weights.")
        return

    if current_weight <= 0 or initial_weight <= 0:
        messagebox.showerror("Input Error", "Weights must be positive numbers.")
        return

    percent_weight, food_weight = percent_and_food_weight(current_weight, initial_weight)

    label_percent.config(text=f"Percent weight (%): {round(percent_weight, 2)}")
    label_food.config(text=f"Food weight (g): {round(food_weight, 2)}")

    if percent_weight < 80:
        messagebox.showwarning("Warning", "Mouse weight is below 80%!")

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

def clear():
    entry_current.delete(0, tk.END)
    entry_initial.delete(0, tk.END)
    label_percent.config(text="Percent weight (%):")
    label_food.config(text="Food weight (g):")
    entry_current.focus_set()

root = tk.Tk()
root.title("Mouse Weight and Food Calculator")
root.resizable(True, True)
root.geometry("400x150") 

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# Inputs
all_frame = tk.Frame(frame)
all_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(all_frame, text="Current weight (g):").grid(row=0, column=0, sticky="e")
entry_current = tk.Entry(all_frame, width=20)
entry_current.grid(row=0, column=1, padx=(5,0))
entry_current.focus_set()

tk.Label(all_frame, text="Initial weight (g):").grid(row=1, column=0, sticky="e")
entry_initial = tk.Entry(all_frame, width=20)
entry_initial.grid(row=1, column=1, padx=(5,0))

# Colored buttons
btn_calc = tk.Button(all_frame, text="Calculate", command=validate_and_calculate,
                     bg="#6FBC72", fg="white", activebackground="#6FBC72", activeforeground="white")
btn_calc.grid(row=2, column=0, pady=10, sticky="ew", columnspan=1)

btn_clear = tk.Button(all_frame, text="Clear", command=clear,
                      bg="#BD7DD2", fg="white", activebackground="#BD7DD2", activeforeground="white")
btn_clear.grid(row=2, column=1, pady=10, sticky="ew", columnspan=1)

# Output
label_percent = tk.Label(all_frame, text="Percent weight (%):", anchor="w")
label_percent.grid(row=3, column=0, columnspan=2, sticky="w")

label_food= tk.Label(all_frame, text="Food weight (g):", anchor="w")
label_food.grid(row=4, column=0, columnspan=2, sticky="w")

# Bind Enter key to calculation
root.bind("<Return>", validate_and_calculate)

root.mainloop()