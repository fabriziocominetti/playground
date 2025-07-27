# 🤖 Streamlit Chatbots with Hugging Face

This repo contains two Streamlit-based chatbots powered by open-source large language models (LLMs) from Hugging Face.

## 🧠 Chatbot 1: Hugging Face Inference API

**File:** `st_app_chatbot_hf_api.py`

Use any hosted Hugging Face model via the **Hugging Face Inference API**. Requires a free Hugging Face account and API token.

**Features:**
- Select models like Mistral-7B, Zephyr, Falcon, etc.
- Chat history stored in session

## 💻 Chatbot 2: Local Model (Offline)

**File:** `local_chatbot.py`  

Runs a local model from Hugging Face using the `transformers` library. No internet, tokens, or API calls required.

**Features:**
- Fully offline after first download
- Uses `pipeline` for easy generation
- Works with CPU or GPU (recommended for larger models)

## ⚙️ Setup with `uv`

> [`uv`](https://github.com/astral-sh/uv) is a fast Python package manager (drop-in for pip + venv).

```bash
# install
brew install uv # Windows: curl -Ls https://astral.sh/uv/install.sh | sh

# create and activate virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# install dependencies
uv pip install streamlit transformers torch accelerate requests
```

## Run the Apps

```bash
streamlit run hf_chatbot.py
streamlit run local_chatbot.py
````
