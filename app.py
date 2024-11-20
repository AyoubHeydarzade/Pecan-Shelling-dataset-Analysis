#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.factorplots import interaction_plot

# Title for the app
st.title('Pecan Project- Shelling Dataset - Statistical Analysis')

# Step 1: Upload dataset
st.subheader("Upload your dataset (Excel format)")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

# If a file is uploaded
if uploaded_file is not None:
    # Load the dataset into a dataframe
    full_data = pd.read_excel(uploaded_file)
    
    # Display the entire dataset
    st.write("Here is the full dataset:")
    st.write(full_data)

    # Add Summary Statistics for Output Variables
    st.subheader("Summary Statistics for Output Variables")
    
    # Specify the columns to summarize
    summary_columns = [
        "Intact Halves (%)",
        "Weight dist1. (%)",
        "Weight dist2. (%)",
        "Weight dist3. (%)",
        "Discharge Throughput (lbs. %)",
        "Loss (%)"
    ]
    
    # Filter and calculate summary statistics
    if all(col in full_data.columns for col in summary_columns):  # Ensure all columns exist
        summary_stats = full_data[summary_columns].describe().T  # Transpose for better readability
        st.write("Summary Statistics:")
        st.write(summary_stats)
    else:
        st.write("Some selected columns are missing from the dataset. Please ensure all required columns are present.")

    # Filter out the first five columns for analysis
    data = full_data.iloc[:, 5:]

    # Output variables to analyze
    output_variables = [
        "Intact Halves (%)",
        "Discharge Throughput (lbs. %)",
        "Loss (%)"
    ]

    # Iterate through output variables for separate analysis
    for response_var in output_variables:
        st.subheader(f"Analysis for {response_var}")

        # Step 2: Main Effects Analysis (ANOVA)
        st.write(f"Main Effects Analysis (ANOVA) for {response_var}")
        main_effects_formula = f'Q("{response_var}") ~ C(Q("Gap between Rings (in)")) + C(Q("Paddle Shaft RPM")) + C(Q("Drum RPM")) + Q("Moisture level (%)")'
        main_effects_model = ols(main_effects_formula, data=data).fit()
        main_effects_anova_results = sm.stats.anova_lm(main_effects_model, typ=2)
        st.write(main_effects_anova_results)

        # Step 3: Main and 2-Way Interaction Effects Analysis (ANOVA)
        st.write(f"Main and 2-Way Interaction Effects Analysis (ANOVA) for {response_var}")
        two_way_interaction_formula = f'''Q("{response_var}") ~ C(Q("Gap between Rings (in)")) 
                                          + C(Q("Paddle Shaft RPM")) 
                                          + C(Q("Drum RPM")) 
                                          + Q("Moisture level (%)")
                                          + C(Q("Gap between Rings (in)")):C(Q("Paddle Shaft RPM")) 
                                          + C(Q("Gap between Rings (in)")):C(Q("Drum RPM")) 
                                          + C(Q("Paddle Shaft RPM")):C(Q("Drum RPM"))'''
        two_way_interaction_model = ols(two_way_interaction_formula, data=data).fit()
        two_way_interaction_anova_results = sm.stats.anova_lm(two_way_interaction_model, typ=2)
        st.write(two_way_interaction_anova_results)

        # Step 4: Main Effects Plots
        st.write(f"Main Effects Plots for {response_var}")
        fig, ax = plt.subplots(4, 1, figsize=(10, 24))  # Adjusted for 4 plots

        # Main effect of Gap between Rings (in)
        sns.boxplot(x='Gap between Rings (in)', y=response_var, data=data, ax=ax[0])
        ax[0].set_title(f'Main Effect of Gap between Rings (in) on {response_var}')

        # Main effect of Paddle Shaft RPM
        sns.boxplot(x='Paddle Shaft RPM', y=response_var, data=data, ax=ax[1])
        ax[1].set_title(f'Main Effect of Paddle Shaft RPM on {response_var}')

        # Main effect of Drum RPM
        sns.boxplot(x='Drum RPM', y=response_var, data=data, ax=ax[2])
        ax[2].set_title(f'Main Effect of Drum RPM on {response_var}')

        # Effect of Moisture level (%) on the response variable
        sns.scatterplot(x='Moisture level (%)', y=response_var, data=data, ax=ax[3])
        ax[3].set_title(f'Effect of Moisture Level (%) on {response_var}')
        ax[3].set_xlabel('Moisture Level (%)')
        ax[3].set_ylabel(response_var)

        st.pyplot(fig)
