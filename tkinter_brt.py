import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import openpyxl

# Define all shop curves
curves = {
    "ELE": np.array([0.13, 0.19, 0.29, 0.58, 1.16, 1.62, 2.10, 2.19, 2.30, 2.39]),
    "ISM": np.array([0.35, 0.54, 0.79, 1.44, 1.67, 1.76, 2.29, 2.73, 3.75, 4.95]),
    "OSM": np.array([0.22, 0.33, 0.50, 1.00, 2.01, 2.61, 2.87, 2.99, 3.13, 3.28]),
    "PIP": np.array([0.14, 0.20, 0.30, 1.04, 1.22, 1.70, 1.96, 2.09, 2.05, 2.04]),
    "PSF": np.array([0.17, 0.26, 0.39, 0.77, 1.55, 2.32, 3.00, 3.14, 3.29, 3.45])
}

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
        
        # Show results in the table
        for i in result_tree.get_children():
            result_tree.delete(i)
        for shop, values in df.iterrows():
            result_tree.insert("", "end", values=[shop] + list(values))

        # Save results to Excel
        df.to_excel("redistributed_hours.xlsx", index=True)
        messagebox.showinfo("Success", "Redistributed hours saved as 'redistributed_hours.xlsx'.")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for all fields.")

# Create Tkinter window
root = tk.Tk()
root.title("Budget Redistribution Tool")
root.geometry("600x500")

# Number of Weeks Entry
tk.Label(root, text="Enter Desired Number of Weeks:").pack(pady=5)
weeks_entry = tk.Entry(root)
weeks_entry.pack(pady=5)

# Shop Entry Fields
shop_entries = {}
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter Hours for Each Shop Type:", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)
for i, shop in enumerate(curves.keys()):
    tk.Label(frame, text=f"{shop}:").grid(row=i+1, column=0, sticky="e", padx=5)
    entry = tk.Entry(frame, width=10)
    entry.grid(row=i+1, column=1, padx=5)
    shop_entries[shop] = entry

# Process Button
tk.Button(root, text="Redistribute Hours", command=process_batch).pack(pady=10)

# Results Table
tk.Label(root, text="Results (Shops as Rows, Weeks as Columns):").pack()
result_tree = ttk.Treeview(root, columns=["Shop"] + [f"Week {i+1}" for i in range(10)], show="headings")
result_tree.pack(expand=True, fill="both")

# Set column headings
result_tree.heading("Shop", text="Shop")
for i in range(10):
    result_tree.heading(f"Week {i+1}", text=f"Week {i+1}")

# Run Tkinter Loop
root.mainloop()
