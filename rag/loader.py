from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import os


def load_and_split_pdf(uploaded_files):

    all_documents = []

    for uploaded_file in uploaded_files:

        # Create temporary PDF file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        # Load PDF
        loader = PyMuPDFLoader(temp_path)

        documents = loader.load()

        # Add original filename
        for document in documents:
            document.metadata["source"] = uploaded_file.name

        all_documents.extend(documents)

        # Delete temporary file
        os.remove(temp_path)

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(
        all_documents
    )

    return chunks