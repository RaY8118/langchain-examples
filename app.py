import streamlit as st
import tempfile
import os

from utils import (
    split_documents_semantic,
    load_pdf,
    create_vectorstore,
    create_huggingface_embeddings,
    create_vector_retriever,
    create_bm25_retriever,
    create_ensemble_retriever,
    create_rag_chain,
    ask_question,
    create_openrouter_llm as create_llm,
)


st.set_page_config(page_title="RAG PDF Summarizer")
st.title("RAG-powered PDF Summarizer")

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "temp_file_path" not in st.session_state:
    st.session_state.temp_file_path = None

upload_file = st.file_uploader("Upload a PDF", type="pdf")

if upload_file and st.session_state.rag_chain is None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(upload_file.read())
            st.session_state.temp_file_path = temp_file.name

        with st.spinner("Loading PDF..."):
            docs = load_pdf(st.session_state.temp_file_path)

        with st.spinner("Creating embeddings..."):
            embeddings = create_huggingface_embeddings()

        with st.spinner("Chunking document..."):
            chunks = split_documents_semantic(docs, embeddings)

        with st.spinner("Indexing document..."):
            vectorstore = create_vectorstore(
                chunks, embeddings, persist_directory="./chroma_index"
            )
            vectorstore.persist()

            vector_retriever = create_vector_retriever(vectorstore)
            bm25_retriever = create_bm25_retriever(chunks)
            ensemble_retriever = create_ensemble_retriever(
                bm25_retriever, vector_retriever
            )

            llm = create_llm()
            st.session_state.rag_chain = create_rag_chain(llm, ensemble_retriever)

        st.success("PDF indexed successfully! Ask your question.")

    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        if st.session_state.temp_file_path and os.path.exists(
            st.session_state.temp_file_path
        ):
            os.unlink(st.session_state.temp_file_path)

if st.session_state.rag_chain is not None:
    question = st.text_input("Ask a question about the PDF")
    if question:
        with st.spinner("Generating answer..."):
            try:
                result = ask_question(question, st.session_state.rag_chain)
                st.subheader("Answer")
                st.write(result)
            except Exception as e:
                st.error(f"Error generating answer: {str(e)}")
