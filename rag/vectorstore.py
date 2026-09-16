import uuid
from pathlib import Path

import streamlit as st
from langchain_chroma import Chroma


@st.cache_resource
def create_vectorstore(chunks, embeddings):
    base_dir = Path(__file__).resolve().parent.parent / "chroma_db"
    base_dir.mkdir(exist_ok=True)

    persist_directory = base_dir / f"session_{uuid.uuid4().hex}"

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="resume_collection",
        persist_directory=str(persist_directory),
    )

    return vectorstore


def retrieve_documents(vectorstore, question, k=6):
    results = vectorstore.max_marginal_relevance_search(
        question,
        k=k,
        fetch_k=30,
        lambda_mult=0.5
    )

    return results