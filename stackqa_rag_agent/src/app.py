import os
import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.manifold import TSNE

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from rag_pipeline import ask_question

logging.basicConfig(level=logging.INFO)

VECTOR_DB_DIR = "./data/chroma_db"

# load vector DB + embeddings
@st.cache_resource
def load_vectordb():
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")
    vectordb = Chroma(collection_name="stackqa", persist_directory=VECTOR_DB_DIR, embedding_function=embeddings_model)
    return vectordb

vectordb = load_vectordb()
logging.info("VectorDB loaded")

logging.info(f"Collections: {vectordb._client.list_collections()}")
logging.info(f"Count docs: {vectordb._collection.count()}")

# streamlit app
st.title("RAG Explorer: Embeddings & Q&A")

# scatterplot section
st.header("🔍 Explore the embedding space")

@st.cache_data
def get_tsne_plot(_vectordb, n_points=500):
    embeddings = _vectordb._collection.get(include=["embeddings"])["embeddings"]
    texts = _vectordb._collection.get(include=["documents"])["documents"]

    if embeddings is None or len(embeddings) == 0 or len(embeddings[0]) == 0:
        st.warning("⚠️ No embeddings found in the vector database.")
        return pd.DataFrame(columns=["x", "y", "text"])

    n_samples = min(len(embeddings), n_points)
    perplexity = min(30, n_samples - 1)

    tsne = TSNE(n_components=2, random_state=42, perplexity=perplexity)
    reduced = tsne.fit_transform(embeddings[:n_samples])

    df = pd.DataFrame({
        "x": reduced[:, 0],
        "y": reduced[:, 1],
        "text": texts[:n_samples]
    })
    return df

df = get_tsne_plot(vectordb)

# Use Plotly for an interactive scatter plot with hover
fig = px.scatter(df, x="x", y="y", hover_data=["text"], title="t-SNE Plot")
st.plotly_chart(fig)

st.write("Hover over the points in the plot to see the associated text!")

df = get_tsne_plot(vectordb)

st.dataframe(df.sample(5))

# Q&A section
st.header("💬 Ask a question")

user_query = st.text_input("Type your question here:", value="How do I create a virtual environment in Python?")
if user_query:
    answer, docs = ask_question(user_query)

    st.subheader("Answer:")
    st.write(answer)

    st.subheader("Context Chunks:")
    for i, doc in enumerate(docs[:3]):
        st.markdown(f"**[{i}]** {doc.page_content[:500]}...")
