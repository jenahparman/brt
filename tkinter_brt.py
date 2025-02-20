import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import os
from tkinter import filedialog, messagebox

# Define all shop curves
# Define all curves in a dictionary for easier management
curves = {
    "ELE" : [
        0.13,	0.19,	0.29,	0.58,	1.16,	1.62,	2.10,	2.19,	2.30,	2.39,	
        2.49,	2.51,	2.57,	2.50,	2.49,	2.49,	2.40,	2.40,	2.40,	2.32,	
        2.31,	2.31,	2.31,	2.23,	2.13,	2.14,	2.14,	2.14,	2.23,	2.23,	
        2.31,	2.31,	2.31,	2.31,	2.40,	2.40,	2.40,	2.31,	2.22,	2.09,	
        1.93,	1.81,	1.63,	1.60,	1.62,	1.89,	1.97,	1.89,	1.71,	1.20
    ],

    "ISM" : [
        0.35,	0.54,	0.79,	1.44,	1.67,	1.76,	2.29,	2.73,	3.75,	4.95,	
        5.54,	6.14,	6.14,	6.44,	6.44,	6.29,	6.29,	5.99,	5.31,	4.29,	
        3.51,	3.00,	2.97,	2.83,	2.64,	2.31,	2.10,	1.50,	0.00,	0.00,	
        0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	
        0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
    ],

    "OSM" : [
        0.22,	0.33,	0.50,	1.00,	2.01,	2.61,	2.87,	2.99,	3.13,	3.28,	
        3.35,	3.32,	3.19,	3.06,	2.90,	2.70,	2.60,	2.56,	2.60,	2.70,	
        2.79,	2.90,	3.01,	3.07,	3.08,	3.09,	3.09,	3.09,	2.99,	2.77,	
        2.67,	2.67,	2.58,	2.52,	2.38,	2.24,	1.93,	1.65,	1.33,	1.04,	
        0.73,	0.00,	0.00,	0.00,	0.00,	0.11,	0.12,	0.12,	0.11,	0.00,
    ],

    "PIP" : [
        0.14,	0.20,	0.30,	1.04,	1.22,	1.70,	1.96,	2.09,	2.05,	2.04,	
        2.04,	2.11,	2.21,	2.31,	2.39,	2.42,	2.48,	2.61,	2.65,	2.64,	
        2.63,	2.62,	2.60,	2.54,	2.33,	2.54,	2.54,	2.54,	2.54,	2.53,	
        2.53,	2.53,	2.53,	2.53,	2.49,	2.43,	2.37,	2.26,	2.18,	2.13,	
        2.07,	1.98,	1.90,	1.80,	1.69,	1.55,	1.25,	0.98,	0.47,	0.32
    ],

    "PSF" : [
        0.17,	0.26,	0.39,	0.77,	1.55,	2.32,	3.00,	3.14,	3.29,	3.45,	
        3.60,	3.75,	3.92,	3.92,	3.97,	3.98,	4.04,	4.13,	4.21,	4.14,	
        4.06,	4.02,	3.98,	3.85,	3.06,	2.49,	2.44,	2.40,	2.22,	2.15,	
        1.97,	1.70,	1.43,	1.33,	1.34,	1.21,	0.83,	0.89,	0.63,	0.00,	
        0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
    ],

    "SHM" : [
        0.14,	0.20,	0.31,	0.63,	1.26,	1.76,	2.29,	2.38,	2.48,	2.60,	
        2.73,	2.87,	3.00,	3.03,	3.05,	3.09,	3.14,	3.16,	3.20,	3.21,	
        3.21,	3.21,	3.21,	2.93,	2.70,	2.93,	2.93,	2.93,	2.93,	2.48,	
        2.48,	2.48,	2.48,	2.48,	2.48,	2.29,	2.09,	1.90,	1.71,	1.51,	
        1.32,	1.12,	0.93,	0.74,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
    ],

    "WLD" : [
        0.16,	0.24,	0.36,	1.03,	1.44,	2.07,	2.50,	2.67,	2.70,	2.70,	
        2.77,	2.87,	3.00,	3.08,	3.15,	3.17,	3.24,	3.24,	3.17,	3.08,	
        3.05,	3.01,	2.98,	2.94,	2.63,	2.65,	2.70,	2.68,	2.65,	2.62,	
        2.56,	2.46,	2.37,	2.34,	2.31,	2.21,	1.97,	1.85,	1.67,	1.51,	
        1.34,	1.21,	0.96,	0.69,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
    ],


    "CRP" : [
        0.19,	0.28,	0.43,	0.85,	1.70,	2.22,	2.88,	3.01,	3.16,	3.11,	
        3.08,	3.00,	2.98,	2.93,	2.91,	2.83,	2.78,	2.76,	2.80,	2.85,	
        2.92,	3.00,	3.03,	3.07,	3.06,	3.00,	2.93,	2.85,	2.73,	2.71,	
        2.67,	2.57,	2.42,	2.18,	1.93,	1.90,	1.87,	1.59,	1.34,	1.27,	
        1.19,	1.14,	1.07,	0.81,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
    ],

    "LAB" : [
        0.22,	0.38,	0.78,	1.03,	1.64,	1.83,	1.88,	1.97,	1.98,	1.98,	
        2.31,	2.45,	2.67,	2.99,	3.21,	3.42,	3.44,	3.47,	3.43,	3.38,	
        3.32,	3.12,	2.92,	2.83,	2.86,	2.74,	2.74,	2.72,	2.51,	2.41,	
        2.20,	1.90,	1.87,	1.86,	1.86,	1.81,	1.75,	1.53,	1.36,	1.00,	
        0.83,	0.76,	1.08,	1.30,	1.38,	1.47,	1.38,	0.99,	0.87,	0.17
    ],


    "LAG" : [
        0.82,	0.97,	1.03,	1.16,	1.36,	1.46,	1.54,	1.57,	1.73,	1.72,	
        1.74,	1.75,	1.74,	1.66,	1.62,	1.58,	1.56,	1.54,	1.52,	1.58,	
        1.65,	1.71,	1.78,	1.80,	1.93,	2.07,	2.15,	2.16,	2.20,	2.30,	
        2.44,	2.50,	2.61,	2.63,	2.67,	2.73,	2.78,	2.79,	2.80,	2.70,	
        2.62,	2.53,	2.52,	2.39,	2.40,	2.40,	2.40,	2.33,	2.23,	2.13
    ],

    "PNT" : [
        0.82,	0.97,	1.03,	1.16,	1.36,	1.46,	1.54,	1.57,	1.73,	1.72,	
        1.74,	1.75,	1.74,	1.66,	1.62,	1.58,	1.56,	1.54,	1.52,	1.58,	
        1.65,	1.71,	1.78,	1.80,	1.93,	2.07,	2.15,	2.16,	2.20,	2.30,	
        2.44,	2.50,	2.61,	2.63,	2.67,	2.73,	2.78,	2.79,	2.80,	2.70,	
        2.62,	2.53,	2.52,	2.39,	2.40,	2.40,	2.40,	2.33,	2.23,	2.13
    ],

    "RIG" : [
        0.12,	0.18,	0.27,	0.53,	1.06,	1.59,	1.91,	1.99,	2.07,	2.16,	
        2.24,	2.33,	2.44,	2.46,	2.47,	2.48,	2.49,	2.49,	2.49,	2.48,	
        2.46,	2.44,	2.39,	2.31,	2.23,	2.31,	2.31,	2.31,	2.31,	2.22,	
        2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	
        2.22,	2.17,	2.12,	2.10,	2.05,	1.80,	1.61,	1.52,	1.38,	1.29

    ],

    "SUB" : [
        0.11,	0.20,	0.34,	0.65,	1.12,	1.59,	1.88,	2.12,	2.29,	2.38,	
        2.51,	2.62,	2.67,	2.79,	2.86,	2.86,	2.86,	2.88,	2.90,	2.89,	
        2.89,	2.89,	2.90,	2.89,	2.87,	2.83,	2.83,	2.82,	2.75,	2.64,	
        2.57,	2.50,	2.42,	2.38,	2.34,	2.26,	2.07,	1.96,	1.79,	1.56,	
        1.43,	1.18,	1.13,	1.08,	0.95,	0.89,	0.80,	0.73,	0.62,	0.51
    ]
}

