import pandas as pd
import numpy as np
import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

logging.basicConfig(level=logging.INFO)

CHUNKS_FILE = "./data/chunks.parquet"
VECTOR_DB_DIR = "./data/chroma_db"

# --------------------
# VECTOR DB
# --------------------

chunks_df = pd.read_parquet(CHUNKS_FILE)
logging.info(f"Loaded {len(chunks_df)} chunks")

texts = chunks_df["text"].tolist()
metadatas = chunks_df.drop(columns=["text"]).to_dict(orient="records")

embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# create local Chroma vector DB
vectordb = Chroma.from_texts(
    texts=texts,
    embedding=embeddings_model,
    metadatas=metadatas,
    persist_directory=VECTOR_DB_DIR
)

# persist to disk
vectordb.persist()

logging.info("Vector DB created and persisted to disk.")
