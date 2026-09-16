# 📄 AI Document Q&A — RAG Application

An AI-powered document question-answering application that allows users to upload PDF documents and ask questions about their content.

The application uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from documents before generating an answer with an LLM.


🚀 **Live Demo:** [Open AI Document Q&A App](https://ai-document-app-rag.streamlit.app/)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-document-app-rag.streamlit.app/)
## 🚀 Features

- Upload one or multiple PDF documents
- Extract text from PDFs
- Split documents into smaller chunks
- Generate embeddings using HuggingFace
- Store embeddings in ChromaDB
- Retrieve relevant document chunks using MMR
- Generate answers using Llama 3.2
- Maintain conversation history
- Display document sources and page numbers
- Clear chat history
- Error handling
- Streamlit user interface

## 🛠️ Technologies

- Python
- Streamlit
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers
- Ollama
- Llama 3.2
- PyMuPDF

## 🧠 RAG Architecture

```text
                PDF Documents
                      ↓
                PDF Extraction
                      ↓
                   Chunking
                      ↓
                  Embeddings
                      ↓
                  ChromaDB
                      ↓
              MMR Retrieval
                      ↓
              Relevant Chunks
                      ↓
              Llama 3.2 (LLM)
                      ↓
                   Answer
                      ↓
              Source + Page
