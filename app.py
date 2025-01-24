import numpy as np
import pandas as pd
import streamlit as st
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

ELE_curve = [
    0.13,	0.19,	0.29,	0.58,	1.16,	1.62,	2.10,	2.19,	2.30,	2.39,	
    2.49,	2.51,	2.57,	2.50,	2.49,	2.49,	2.40,	2.40,	2.40,	2.32,	
    2.31,	2.31,	2.31,	2.23,	2.13,	2.14,	2.14,	2.14,	2.23,	2.23,	
    2.31,	2.31,	2.31,	2.31,	2.40,	2.40,	2.40,	2.31,	2.22,	2.09,	
    1.93,	1.81,	1.63,	1.60,	1.62,	1.89,	1.97,	1.89,	1.71,	1.20
]

ISM_curve = [
    0.35,	0.54,	0.79,	1.44,	1.67,	1.76,	2.29,	2.73,	3.75,	4.95,	
    5.54,	6.14,	6.14,	6.44,	6.44,	6.29,	6.29,	5.99,	5.31,	4.29,	
    3.51,	3.00,	2.97,	2.83,	2.64,	2.31,	2.10,	1.50,	0.00,	0.00,	
    0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	
    0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
]

OSM_curve = [
    0.22,	0.33,	0.50,	1.00,	2.01,	2.61,	2.87,	2.99,	3.13,	3.28,	
    3.35,	3.32,	3.19,	3.06,	2.90,	2.70,	2.60,	2.56,	2.60,	2.70,	
    2.79,	2.90,	3.01,	3.07,	3.08,	3.09,	3.09,	3.09,	2.99,	2.77,	
    2.67,	2.67,	2.58,	2.52,	2.38,	2.24,	1.93,	1.65,	1.33,	1.04,	
    0.73,	0.00,	0.00,	0.00,	0.00,	0.11,	0.12,	0.12,	0.11,	0.00,
]

PIP_curve = [
    0.14,	0.20,	0.30,	1.04,	1.22,	1.70,	1.96,	2.09,	2.05,	2.04,	
    2.04,	2.11,	2.21,	2.31,	2.39,	2.42,	2.48,	2.61,	2.65,	2.64,	
    2.63,	2.62,	2.60,	2.54,	2.33,	2.54,	2.54,	2.54,	2.54,	2.53,	
    2.53,	2.53,	2.53,	2.53,	2.49,	2.43,	2.37,	2.26,	2.18,	2.13,	
    2.07,	1.98,	1.90,	1.80,	1.69,	1.55,	1.25,	0.98,	0.47,	0.32
]

PSF_curve = [
    0.17,	0.26,	0.39,	0.77,	1.55,	2.32,	3.00,	3.14,	3.29,	3.45,	
    3.60,	3.75,	3.92,	3.92,	3.97,	3.98,	4.04,	4.13,	4.21,	4.14,	
    4.06,	4.02,	3.98,	3.85,	3.06,	2.49,	2.44,	2.40,	2.22,	2.15,	
    1.97,	1.70,	1.43,	1.33,	1.34,	1.21,	0.83,	0.89,	0.63,	0.00,	
    0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
]

SHM_curve = [
    0.14,	0.20,	0.31,	0.63,	1.26,	1.76,	2.29,	2.38,	2.48,	2.60,	
    2.73,	2.87,	3.00,	3.03,	3.05,	3.09,	3.14,	3.16,	3.20,	3.21,	
    3.21,	3.21,	3.21,	2.93,	2.70,	2.93,	2.93,	2.93,	2.93,	2.48,	
    2.48,	2.48,	2.48,	2.48,	2.48,	2.29,	2.09,	1.90,	1.71,	1.51,	
    1.32,	1.12,	0.93,	0.74,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
]

WLD_curve = [
    0.16,	0.24,	0.36,	1.03,	1.44,	2.07,	2.50,	2.67,	2.70,	2.70,	
    2.77,	2.87,	3.00,	3.08,	3.15,	3.17,	3.24,	3.24,	3.17,	3.08,	
    3.05,	3.01,	2.98,	2.94,	2.63,	2.65,	2.70,	2.68,	2.65,	2.62,	
    2.56,	2.46,	2.37,	2.34,	2.31,	2.21,	1.97,	1.85,	1.67,	1.51,	
    1.34,	1.21,	0.96,	0.69,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
]


