import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Streamlit page
st.set_page_config(page_title="Solar Farm Data Analysis", layout="wide")

# App Title
st.title("Solar Farm Data Analysis Dashboard")

# **Section: Data Understanding and Cleaning**
st.header("Data Understanding and Cleaning")

# File Upload for Data Understanding and Cleaning
uploaded_file = st.file_uploader("Upload CSV File for Analysis", type=["csv"], key="upload_cleaning")

if uploaded_file:
    # Load data
    data = pd.read_csv(uploaded_file)
    
    # Display raw data
    st.subheader("Raw Data Preview")
    st.write(data.head())

    # Basic Information
    st.subheader("Dataset Overview")
    st.write("Shape of the data:", data.shape)
    st.write("Columns in the dataset:", data.columns.tolist())

    # Missing Values
    st.subheader("Data Quality Check")
    missing_values = data.isnull().sum()
    if missing_values.sum() > 0:
        st.write("Missing values in each column:")
        st.write(missing_values[missing_values > 0])
        
        # Handle missing values
        handle_missing = st.radio(
            "Select how to handle missing values:",
            ("No action", "Forward fill", "Drop rows with missing values"),
        )

        if handle_missing == "Forward fill":
            data.ffill(inplace=True)
            st.success("Missing values filled using forward fill!")
        elif handle_missing == "Drop rows with missing values":
            data.dropna(inplace=True)
            st.success("Rows with missing values have been dropped!")
    else:
        st.write("No missing values detected!")

    # Column-wise Data Types
    st.subheader("Column Data Types")
    st.write(data.dtypes)

    # Convert object columns to a more specific type
    for column in data.select_dtypes(include='object').columns:
        # Attempt to convert to numeric if applicable
        try:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        except ValueError:
            # If that fails, convert to string
            data[column] = data[column].astype(str)

    # Sidebar Cleaning Options
    st.sidebar.header("Cleaning Options")
    clean_data = st.sidebar.checkbox("Show cleaned data")
    if clean_data:
        st.write("### Cleaned Data Preview")
        st.write(data.head())
else:
    st.info("Awaiting CSV file upload for cleaning and analysis.")

# **Section: Exploratory Data Analysis (EDA)**
if uploaded_file:
    st.header("Exploratory Data Analysis (EDA)")

    # Plot Solar Radiation Trends
    st.subheader("Solar Radiation Trends")
    numeric_columns = data.select_dtypes(include='number').columns.tolist()
    selected_columns = st.multiselect(
        "Select columns for line chart:", numeric_columns, default=["GHI", "DNI", "DHI"]
    )
    if selected_columns:
        st.line_chart(data[selected_columns])
    else:
        st.warning("Please select at least one column for the line chart.")

    # Histogram for GHI
    if "GHI" in data.columns:
        st.subheader("Histogram for Global Horizontal Irradiance (GHI)")
        bin_size = st.slider("Select number of bins:", min_value=5, max_value=50, value=20)
        fig, ax = plt.subplots()
        sns.histplot(data["GHI"], kde=True, bins=bin_size, ax=ax, color="skyblue")
        st.pyplot(fig)
    else:
        st.warning("GHI column is missing in the dataset!")

    # Correlation Matrix
    st.subheader("Correlation Analysis")
    selected_corr_columns = st.multiselect(
        "Select numeric columns for correlation matrix:", numeric_columns, default=numeric_columns
    )
    if selected_corr_columns:
        fig, ax = plt.subplots(figsize=(10, 8))
        corr_matrix = data[selected_corr_columns].corr()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Please select at least one column for correlation analysis.")

    # Wind Analysis (if columns are present)
    if "WD" in data.columns and "WS" in data.columns:
        st.subheader("Wind Analysis")
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        wind_direction = np.deg2rad(data["WD"])
        wind_speed = data["WS"]
        ax.scatter(wind_direction, wind_speed, alpha=0.75)
        st.pyplot(fig)
    else:
        st.warning("Wind direction (WD) or speed (WS) columns are missing!")

else:
    st.info("Upload a dataset to unlock EDA features.")

# Sidebar Information
st.sidebar.write("### About")
st.sidebar.info("This dashboard allows users to perform data cleaning and exploratory data analysis on solar farm data.")
