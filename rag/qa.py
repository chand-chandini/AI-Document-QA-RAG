import os
import streamlit as st
from google import genai


@st.cache_resource
def get_llm():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)

    return client


def generate_answer(question, documents, chat_history):

    context = "\n\n".join(
        [
            f"""
SOURCE: {document.metadata.get('source', 'Unknown')}
PAGE: {document.metadata.get('page', 0) + 1}

{document.page_content}
"""
            for document in documents
        ]
    )

    history = "\n".join(
        [
            f"User: {chat['question']}\nAssistant: {chat['answer']}"
            for chat in chat_history
        ]
    )

    client = get_llm()

    prompt = f"""
You are a document question-answering assistant.

Use the retrieved context as your source of truth.

Rules:
- Combine information from multiple chunks when necessary.
- Give a clear answer in 2-4 sentences.
- Do not add unsupported information.
- If the answer is not present in the context, say:
  "I couldn't find this information in the documents."

CONTEXT:
{context}

CONVERSATION HISTORY:
{history}

QUESTION:
{question}

Answer using only the context.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text