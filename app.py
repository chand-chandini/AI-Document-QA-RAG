from rag.loader import load_and_split_pdf
from rag.embeddings import create_embeddings
from rag.vectorstore import create_vectorstore, retrieve_documents
from rag.qa import generate_answer


chunks = load_and_split_pdf()

print("Number of chunks:", len(chunks))

embeddings = create_embeddings()

vectorstore = create_vectorstore(
    chunks,
    embeddings
)

print("Chunks stored in ChromaDB")


chat_history = []

while True:

    question = input(
        "\nAsk a question about the PDF (type 'exit' to quit): "
    )

    if question.lower() == "exit":
        break

    documents = retrieve_documents(
        vectorstore,
        question,
        k=6
    )

    print("\n--- Retrieved Documents ---")

    for i, doc in enumerate(documents):
        print(f"\nChunk {i + 1}")
        print("Source:", doc.metadata.get("source"))
        print("Page:", doc.metadata.get("page"))
        print("Content:", doc.page_content[:300])

    answer = generate_answer(
        question,
        documents,
        chat_history
    )

    chat_history.append({
        "question": question,
        "answer": answer
    })

    print("\n--- Final Answer ---")
    print(answer)