import os

from utils import (
    load_pdfs,
    split_documents,
    create_huggingface_embeddings as create_embeddings,
    create_vectorstore,
    create_vector_retriever,
    create_bm25_retriever,
    create_ensemble_retriever,
    create_rag_chain,
    ask_question,
    create_openrouter_llm as create_llm,
)


def run_rag_pipeline(question: str, pdf_folder: str = "./pdfs") -> str:
    ensure_pdf_directory(pdf_folder)
    docs = load_pdfs(pdf_folder)
    chunks = split_documents(docs)

    embeddings = create_embeddings()
    vectorstore = create_vectorstore(chunks, embeddings)

    vector_retriever = create_vector_retriever(vectorstore)
    bm25_retriever = create_bm25_retriever(chunks)
    ensemble_retriever = create_ensemble_retriever(bm25_retriever, vector_retriever)

    llm = create_llm()
    rag_chain = create_rag_chain(llm, ensemble_retriever)

    return ask_question(question, rag_chain)


def main():
    question = "Tell me about the pdf"
    print("\n=== Generating Answer ===")
    answer = run_rag_pipeline(question)
    print(answer)


def ensure_pdf_directory(pdf_folder: str) -> None:
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)


if __name__ == "__main__":
    main()
