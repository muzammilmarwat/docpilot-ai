import streamlit as st

st.set_page_config(
    page_title="DocPilot AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 DocPilot AI")
st.subheader("AI-Powered Document Intelligence Platform")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")