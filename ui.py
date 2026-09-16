import streamlit as st

from rag.loader import load_and_split_pdf
from rag.embeddings import create_embeddings
from rag.vectorstore import create_vectorstore, retrieve_documents
from rag.qa import generate_answer


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Document Q&A",
    page_icon="📄"
)


# -----------------------------------
# Title
# -----------------------------------

st.title("📄 AI Document Q&A")
st.caption("Upload PDFs and ask questions about them.")


# -----------------------------------
# Chat History
# -----------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -----------------------------------
# Clear Chat
# -----------------------------------

def clear_chat():
    st.session_state.chat_history = []


st.button(
    "🗑️ Clear Chat",
    on_click=clear_chat
)


# -----------------------------------
# Upload PDF
# -----------------------------------

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)


# -----------------------------------
# If PDFs are uploaded
# -----------------------------------

if uploaded_files:

    st.success(
        f"{len(uploaded_files)} PDF(s) uploaded."
    )

    try:

        # Load and split PDFs
        chunks = load_and_split_pdf(
            uploaded_files
        )

        # Create embeddings
        embeddings = create_embeddings()

        # Create vector database
        vectorstore = create_vectorstore(
            chunks,
            embeddings
        )

        st.success(
            f"Created {len(chunks)} chunks from your PDFs."
        )


        # -----------------------------------
        # Display Previous Chat
        # -----------------------------------

        for chat in st.session_state.chat_history:

            with st.chat_message("user"):
                st.write(chat["question"])

            with st.chat_message("assistant"):
                st.write(chat["answer"])


        # -----------------------------------
        # User Question
        # -----------------------------------

        question = st.chat_input(
            "Ask something about your documents..."
        )


        if question:

            # Show user question
            with st.chat_message("user"):
                st.write(question)


            try:

                # -----------------------------------
                # Retrieve relevant documents
                # -----------------------------------

                documents = retrieve_documents(
                    vectorstore,
                    question,
                    k=6
                )


                # -----------------------------------
                # Check retrieval
                # -----------------------------------

                if not documents:

                    st.warning(
                        "I couldn't find relevant information "
                        "in the documents."
                    )

                else:

                    # -----------------------------------
                    # Generate Answer
                    # -----------------------------------

                    answer = generate_answer(
                        question,
                        documents,
                        st.session_state.chat_history
                    )


                    # -----------------------------------
                    # Display Answer
                    # -----------------------------------

                    with st.chat_message("assistant"):

                        st.write(answer)


                        # -----------------------------------
                        # Sources
                        # -----------------------------------

                        with st.expander("📚 Sources"):

                            sources = []


                            for doc in documents:

                                source = (
                                    f"{doc.metadata.get('source', 'Unknown')} "
                                    f"— page "
                                    f"{doc.metadata.get('page', 0) + 1}"
                                )


                                if source not in sources:
                                    sources.append(source)


                            for source in sources:
                                st.caption(source)


                    # -----------------------------------
                    # Save Chat
                    # -----------------------------------

                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer
                    })


            except Exception as error:

                st.error(
                    "Something went wrong while answering "
                    "your question. Please try again."
                )


    except Exception as error:

        st.error(
            "Something went wrong while processing "
            "the PDF. Please upload the PDF again."
        )


# -----------------------------------
# No PDF Uploaded
# -----------------------------------

else:

    st.info(
        "👆 Upload one or more PDF documents to start."
    )