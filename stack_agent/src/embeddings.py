import pandas as pd
import numpy as np
import logging
from langchain_huggingface import HuggingFaceEmbeddings

logging.basicConfig(level=logging.INFO)

CHUNKS_FILE = "./data/parquet/chunks_sample.parquet"
EMB_FILE = "./data/embeddings/embeddings_sample.npy"

chunks_df = pd.read_parquet(CHUNKS_FILE)
logging.info(f"Loaded {len(chunks_df)} chunks")

#embeddings_model = HuggingFaceEmbeddings(
#    model_name="sentence-transformers/all-MiniLM-L6-v2",
#    encode_kwargs={"batch_size": 64} # batch encoding
#)

# try a smaller model
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
    encode_kwargs={"batch_size": 128},  # increase batch_size to speed up
)

embeddings = embeddings_model.embed_documents(chunks_df["text"].tolist())
np.save(EMB_FILE, embeddings)
logging.info(f"Saved embeddings to {EMB_FILE}")
