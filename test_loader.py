from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader("documents/Python_notes.pdf")
pages = loader.load()

print("Total pages:", len(pages))

for i in [0, 5, 15, 30]:
    text = pages[i].page_content
    print(f"\n--- Page {i} ---")
    print("Length of text:", len(text))
    print("First 200 chars:")
    print(repr(text[:200]))