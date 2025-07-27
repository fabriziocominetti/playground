import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from datetime import datetime

st.title("💻 Local Chatbot")

# Sidebar for model selection
with st.sidebar:
    st.header("Model Loader")
    model_id = st.selectbox(
        "Choose a model:",
        ["", "HuggingFaceH4/zephyr-7b-beta", "tiiuae/falcon-7b-instruct", "gpt2"],
        index=0
    )
    max_tokens = st.slider("Max response length:", 64, 512, 256)
    temperature = st.slider("Creativity (temperature):", 0.0, 1.5, 0.7)

# Load model only after selection
@st.cache_resource
def load_pipeline(model_id):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"
    )
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

# Don't load model unless selected
if model_id:
    generator = load_pipeline(model_id)
    st.success(f"Model `{model_id}` loaded.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            st.caption(f"*{msg['timestamp']}*")

    # Handle new prompt
    if prompt := st.chat_input("Ask something..."):
        st.chat_message("user").markdown(prompt)
        user_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": user_time})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                history = "\n".join(
                    f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}" for m in st.session_state.messages
                )
                full_prompt = f"{history}\nAssistant:"
                output = generator(
                    full_prompt,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    return_full_text=False
                )
                reply = output[0]["generated_text"].strip()
                st.markdown(reply)
                reply_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.caption(f"*{reply_time}*")
                st.session_state.messages.append({"role": "assistant", "content": reply, "timestamp": reply_time})
else:
    st.warning("Please select a model in the sidebar to start.")
