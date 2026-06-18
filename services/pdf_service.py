import pdfplumber


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF file using pdfplumber.
    Returns extracted text as a single string.
    """
    extracted_text = []

    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()

                if page_text:
                    extracted_text.append(f"\n--- Page {page_number} ---\n")
                    extracted_text.append(page_text)

        return "\n".join(extracted_text).strip()

    except Exception as error:
        raise RuntimeError(f"Failed to extract text from PDF: {error}") from error