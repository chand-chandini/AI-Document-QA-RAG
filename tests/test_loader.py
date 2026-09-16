from rag.loader import load_and_split_pdf


def test_load_and_split_pdf_loads_all_document_sources():
    docs = load_and_split_pdf()

    sources = {doc.metadata.get("source") for doc in docs}

    assert "Resume.pdf" in sources
    assert "Python_notes.pdf" in sources
    assert len(docs) > 0