redistribute_hours = []

# Normalize the curves
for key in curves:
    curves[key] = curves[key] / np.sum(curves[key])

# Function to scale a curve to a new number of weeks
def scale_curve(percentages, original_weeks, new_weeks):
    original_x = np.linspace(0, 1, original_weeks)
    new_x = np.linspace(0, 1, new_weeks)
    interpolation_function = interp1d(original_x, percentages, kind='linear')
    scaled_curve = interpolation_function(new_x)
    return scaled_curve / np.sum(scaled_curve)

# Function to redistribute hours
def redistribute_hours(total_hours, num_weeks, curve):
    original_weeks = len(curve)
    scaled_curve = scale_curve(curve, original_weeks, num_weeks)
    return total_hours * scaled_curve

# Function to handle batch entry
def process_batch():
    try:
        num_weeks = int(weeks_entry.get())
        if num_weeks <= 0:
            messagebox.showerror("Input Error", "Number of weeks must be greater than 0.")
            return

        results = {}

        for shop, entry in shop_entries.items():
            total_hours = entry.get().strip()
            if total_hours:
                total_hours = float(total_hours)
                results[shop] = redistribute_hours(total_hours, num_weeks, curves[shop])

        # Create DataFrame
        df = pd.DataFrame(results).T
        df.columns = [f"Week {i+1}" for i in range(num_weeks)]
        
        messagebox.showinfo("Success", "PDFs parsed successfully! Press 'Save to Excel' to save hours.")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for all fields.")

def save_to_excel():
    folder_selected = filedialog.askdirectory(title="Select Folder to Save Files")

    if not folder_selected:
        return
    redistributed_hours_file = os.path.join(folder_selected, rf"Redistributed Hours.xlsx")

    redistributed_hours = pd.DataFrame()

    with pd.ExcelWriter(redistributed_hours_file) as writer:
        redistribute_hours.to_excel(writer, sheet_name='Redistributed Hours', index=False)

    messagebox.showinfo("Success", f"File saved:\n{redistributed_hours_file}")


# Create Tkinter window
root = tk.Tk()
root.title("Budget Redistribution Tool")
root.geometry("500x600")

# Number of Weeks Entry
tk.Label(root, text="Enter Desired Number of Weeks:", font=("Dubai", 12)).pack(pady=(15,2))
weeks_entry = tk.Entry(root, width=7)
weeks_entry.pack(pady=(2,5))

# Shop Entry Fields
shop_entries = {}
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter Shop Hours:", font=("Dubai", 12)).grid(row=0, column=1, padx=5)
for i, shop in enumerate(curves.keys()):
    tk.Label(frame, text=f"{shop}:").grid(row=i+1, column=0, sticky="e", padx=5)
    entry = tk.Entry(frame, width=10)
    entry.grid(row=i+1, column=1, padx=5)
    shop_entries[shop] = entry

# Process Button
tk.Button(root, text="Redistribute Hours", command=process_batch, font=("Dubai", 10)).pack(pady=10)

tk.Button(root, text="Save to Excel", command=save_to_excel, font=("Dubai", 10)).pack(pady=10)


# Run Tkinter Loop
root.mainloop()
