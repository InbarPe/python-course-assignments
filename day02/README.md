# How I solved the assignment:

1. Using GitHub copilot I created the circle_area_calculator_gui
2. Wrote mice_weight_and_food_calculator_inputs on my own - a tool that can help me with animal monitoring in the lab
3. Wrote mice_weight_and_food_calculator_cli based on triangle_area_cli.py from the class and with help of GitHub copilot
4. Wrote mice_weight_and_food_calculator_gui based on circle_area_calculator_gui and with help of ChatGPT

## AI prompts

### For step 1 (GUI for circle)

* Can you please write me a GUI program that gets from the user the circle radius and calculates the circle area?
* Can you please specify in the GUI that the radius is in cm?
* Is there a way to draw the required circle next to a reference circle of 1cm radius?
* Now can you make the window adjustable? so I can expend it if I want. Also, can we add some colors? Maybe for the buttons?

### For step 3 (Command line)

* What does this section do? Is it obligatory?
    "parser = argparse.ArgumentParser(
        description="Calculate the area of a triangle using base and height",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python triangle_area_cli.py 10 5
  python triangle_area_cli.py --base 7.5 --height 4.2
  python triangle_area_cli.py -b 12 --height 8
        """
    )"
* Can you please explain to me each section here?
 "parser.add_argument('base', nargs='?', type=float, 
                       help='Base of the triangle')
    parser.add_argument('height', nargs='?', type=float, 
                       help='Height of the triangle')

    parser.add_argument('-b', '--base', dest='base_opt', type=float,
                       help='Base of the triangle (alternative to positional argument)')
    parser.add_argument('--height', dest='height_opt', type=float,
                       help='Height of the triangle (alternative to positional argument)')

    parser.add_argument('--version', action='version', version='Triangle Calculator 1.0')

    args = parser.parse_args()"
* I want to make a custom error for invalid arguments. How can I do it?

### For step 4 (GUI)

* How can I validate the input and add errors?
* Is there a way to center all widgets in the window?
