import os
import pandas as pd
import numpy as np
import logging
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

logging.basicConfig(level=logging.INFO)

CHUNKS_FILE = "./data/parquet/chunks_sample.parquet"
EMB_FILE = "./data/embeddings/embeddings_sample.npy"
CHROMA_DIR = "./data/chroma_db"

# load data + embeddings
chunks_df = pd.read_parquet(CHUNKS_FILE)
embeddings = np.load(EMB_FILE)
logging.info(f"Loaded {len(chunks_df)} chunks and embeddings {embeddings.shape}")

# embeddings model (needed by Chroma)
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
)

# create documents
docs = []
for i, row in chunks_df.iterrows():
    docs.append(Document(page_content=row["text"], metadata=row["metadata"]))

# create Chroma index manually
chroma_index = Chroma(
    embedding_function=embeddings_model,
    persist_directory=CHROMA_DIR
)

# add texts + embeddings manually
chroma_index.add_texts(texts=[d.page_content for d in docs],
                       metadatas=[d.metadata for d in docs],
                       embeddings=embeddings.tolist())  # convert numpy -> list

# persist to disk
chroma_index.persist()
logging.info(f"Chroma DB saved to {CHROMA_DIR}")
