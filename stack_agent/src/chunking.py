import os
import pandas as pd
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

logging.basicConfig(level=logging.INFO)

PARQUET_DIR = "./data/parquet"
OUTPUT_FILE = "./data/parquet/chunks.parquet"

# load Parquet files
query_table = pd.read_parquet(os.path.join(PARQUET_DIR, "query_table.parquet"))

logging.info("Data loaded")

# --------------------
# CHUNKING
# --------------------

# create combined list for corpus: merge title, question_body, answer_body, and tags
# (for smaller datasets, add this as a column to the dataframe)
texts = (
    query_table['title'].fillna("") + "\n" + 
    query_table['question_body'].fillna("") + "\nAnswer:\n" + 
    query_table['answer_body'].fillna("") + "\nTags: " + 
    query_table['tags'].fillna("")
).to_list()

logging.info(f"Number of documents before chunking: {len(texts)}")

# create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, # max dimension of each chunk
    chunk_overlap=50, # overlap between chunks for context
)

documents = []

for idx, row in query_table.iterrows():
    base_text = (
        (row["title"] or "") + "\n" +
        (row["question_body"] or "") + "\nAnswer:\n" +
        (row["answer_body"] or "") + "\nTags: " +
        (row["tags"] or "")
    )
    # divide in chunk
    chunks = text_splitter.split_text(base_text)

    # add each chunk with metadata
    for chunk_id, chunk in enumerate(chunks):
        documents.append(
            {
                "text": chunk,
                "metadata": {
                    "question_id": row["question_id"],
                    "title": row["title"],
                    "tags": row["tags"],
                    "chunk_id": chunk_id
                }
            }
        )

logging.info(f"Created {len(documents)} chunked documents with metadata")

# salva come parquet
chunks_df = pd.DataFrame(documents)
chunks_df.to_parquet(OUTPUT_FILE, index=False)
logging.info(f"Saved chunks to {OUTPUT_FILE}")
