import numpy as np
import pandas as pd
import streamlit as st
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# Define all curves in a dictionary for easier management
curves = {
    "ELE": [
        0.13, 0.19, 0.29, 0.58, 1.16, 1.62, 2.10, 2.19, 2.30, 2.39, 2.49, 2.51, 2.57,
        2.50, 2.49, 2.49, 2.40, 2.40, 2.40, 2.32, 2.31, 2.31, 2.31, 2.23, 2.13, 2.14,
        2.14, 2.14, 2.23, 2.23, 2.31, 2.31, 2.31, 2.31, 2.40, 2.40, 2.40, 2.31, 2.22,
        2.09, 1.93, 1.81, 1.63, 1.60, 1.62, 1.89, 1.97, 1.89, 1.71, 1.20
    ],
    "ISM": [
        0.35, 0.54, 0.79, 1.44, 1.67, 1.76, 2.29, 2.73, 3.75, 4.95, 5.54, 6.14, 6.14,
        6.44, 6.44, 6.29, 6.29, 5.99, 5.31, 4.29, 3.51, 3.00, 2.97, 2.83, 2.64, 2.31,
        2.10, 1.50, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
        0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00
    ],
    # Add other curves (OSM, PIP, etc.) similarly
}

# Normalize curves
normalized_curves = {
    name: [p / sum(values) for p in values] for name, values in curves.items()
}

# Function to scale a curve to a new number of weeks
def scale_curve(percentages, original_weeks, new_weeks):
    original_x = np.linspace(0, 1, original_weeks)  # Original weeks scaled to [0, 1]
    new_x = np.linspace(0, 1, new_weeks)  # New weeks scaled to [0, 1]

    # Interpolate the original curve
    interpolation_function = interp1d(original_x, percentages, kind='linear')
    scaled_curve = interpolation_function(new_x)

    # Normalize the scaled curve to ensure it sums to 1
    normalized_scaled_curve = scaled_curve / np.sum(scaled_curve)
    return normalized_scaled_curve

# Function to redistribute hours based on the curve
def redistribute_hours(total_hours, num_weeks, curve_type, custom_curve=None, percentages=None, original_weeks=None):
    if curve_type in normalized_curves:
        # Use predefined normalized curve
        curve = scale_curve(normalized_curves[curve_type], len(curves[curve_type]), num_weeks)
    elif curve_type == 'linear':
        curve = np.ones(num_weeks) / num_weeks
    elif curve_type == 'bell':
        curve = np.exp(-0.5 * (np.linspace(-2, 2, num_weeks) ** 2))
        curve /= np.sum(curve)  # Normalize
    elif curve_type == 'front_loaded':
        curve = np.linspace(1.5, 0.5, num_weeks)
        curve /= np.sum(curve)  # Normalize
    elif curve_type == 'back_loaded':
        curve = np.linspace(0.5, 1.5, num_weeks)
        curve /= np.sum(curve)  # Normalize
    elif curve_type == 'custom' and custom_curve:
        curve = np.array(custom_curve) / np.sum(custom_curve)  # Normalize
    elif curve_type == 'fitted' and percentages and original_weeks:
        curve = scale_curve(percentages, original_weeks, num_weeks)
    else:
        st.error("Invalid curve type or input data.")
        return None

    # Redistribute the hours
    redistributed_hours = total_hours * curve
    weeks = [f"Week {i+1}" for i in range(num_weeks)]
    return pd.DataFrame({'Week': weeks, 'Redistributed Hours': redistributed_hours, 'Curve Value': curve})

# Streamlit app
st.title("Budget Redistribution Tool")

# Inputs
total_hours = st.number_input("Total Hours Budget", min_value=0.0, value=1000.0, step=100.0)
num_weeks = st.number_input("Enter desired number of weeks", min_value=1, max_value=200, value=50)
curve_type = st.selectbox(
    "Curve Shape",
    options=list(normalized_curves.keys()) + ['linear', 'bell', 'front_loaded', 'back_loaded', 'fitted', 'custom']
)

custom_curve = None
percentages = None
original_weeks = None

if curve_type == 'custom':
    custom_curve_input = st.text_area(
        f"Enter {num_weeks} values separated by commas (e.g., 0.1, 0.2, 0.3...):", ""
    )
    if custom_curve_input.strip():
        try:
            custom_curve = list(map(float, custom_curve_input.strip().split(',')))
            if len(custom_curve) != num_weeks:
                st.error(f"Please enter exactly {num_weeks} values.")
                custom_curve = None
        except ValueError:
            st.error("Invalid input. Ensure all values are numbers separated by commas.")
            custom_curve = None

if curve_type == 'fitted':
    original_weeks = st.number_input("Original Number of Weeks for the Curve", min_value=1, max_value=200, value=77)
    percentage_input = st.text_area(
        f"Enter {original_weeks} percentages (comma-separated, summing to 100):", ""
    )
    if percentage_input.strip():
        try:
            percentages = list(map(float, percentage_input.strip().split(',')))
            if len(percentages) != original_weeks:
                st.error(f"Please enter exactly {original_weeks} percentages.")
                percentages = None
            elif abs(sum(percentages) - 100) > 1e-6:
                st.error("Percentages must sum to 100.")
                percentages = None
        except ValueError:
            st.error("Invalid input. Ensure all values are numbers separated by commas.")
            percentages = None

if st.button("Redistribute Hours"):
    if (curve_type == 'custom' and custom_curve is None) or (curve_type == 'fitted' and (percentages is None or original_weeks is None)):
        st.warning("Please provide valid input for the selected curve type.")
    else:
        df = redistribute_hours(total_hours, num_weeks, curve_type, custom_curve, percentages, original_weeks)
        if df is not None:
            # Display the DataFrame
            st.write("Redistributed Hours:")
            st.dataframe(df)

            # Plot the curve
            plt.figure(figsize=(10, 6))
            plt.plot(df['Week'], df['Curve Value'], label=f"{curve_type} Curve", marker="o")
            plt.xlabel("Weeks")
            plt.ylabel("Redistributed Fraction")
            plt.xticks(range(0, num_weeks, max(1, num_weeks // 10)))  # Show ticks every ~10 weeks
            plt.title(f"{curve_type.capitalize()} Curve")
            plt.grid(True)
            plt.legend()
            st.pyplot(plt)

            # Save to Excel
            output_excel = pd.ExcelWriter("redistributed_hours.xlsx", engine='xlsxwriter')
            df.to_excel(output_excel, index=False, sheet_name="Redistribution")
            output_excel.save()

            st.download_button(
                "Download Excel File",
                data=open("redistributed_hours.xlsx", "rb"),
                file_name="redistributed_hours.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )