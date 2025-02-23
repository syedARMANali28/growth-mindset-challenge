import streamlit as st 
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title = "Data Sweeper", layout='wide' )

#custom css
st.markdown(
"""
<style>
.stApp {
    background-color: black;
    color: white;
    textcolor: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#title and description 
st.title("❄️Data Sweeper sterling by Syed Arman Ali")
st.write("A tool to identify and remove sensitive data from CSV files and tranform your files between CSV and Excell formats.")

#file uploader 
uploaded_files = st.file_uploader("Upload your files🎯 (accepts CSV file or Excell files):", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_files:
 for file in uploaded_files:
    file_ext = os.path.splitext(file.name)[-1].lower()

    if file_ext == '.csv':
        df = pd.read_csv(file)
    elif file_ext == '.xlsx':
        df = pd.read_excel(file)
    else:
        st.error(f"File format not supported. Please upload a CSV or Excell file. :{file_ext}")
        continue

    #file details 
    st.write("Preview the head of the DataFrame")
    st.dataframe(df.head())

    #data cleaning options 
    st.subheader("Data cleaning options")
    if st.checkbox(f"Clean Data for {file.name}"):
        col1, col2 =st.columns(2)
        
        with col1:
            if st.button(f"Remove duplicates from the files: {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates were removed!")

        with col2:
            if st.button(f"Fill missing values for {file.name}"):
                numerical_cols = df.select_dtypes(include=['number']).columns
                df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].mean())
                st.write("missing values have been filled!")

    st.subheader("Select colums to keep")     
    columns = st.multiselect(f"Choose columns for {file.name}",df.columns ,default=df.columns)      
    df = df[columns]

    #data visualization
    st.subheader("Data visualization")
    if st.checkbox(f"Show Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
    
    #Conversion options 
    st.subheader("Conversion options")
    conversion_type = st.radio(f"Convert {file.name} to: ",["CVS","Excell"],key=file.name)
    if st.button(f"Convert{file.name}"):
        buffer = BytesIO()
        if conversion_type == "CVS":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"

        elif conversion_type == "Excell":
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)
        
        st.download_button(
            label=f"Download {file_name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )
st.success("All files processed successfully!")    
