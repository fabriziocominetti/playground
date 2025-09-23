import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

logging.basicConfig(level=logging.INFO)

CHROMA_DIR = "./data/chroma_db"

# embeddings model
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
    encode_kwargs={"batch_size": 128},
)

# load existing database
chroma_index = Chroma(
    collection_name="stackqa",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_DIR,
)

logging.info("Chroma index loaded.")

# query test
query = "How do I create a virtual environment in Python?"
results = chroma_index.similarity_search(query, k=5)

print("\n=== Top Results ===")
for r in results:
    meta = r.metadata
    snippet = r.page_content[:200].replace("\n", " ")
    print(f"QID: {meta.get('question_id')} | Title: {meta.get('title')} | Tags: {meta.get('tags')}")
    print(f"Snippet: {snippet}...")
    print("-" * 80)
