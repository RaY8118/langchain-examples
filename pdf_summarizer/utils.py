from langchain_openrouter import ChatOpenRouter
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def load_pdfs(pdf_folder: str):
    loader = PyPDFDirectoryLoader(pdf_folder)
    return loader.load()


def load_pdf(pdf_name: str):
    loader = PyPDFLoader(pdf_name)
    return loader.load()


def split_documents(docs, chunk_size=800, chunk_overlap=150):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ". ", ""],
    )
    return text_splitter.split_documents(docs)


def split_documents_semantic(docs, embeddings, breakpoint_threshold_amount=1.0):
    text_splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_amount=breakpoint_threshold_amount,
    )
    return text_splitter.split_documents(docs)


def create_local_embeddings(model="nomic-embed-text"):
    return OllamaEmbeddings(model=model)


def create_huggingface_embeddings(model="sentence-transformers/all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(
        model_name=model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def create_vectorstore(chunks, embeddings, persist_directory="./chroma_db"):
    return Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=persist_directory
    )


def create_vector_retriever(vectorstore, k=6):
    return vectorstore.as_retriever(search_kwargs={"k": k})


def create_bm25_retriever(chunks, k=6):
    retriever = BM25Retriever.from_documents(chunks)
    retriever.k = k
    return retriever


def create_ensemble_retriever(bm25_retriever, vector_retriever, weights=[0.4, 0.6]):
    return EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever], weights=weights
    )


def create_local_llm(model="llama3.2:1b"):
    from langchain_ollama import ChatOllama

    return ChatOllama(model=model)


def create_openrouter_llm(model="openai/gpt-oss-120b:free"):
    return ChatOpenRouter(model=model)


def create_rag_chain(llm, ensemble_retriever):
    template = """You are a helpful assistant. Answer the question based **only** on the following context.
    If you cannot find the answer in the context, say "I don't have enough information."

    Context:
    {context}

    Question: {question}

    Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    return (
        {"context": ensemble_retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


def ask_question(question, rag_chain):
    answer = rag_chain.invoke(question)
    return answer
