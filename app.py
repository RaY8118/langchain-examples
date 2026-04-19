import streamlit as st
from pdfminer.high_level import extract_text
from langchain_openrouter import ChatOpenRouter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
import tempfile

# LLM and Embedding setup
llm = ChatOpenRouter(
    model="openai/gpt-oss-120b:free",
)

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text",
)

# Embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

st.set_page_config(page_title="RAG PDF Summarizer")
st.title("RAG-powered PDF Summarizer")
upload_file = st.file_uploader("Upload a PDF", type="pdf")
if upload_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(upload_file.read())
        temp_file_path = temp_file.name

        # Step 1: Extract text
        raw_text = extract_text(temp_file_path)

        # Step 2: Chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200)

        chunks = text_splitter.split_text(raw_text)

        # Step 3: Embed and store in Chroma
        with st.spinner("Indexing document..."):
            vectordb = Chroma.from_texts(
                chunks, embedding_model, persist_directory="./chroma_index")
            vectordb.persist()

            # Step 4: RAG QA Chain
            retriever = vectordb.as_retriever(
                search_type="similarity", search_kwargs={"k": 5})
            prompt = ChatPromptTemplate.from_template("{context}\n\n{input}")
            # Create the chains
            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(
                retriever, question_answer_chain)
            summary_prompt = "Please summarize the documents based on key topics"
            with st.spinner("Running RAG summarization..."):
                result = rag_chain.invoke({"input": summary_prompt})
            st.subheader("Summary")
            st.write(result["answer"])