CRP_curve = [
    0.19,	0.28,	0.43,	0.85,	1.70,	2.22,	2.88,	3.01,	3.16,	3.11,	
    3.08,	3.00,	2.98,	2.93,	2.91,	2.83,	2.78,	2.76,	2.80,	2.85,	
    2.92,	3.00,	3.03,	3.07,	3.06,	3.00,	2.93,	2.85,	2.73,	2.71,	
    2.67,	2.57,	2.42,	2.18,	1.93,	1.90,	1.87,	1.59,	1.34,	1.27,	
    1.19,	1.14,	1.07,	0.81,	0.00,	0.00,	0.00,	0.00,	0.00,	0.00
]

LAB_curve = [
    0.22,	0.38,	0.78,	1.03,	1.64,	1.83,	1.88,	1.97,	1.98,	1.98,	
    2.31,	2.45,	2.67,	2.99,	3.21,	3.42,	3.44,	3.47,	3.43,	3.38,	
    3.32,	3.12,	2.92,	2.83,	2.86,	2.74,	2.74,	2.72,	2.51,	2.41,	
    2.20,	1.90,	1.87,	1.86,	1.86,	1.81,	1.75,	1.53,	1.36,	1.00,	
    0.83,	0.76,	1.08,	1.30,	1.38,	1.47,	1.38,	0.99,	0.87,	0.17
]


LAG_curve = [
    0.82,	0.97,	1.03,	1.16,	1.36,	1.46,	1.54,	1.57,	1.73,	1.72,	
    1.74,	1.75,	1.74,	1.66,	1.62,	1.58,	1.56,	1.54,	1.52,	1.58,	
    1.65,	1.71,	1.78,	1.80,	1.93,	2.07,	2.15,	2.16,	2.20,	2.30,	
    2.44,	2.50,	2.61,	2.63,	2.67,	2.73,	2.78,	2.79,	2.80,	2.70,	
    2.62,	2.53,	2.52,	2.39,	2.40,	2.40,	2.40,	2.33,	2.23,	2.13
]

PNT_curve = [
    0.82,	0.97,	1.03,	1.16,	1.36,	1.46,	1.54,	1.57,	1.73,	1.72,	
    1.74,	1.75,	1.74,	1.66,	1.62,	1.58,	1.56,	1.54,	1.52,	1.58,	
    1.65,	1.71,	1.78,	1.80,	1.93,	2.07,	2.15,	2.16,	2.20,	2.30,	
    2.44,	2.50,	2.61,	2.63,	2.67,	2.73,	2.78,	2.79,	2.80,	2.70,	
    2.62,	2.53,	2.52,	2.39,	2.40,	2.40,	2.40,	2.33,	2.23,	2.13
]

RIG_curve = [
    0.12,	0.18,	0.27,	0.53,	1.06,	1.59,	1.91,	1.99,	2.07,	2.16,	
    2.24,	2.33,	2.44,	2.46,	2.47,	2.48,	2.49,	2.49,	2.49,	2.48,	
    2.46,	2.44,	2.39,	2.31,	2.23,	2.31,	2.31,	2.31,	2.31,	2.22,	
    2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	2.22,	
    2.22,	2.17,	2.12,	2.10,	2.05,	1.80,	1.61,	1.52,	1.38,	1.29

]

SUB_curve = [
    0.11,	0.20,	0.34,	0.65,	1.12,	1.59,	1.88,	2.12,	2.29,	2.38,	
    2.51,	2.62,	2.67,	2.79,	2.86,	2.86,	2.86,	2.88,	2.90,	2.89,	
    2.89,	2.89,	2.90,	2.89,	2.87,	2.83,	2.83,	2.82,	2.75,	2.64,	
    2.57,	2.50,	2.42,	2.38,	2.34,	2.26,	2.07,	1.96,	1.79,	1.56,	
    1.43,	1.18,	1.13,	1.08,	0.95,	0.89,	0.80,	0.73,	0.62,	0.51
]

