import pandas as pd
import numpy as np
import logging
from langchain_huggingface import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO)

CHUNKS_FILE = "./data/parquet/chunks.parquet"
EMB_FILE = "./data/embeddings.npy"

chunks_df = pd.read_parquet(CHUNKS_FILE)
logging.info(f"Loaded {len(chunks_df)} chunks")

# --------------------
# EMBEDDINGS
# --------------------

embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"batch_size": 64} # batch encoding
)

embeddings = embeddings_model.embed_documents(chunks_df["text"].tolist())
np.save(EMB_FILE, embeddings)
logging.info(f"Saved embeddings to {EMB_FILE}")
