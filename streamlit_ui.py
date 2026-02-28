"""
streamlit_ui.py
----------------
Streamlit frontend for the Document Portal.

Run with:  streamlit run streamlit_ui.py
"""

import streamlit as st

# Page configuration
st.set_page_config(page_title="Document Portal", layout="wide")

st.title("📄 Document Portal")
st.write("Upload and analyze your documents using AI.")

# File uploader
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    # TODO: Add document processing logic here
