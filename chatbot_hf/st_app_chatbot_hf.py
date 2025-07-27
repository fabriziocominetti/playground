import streamlit as st
import requests
from datetime import datetime

# Title
st.title("🤖 Hugging Face Chatbot")
st.markdown("Chat with an open-source model via Hugging Face Inference API!")

# Sidebar config
with st.sidebar:
    st.header("Configuration")

    hf_token = st.text_input("Enter your Hugging Face API Token:", type="password", help="Get your token at https://huggingface.co/settings/tokens")
    
    model_id = st.selectbox(
        "Choose a model:",
        [
            "mistralai/Mistral-7B-Instruct-v0.1",
            "HuggingFaceH4/zephyr-7b-beta",
            "tiiuae/falcon-7b-instruct",
            "meta-llama/Llama-2-7b-chat-hf"
        ],
        index=0
    )

# Track chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        st.caption(f"*{msg['timestamp']}*")

# Chat input
if prompt := st.chat_input("Say something..."):
    if not hf_token:
        st.error("Please enter your Hugging Face API token.")
        st.stop()
    
    # Save user message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp})

    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"*{timestamp}*")

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Format prompt with context
                history = "\n".join(
                    f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in st.session_state.messages
                )
                full_prompt = f"{history}\nAssistant:"

                # Call Hugging Face Inference API
                api_url = f"https://api-inference.huggingface.co/models/{model_id}"
                headers = {"Authorization": f"Bearer {hf_token}"}
                payload = {
                    "inputs": full_prompt,
                    "parameters": {
                        "max_new_tokens": 256,
                        "temperature": 0.7,
                        "return_full_text": False
                    }
                }

                response = requests.post(api_url, headers=headers, json=payload)

                if response.status_code != 200:
                    st.error(f"API Error {response.status_code}: {response.text}")
                    st.stop()

                result = response.json()
                generated_text = result[0]["generated_text"].strip()

                # Extract only the assistant's reply
                reply = generated_text.split("Assistant:")[-1].strip()

                response_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.markdown(reply)
                st.caption(f"*{response_timestamp}*")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "timestamp": response_timestamp
                })

            except Exception as e:
                st.error(f"Error: {str(e)}")
