import streamlit as st
import pandas as pd
from utils.cleaning import clean_data

st.title("AI-Powered SME Business Intelligence Platform")
st.write("Upload your sales CSV file for automatic cleaning and analysis")
uploaded_file=st.file_uploader("Upload CSV",type=["csv"])

#Processing file 
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file,encoding="utf-8")

    except UnicodeDecodeError:
        uploaded_file.seek(0)

        df = pd.read_csv(uploaded_file,encoding="latin1")
    
    st.subheader("Original Dataset")
    st.write("Shape : ",df.shape)
    st.dataframe(df.head())

    #Clean dataset
    (cleaned_df,missing_before,missing_after,duplicates_removed)=clean_data(df)

    st.subheader("Available Columns")

    st.write(cleaned_df.columns.tolist())

    #Cleaning report
    st.subheader("Data Cleaning Report")
    st.write(f"Missing Values Before Cleaning: {missing_before}")
    st.write(f"Missing Values After Cleaning : {missing_after}")
    st.write(f"Duplicate Rows Removed : {duplicates_removed}")

    #Cleaned dataset
    st.subheader("Cleaned Datast")
    st.write("Shape : ",cleaned_df.shape)
    st.dataframe(cleaned_df.head())
    st.success("Data Cleaning Completed Successfully")

    from utils.column_detector import detect_columns
    mapping = detect_columns(cleaned_df)
    st.subheader("Detected Columns")

    st.json(mapping)