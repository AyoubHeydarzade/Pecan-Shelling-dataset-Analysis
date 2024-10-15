#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

if uploaded_file is not None:
    # Load the dataset into a dataframe
    data = pd.read_excel(uploaded_file)
    
    # Display the first few rows of the dataset
    st.write("Here is a preview of your dataset:")
    st.write(data.head())

    # Step 2: Main Effects Analysis (ANOVA)
    st.subheader("Main Effects Analysis (ANOVA)")
    
    # Define the model formula for main effects only
    main_effects_formula = 'Q("Intact Halves (%)") ~ C(Q("Gap between Rings (in)")) + C(Q("Paddle Shaft RPM")) + C(Q("Drum RPM"))'

    # Fit the model for main effects
    main_effects_model = ols(main_effects_formula, data=data).fit()

    # Perform ANOVA for main effects
    main_effects_anova_results = sm.stats.anova_lm(main_effects_model, typ=2)

    # Display the ANOVA results
    st.write("ANOVA Results for Main Effects")
    st.write(main_effects_anova_results)

    # Step 3: Interaction Effects Analysis (ANOVA)
    st.subheader("Main and 2-Way Interaction Effects Analysis (ANOVA)")
    
    # Define the model formula for main and 2-way interaction effects
    two_way_interaction_formula = '''Q("Intact Halves (%)") ~ C(Q("Gap between Rings (in)")) 
                                     + C(Q("Paddle Shaft RPM")) 
                                     + C(Q("Drum RPM")) 
                                     + C(Q("Gap between Rings (in)")):C(Q("Paddle Shaft RPM")) 
                                     + C(Q("Gap between Rings (in)")):C(Q("Drum RPM")) 
                                     + C(Q("Paddle Shaft RPM")):C(Q("Drum RPM"))'''

    # Fit the model including 2-way interactions
    two_way_interaction_model = ols(two_way_interaction_formula, data=data).fit()

    # Perform ANOVA including 2-way interaction effects
    two_way_interaction_anova_results = sm.stats.anova_lm(two_way_interaction_model, typ=2)

    # Display the ANOVA results
    st.write("ANOVA Results for Main and 2-Way Interaction Effects")
    st.write(two_way_interaction_anova_results)

    # Step 4: Main Effects Plots
    st.subheader("Main Effects Plots")
    
    # Generate boxplots for main effects
    fig, ax = plt.subplots(3, 1, figsize=(10, 18))

    sns.boxplot(x='Gap between Rings (in)', y='Intact Halves (%)', data=data, ax=ax[0])
    ax[0].set_title('Main Effect of Gap between Rings (in) on Intact Halves (%)')

    sns.boxplot(x='Paddle Shaft RPM', y='Intact Halves (%)', data=data, ax=ax[1])
    ax[1].set_title('Main Effect of Paddle Shaft RPM on Intact Halves (%)')

    sns.boxplot(x='Drum RPM', y='Intact Halves (%)', data=data, ax=ax[2])
    ax[2].set_title('Main Effect of Drum RPM on Intact Halves (%)')

    st.pyplot(fig)

    # Step 5: Interaction Plots
    st.subheader("Interaction Plots")
    
    fig, ax = plt.subplots(3, 1, figsize=(10, 18))

    # Interaction between Gap between Rings and Paddle Shaft RPM
    interaction_plot(data['Gap between Rings (in)'], data['Paddle Shaft RPM'], data['Intact Halves (%)'],
                     colors=['red', 'blue', 'green'], markers=['D', '^', 'o'], ms=10, ax=ax[0])
    ax[0].set_title('Interaction Between Gap between Rings (in) and Paddle Shaft RPM')

    # Interaction between Gap between Rings and Drum RPM
    interaction_plot(data['Gap between Rings (in)'], data['Drum RPM'], data['Intact Halves (%)'],
                     colors=['red', 'blue', 'green'], markers=['D', '^', 'o'], ms=10, ax=ax[1])
    ax[1].set_title('Interaction Between Gap between Rings (in) and Drum RPM')

    # Interaction between Paddle Shaft RPM and Drum RPM
    interaction_plot(data['Paddle Shaft RPM'], data['Drum RPM'], data['Intact Halves (%)'],
                     colors=['red', 'blue', 'green'], markers=['D', '^', 'o'], ms=10, ax=ax[2])
    ax[2].set_title('Interaction Between Paddle Shaft RPM and Drum RPM')

    st.pyplot(fig)


