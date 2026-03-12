import streamlit as st
import pandas as pd
import json

from utils.pdf_reader import extract_text_from_pdf
from utils.docx_reader import extract_text_from_docx
from parser import parse_resume


st.title("Smart Resume Parser")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf","docx"]
)


if uploaded_file:

    if uploaded_file.name.endswith(".pdf"):

        text = extract_text_from_pdf(uploaded_file)

    else:

        text = extract_text_from_docx(uploaded_file)


    st.subheader("Resume Text Preview")

    st.write(text[:1500])


    parsed_data = parse_resume(text)


    st.subheader("Extracted Information")

    st.json(parsed_data)


    df = pd.DataFrame([parsed_data])

    st.table(df)


    if st.button("Export Results"):

        df.to_csv("outputs/parsed_resume.csv", index=False)

        with open("outputs/parsed_resume.json", "w") as f:

            json.dump(parsed_data, f)

        st.success("Results exported successfully!")