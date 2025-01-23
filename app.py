import numpy as np
import pandas as pd
import streamlit as st
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

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
    if curve_type == 'linear':
        curve = np.ones(num_weeks)
    elif curve_type == 'bell':
        curve = np.exp(-0.5 * (np.linspace(-2, 2, num_weeks) ** 2))
    elif curve_type == 'front_loaded':
        curve = np.linspace(1.5, 0.5, num_weeks)
    elif curve_type == 'back_loaded':
        curve = np.linspace(0.5, 1.5, num_weeks)
    elif curve_type == 'fitted' and percentages is not None and original_weeks is not None:
        # Scale the original curve to match the new number of weeks
        curve = scale_curve(percentages, original_weeks, num_weeks)
    elif curve_type == 'custom' and custom_curve:
        curve = np.array(custom_curve)
    else:
        st.error("Invalid curve type or input data.")
        return None

    # Normalize the curve so the sum equals 1
    normalized_curve = curve / np.sum(curve)

    # Redistribute the hours
    redistributed_hours = total_hours * normalized_curve

    weeks = [f"Week {i+1}" for i in range(num_weeks)]
    return pd.DataFrame({'Week': weeks, 'Redistributed Hours': redistributed_hours})

# Streamlit app
st.title("Budget Redistribution Tool")

# Inputs
total_hours = st.number_input("Total Hours Budget", min_value=0.0, value=1000.0, step=100.0)
num_weeks = st.slider("Number of Weeks (Target)", min_value=1, max_value=200, value=50)
curve_type = st.selectbox("Curve Shape", options=['linear', 'bell', 'front_loaded', 'back_loaded', 'fitted', 'custom'])

custom_curve = None
percentages = None
original_weeks = None

if curve_type == 'custom':
    custom_curve_input = st.text_area(
        f"Enter {num_weeks} values separated by commas (e.g., 0.1, 0.2, 0.3...):", ""
    )
    if custom_curve_input.strip():
        try:
            # Parse the custom input into a list of floats
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
            st.write("Redistributed Hours:")
            st.write(df)
            st.download_button("Download as CSV", df.to_csv(index=False), file_name="redistributed_hours.csv")

            # Optional: Plot the curve
            if curve_type == 'fitted' and percentages is not None and original_weeks is not None:
                scaled_curve = scale_curve(percentages, original_weeks, num_weeks)
                plt.plot(np.linspace(0, num_weeks, num_weeks), scaled_curve, label="Scaled Curve")
                plt.xlabel("Weeks")
                plt.ylabel("Redistributed Fraction")
                plt.title("Scaled Curve")
                plt.legend()
                st.pyplot(plt)
