import os
import logging
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp
from langchain_huggingface import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO)

VECTOR_DB_DIR = "./data/chroma_db" # saved Chroma DB path
LLM_MODEL_PATH = "./models/gemma-2b.gguf"

# load chroma vector db
logging.info("Loading Chroma vector store...")

embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")
vectordb = Chroma(collection_name="stackqa", persist_directory=VECTOR_DB_DIR, embedding_function=embeddings_model)
retriever = vectordb.as_retriever(search_kwargs={"k": 5})  # k most relevant chunks

logging.info("Chroma loaded successfully.")

# LLM setup
logging.info("Loading LLM...")
llm = LlamaCpp(model_path=LLM_MODEL_PATH, n_ctx=2048)  # adjust n_ctx as needed
logging.info("LLM loaded successfully.")

# Prompt template
PROMPT_TEMPLATE = """
You are an expert programming assistant. Use the provided context to answer the user's question accurately and clearly. 
Explain your answer in a step-by-step manner when relevant, and provide code examples if applicable. 
Do not make assumptions beyond the given context, but if the context is insufficient, provide a general answer based on your programming knowledge. 
Make your explanation easy to understand for someone with intermediate programming skills.

Question: {question}
Context:
{context}

Answer:
"""
prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["question", "context"])

# RetrievalQA pipeline
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # "stuff" uses all chunks; for large dataset consider "map_reduce"
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)

# query function
def ask_question(query: str):
    """
    Executes a query on the RAG pipeline and returns both the answer and the supporting context documents.
    """
    result = qa_chain.invoke({"query": query})
    answer = result["result"]
    docs = result["source_documents"]
    logging.info(f"Retrieved {len(docs)} chunks for query")
    return answer, docs

# rapid test
if __name__ == "__main__":
    while True:
        user_query = input("\nInsert a question (or 'exit' to close): ")
        if user_query.lower() in ("exit", "quit"):
            break
        answer, docs = ask_question(user_query)
        print("\n=== ANSWER ===")
        print(answer)
        print("\n=== CONTEXT CHUNKS ===")
        for i, doc in enumerate(docs[:3]):  # print only first 3 chunks
            print(f"[{i}] {doc.page_content[:200]}...\n")
