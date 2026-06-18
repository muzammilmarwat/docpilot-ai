import streamlit as st

from services.pdf_service import extract_text_from_pdf


st.set_page_config(
    page_title="DocPilot AI",
    page_icon="📄",
    layout="wide",
)

st.title("📄 DocPilot AI")
st.subheader("AI-Powered Document Intelligence Platform")

st.markdown(
    "Upload a PDF and DocPilot AI will extract readable text from it. "
    "This is the foundation for future resume analysis, proposal generation, and PDF intelligence."
)

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"],
)

if uploaded_file:
    st.info(f"Processing: {uploaded_file.name}")

    try:
        extracted_text = extract_text_from_pdf(uploaded_file)

        if extracted_text:
            st.success("PDF text extracted successfully.")

            st.subheader("Extracted Text")

            st.text_area(
                label="PDF Content",
                value=extracted_text,
                height=500,
            )

            st.download_button(
                label="Download Extracted Text",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain",
            )
        else:
            st.warning(
                "No readable text found. This may be a scanned/image-based PDF."
            )

    except RuntimeError as error:
        st.error(str(error))