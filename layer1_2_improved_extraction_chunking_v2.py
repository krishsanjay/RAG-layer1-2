"""
This script demonstrates an improved approach to extracting text from a PDF document, with a focus on better handling of sections and tables. 
It uses the `docling` library to convert the PDF into a structured format, and then processes the content to create 
LangChain `Document` objects that are suitable for use in a Retrieval-Augmented Generation (RAG) pipeline.
In this, chunks are created based on sections, and tables are included in the section text to ensure that important contextual information is preserved.
And if any section size exceeds the specified chunk size, it will be further split into smaller chunks with some overlap to maintain context.
"""


from docling.document_converter import DocumentConverter
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_rag_documents(pdf_path: str) -> list[Document]:

    converter = DocumentConverter()
    result = converter.convert(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    # splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=50,
    #     chunk_overlap=10,
    # )

    docs = []

    current_section = None
    current_page = None
    section_buffer = []

    chunk_counter = 0

    def flush_section():
        """Create LangChain Documents from accumulated section text."""
        nonlocal chunk_counter

        if not section_buffer:
            return

        section_text = "\n".join(section_buffer).strip()

        if not section_text:
            return

        chunks = splitter.split_text(section_text)

        for chunk in chunks:
            chunk_counter += 1

            docs.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": pdf_path,
                        "page": current_page,
                        "section": current_section,
                        "chunk": chunk_counter,
                        "type": "policy_text",
                    },
                )
            )

    for item, level in result.document.iterate_items():

        # Skip items without text
        if not hasattr(item, "text"):
            continue

        text = (item.text or "").strip()

        if not text:
            continue

        # Extract page number from provenance
        page_no = None
        if hasattr(item, "prov") and item.prov:
            page_no = item.prov[0].page_no

        item_type = item.__class__.__name__

        # ----------------------------
        # New Section Found
        # ----------------------------
        if item_type == "SectionHeaderItem":

            # Save previous section first
            flush_section()

            current_section = text
            current_page = page_no
            section_buffer = [text]

            continue

        # ----------------------------
        # Tables
        # ----------------------------
        if item_type == "TableItem":

            try:
                table_text = item.export_to_markdown()
            except Exception:
                table_text = text

            section_buffer.append(table_text)
            continue

        # ----------------------------
        # Normal Text
        # ----------------------------
        section_buffer.append(text)

    # Flush final section
    flush_section()

    return docs


if __name__ == "__main__":

    docs = create_rag_documents("2column_paper.pdf")

    print(f"\nCreated {len(docs)} chunks\n")

    for doc in docs:

        print("=" * 60)

        print("CONTENT:")
        print(doc.page_content)

        print("\nMETADATA:")
        print(doc.metadata)

        print()