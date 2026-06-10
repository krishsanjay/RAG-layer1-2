from pypdf import PdfReader


def naive_extract(pdf_path:str) -> str:
    """
    Naively extract text from a PDF file using pypdf.

    Args:
            pdf_path (str): The path to the PDF file."""
    reader = PdfReader(pdf_path)
    full_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text.append(text)
    return "\n".join(full_text)

if __name__ == "__main__":
    text = naive_extract("messy_policy.pdf")
    print("=============NAIVE EXTRACTION RESULT=============")
    print(text)