ELE_curve_normalized = [p / sum(ELE_curve) for p in ELE_curve]
ISM_curve_normalized = [p / sum(ISM_curve) for p in ISM_curve]
OSM_curve_normalized = [p / sum(OSM_curve) for p in OSM_curve]
PIP_curve_normalized = [p / sum(PIP_curve) for p in PIP_curve]
PSF_curve_normalized = [p / sum(PSF_curve) for p in PSF_curve]
SHM_curve_normalized = [p / sum(SHM_curve) for p in SHM_curve]
WLD_curve_normalized = [p / sum(WLD_curve) for p in WLD_curve]
CRP_curve_normalized = [p / sum(CRP_curve) for p in CRP_curve]
LAB_curve_normalized = [p / sum(LAB_curve) for p in LAB_curve]
LAG_curve_normalized = [p / sum(LAG_curve) for p in LAG_curve]
PNT_curve_normalized = [p / sum(PNT_curve) for p in PNT_curve]
RIG_curve_normalized = [p / sum(RIG_curve) for p in RIG_curve]
SUB_curve_normalized = [p / sum(SUB_curve) for p in SUB_curve]

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
    elif curve_type == 'ELE':
        curve = scale_curve(ELE_curve_normalized, len(ELE_curve_normalized), num_weeks)
    elif curve_type == 'ISM':
        curve = scale_curve(ISM_curve_normalized, len(ISM_curve_normalized), num_weeks)
    elif curve_type == 'OSM':
        curve = scale_curve(OSM_curve_normalized, len(OSM_curve_normalized), num_weeks)
    elif curve_type == 'PIP':
        curve = scale_curve(PIP_curve_normalized, len(PIP_curve_normalized), num_weeks)
    elif curve_type == 'PSF':
        curve = scale_curve(PSF_curve_normalized, len(PSF_curve_normalized), num_weeks)
    elif curve_type == 'SHM':
        curve = scale_curve(SHM_curve_normalized, len(SHM_curve_normalized), num_weeks)
    elif curve_type == 'WLD':
        curve = scale_curve(WLD_curve_normalized, len(WLD_curve_normalized), num_weeks)
    elif curve_type == 'CRP':
        curve = scale_curve(CRP_curve_normalized, len(CRP_curve_normalized), num_weeks)
    elif curve_type == 'LAB':
        curve = scale_curve(LAB_curve_normalized, len(LAB_curve_normalized), num_weeks)
    elif curve_type == 'LAG':
        curve = scale_curve(LAG_curve_normalized, len(LAG_curve_normalized), num_weeks)
    elif curve_type == 'PNT':
        curve = scale_curve(PNT_curve_normalized, len(PNT_curve_normalized), num_weeks)
    elif curve_type == 'RIG':
        curve = scale_curve(RIG_curve_normalized, len(RIG_curve_normalized), num_weeks)
    elif curve_type == 'SUB':
        curve = scale_curve(SUB_curve_normalized, len(SUB_curve_normalized), num_weeks)

    # Normalize the curve so the sum equals 1
    normalized_curve = curve / np.sum(curve)

    # Redistribute the hours
    redistributed_hours = total_hours * normalized_curve

    weeks = [f"Week {i+1}" for i in range(num_weeks)]


    if curve is not None:
        plt.figure(figsize=(16,10))
        plt.plot(weeks, curve, label=f"{curve_type} Curve", marker="o")
        plt.xlabel("Weeks")
        plt.ylabel("Redistributed Fraction")
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.error("Invalid curve type or input data.")
        return None

    return pd.DataFrame({'Week': weeks, 'Redistributed Hours': redistributed_hours})



# Streamlit app
st.title("Budget Redistribution Tool")

# Inputs
total_hours = st.number_input("Total Hours Budget", min_value=0.0, value=1000.0, step=100.0)
num_weeks = st.number_input("Enter desired number of weeks", min_value=1, max_value=200, value=50)
curve_type = st.selectbox(
    "Curve Shape", 
    options=['ELE','ISM','OSM','PIP','SHM','WLD','CRP','LAB','LAG','PNT','RIG','SUB','linear', 'bell', 'front_loaded', 'back_loaded', 'fitted', 'custom'])

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

