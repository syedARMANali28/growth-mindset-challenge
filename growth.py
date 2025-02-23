import streamlit as st 
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS for better visibility
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    /* Improve heading visibility */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #ffffff !important;
        font-weight: bold !important;
        text-transform: uppercase;
    }
    /* Increase font size for important labels */
    .stFileUploader label, .stRadio label, .stCheckbox label, .stButton {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #ffffff !important;
    }
    /* Style data frame for dark mode */
    .stDataFrame {
        background-color: #222222 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("🚀 Data Sweeper Sterling by Syed Arman Ali")
st.write("A tool to identify and remove sensitive data from CSV files and transform your files between CSV and Excel formats.")

# File uploader with enhanced visibility
st.subheader("📂 Upload Your Files")
uploaded_files = st.file_uploader("Accepts CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f"❌ File format not supported. Please upload a CSV or Excel file: {file_ext}")
            continue

        # File details
        st.subheader(f"📜 Preview of {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"🔍 Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates were removed!")

            with col2:
                if st.button(f"🩹 Fill Missing Values for {file.name}"):
                    numerical_cols = df.select_dtypes(include=['number']).columns
                    df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].mean())
                    st.write("✅ Missing values have been filled!")

        st.subheader("🎯 Select Columns to Keep")     
        columns = st.multiselect(f"🎛 Choose columns for {file.name}", df.columns, default=df.columns)      
        df = df[columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📉 Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"📥 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All files processed successfully!")

