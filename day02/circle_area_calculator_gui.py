import math
import tkinter as tk
from tkinter import messagebox

CANVAS_WIDTH = 520
CANVAS_HEIGHT = 220
REF_RADIUS_CM = 1.0
PADDING = 12
BASE_SCALE = 80  # pixels per cm (max)

last_radius = 0.0

def calculate_area(event=None):
    global last_radius
    radius_str = entry_radius.get().strip()
    try:
        r = float(radius_str)
        if r < 0:
            raise ValueError("Negative radius")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a non-negative number for the radius (cm).")
        entry_radius.focus_set()
        return

    last_radius = r
    area = math.pi * r * r
    label_result.config(text=f"Area: {area:.4f} cm²")
    draw_circles(r)

def clear():
    global last_radius
    entry_radius.delete(0, tk.END)
    label_result.config(text="Area (cm²):")
    entry_radius.focus_set()
    last_radius = 0.0
    canvas.delete("all")
    # draw only the 1 cm reference when cleared
    draw_circles(0)

def draw_circles(user_r_cm: float):
    canvas.delete("all")

    # use current canvas size so drawing scales when window is resized
    cw = max(canvas.winfo_width(), 1)
    ch = max(canvas.winfo_height(), 1)

    # Layout: two circles side-by-side with padding
    available_width = (cw - 3 * PADDING) / 2.0
    available_height = ch - 2 * PADDING
    # Determine scale so both circles fit (use max radius among user and reference)
    max_radius_cm = max(user_r_cm, REF_RADIUS_CM, 0.001)
    scale = min(BASE_SCALE, available_width / (2 * max_radius_cm), available_height / (2 * max_radius_cm))
    # If user radius is zero, still show a small marker
    user_px = max(2.0, user_r_cm * scale)
    ref_px = max(2.0, REF_RADIUS_CM * scale)

    left_center_x = PADDING + available_width / 2.0
    right_center_x = left_center_x + available_width + PADDING
    center_y = ch / 2.0

    # Draw user's circle (if radius > 0 show proportionally, else a small dot)
    if user_r_cm > 0:
        canvas.create_oval(
            left_center_x - user_px, center_y - user_px,
            left_center_x + user_px, center_y + user_px,
            outline="#1565C0", width=2, fill="#E3F2FD"
        )
    else:
        canvas.create_oval(
            left_center_x - user_px, center_y - user_px,
            left_center_x + user_px, center_y + user_px,
            outline="#1565C0", width=2, fill="#1565C0"
        )

    # Draw 1 cm reference circle
    canvas.create_oval(
        right_center_x - ref_px, center_y - ref_px,
        right_center_x + ref_px, center_y + ref_px,
        outline="#555555", width=2, dash=(2, 2)
    )

    # Labels
    canvas.create_text(left_center_x, center_y + max(user_px, ref_px) + 14,
                       text=f"Your circle: {user_r_cm} cm" if user_r_cm > 0 else "Your circle: 0 cm",
                       fill="#1565C0", font=("Arial", 10))
    canvas.create_text(right_center_x, center_y + ref_px + 14,
                       text=f"Reference: {REF_RADIUS_CM} cm", fill="#333333", font=("Arial", 10))

    # Scale legend
    canvas.create_text(PADDING, 10, anchor="nw",
                       text=f"Scale: {scale:.1f} px/cm", fill="#000", font=("Arial", 9))

root = tk.Tk()
root.title("Circle Area Calculator")
# make the window resizable
root.resizable(True, True)

frame = tk.Frame(root, padx=10, pady=10)
# allow frame to expand with the window
frame.pack(fill="both", expand=True)

# Left: inputs
left_frame = tk.Frame(frame)
left_frame.grid(row=0, column=0, sticky="n")

tk.Label(left_frame, text="Radius (cm):").grid(row=0, column=0, sticky="e")
entry_radius = tk.Entry(left_frame, width=20)
entry_radius.grid(row=0, column=1, padx=(5,0))
entry_radius.focus_set()

# colored buttons
btn_calc = tk.Button(left_frame, text="Calculate", command=calculate_area,
                     bg="#6FBC72", fg="white", activebackground="#6FBC72", activeforeground="white")
btn_calc.grid(row=1, column=0, pady=10, sticky="ew", columnspan=1)

btn_clear = tk.Button(left_frame, text="Clear", command=clear,
                      bg="#BD7DD2", fg="white", activebackground="#BD7DD2", activeforeground="white")
btn_clear.grid(row=1, column=1, pady=10, sticky="ew", columnspan=1)

label_result = tk.Label(left_frame, text="Area (cm²):", anchor="w")
label_result.grid(row=2, column=0, columnspan=2, sticky="w")

# Right: canvas for drawing
canvas = tk.Canvas(frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white", bd=1, relief="sunken")
# allow canvas to expand when window is resized
canvas.grid(row=0, column=1, padx=(12,0), sticky="nsew")

# make the canvas column expand
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Bind Enter key to calculation
root.bind("<Return>", calculate_area)

# redraw when canvas size changes (window resize)
canvas.bind("<Configure>", lambda e: draw_circles(last_radius))

# Initial draw: show only reference circle
draw_circles(0)

root.mainloop()