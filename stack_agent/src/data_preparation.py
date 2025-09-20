import os
import pandas as pd
import duckdb
import logging

logging.basicConfig(level=logging.INFO)

PARQUET_DIR = "./data/parquet"

# create DuckDB in-memory connection
con = duckdb.connect(database=':memory:')

# load Parquet files
questions = pd.read_parquet(os.path.join(PARQUET_DIR, "questions.parquet"))
answers = pd.read_parquet(os.path.join(PARQUET_DIR, "answers.parquet"))
tags = pd.read_parquet(os.path.join(PARQUET_DIR, "tags.parquet"))

logging.info("Data loaded")

# keep only relevant columns
questions = questions[['id', 'title', 'body']]
answers = answers[['parentid', 'body']]

# register DataFranes as temp tables
con.register("questions", questions)
con.register("answers", answers)
con.register("tags", tags)

# SQL query to join tables
query_table = con.execute("""
                    SELECT q.id AS question_id, q.title, q.body AS question_body, a.body AS answer_body, STRING_AGG(t.tag, ',') AS tags
                    FROM questions q
                    LEFT JOIN answers a
                        ON q.id = a.parentid
                    LEFT JOIN tags t
                        ON q.id = t.id
                    GROUP BY q.id, q.title, q.body, a.body
                    """).df()

logging.info(f"Joined data shape: {query_table.shape}")
logging.info(f"Joined data head: {query_table.head()}")

# save table as Parquet file
query_table.to_parquet(os.path.join(PARQUET_DIR, "query_table.parquet"), index=False)

logging.info("Data preparation completed and table file saved as Parquet.")