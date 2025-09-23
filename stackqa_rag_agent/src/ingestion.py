import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

DATA_DIR = "./data/raw"
PARQUET_DIR = "./data/parquet"

# load CSV files
questions = pd.read_csv(os.path.join(DATA_DIR, "Questions.csv"), encoding="ISO-8859-1")
answers = pd.read_csv(os.path.join(DATA_DIR, "Answers.csv"), encoding="ISO-8859-1")
tags = pd.read_csv(os.path.join(DATA_DIR, "Tags.csv"), encoding="ISO-8859-1")

logging.info("Data loaded")

# normalize column names
questions.columns = [col.lower().replace(' ', '_') for col in questions.columns]
answers.columns = [col.lower().replace(' ', '_') for col in answers.columns]
tags.columns = [col.lower().replace(' ', '_') for col in tags.columns]

# save as Parquet files
questions.to_parquet(os.path.join(PARQUET_DIR, "questions.parquet"), index=False)
answers.to_parquet(os.path.join(PARQUET_DIR, "answers.parquet"), index=False)
tags.to_parquet(os.path.join(PARQUET_DIR, "tags.parquet"), index=False)

logging.info("Data ingestion completed and files saved as Parquet.")