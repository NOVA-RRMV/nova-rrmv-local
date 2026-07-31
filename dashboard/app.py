"""RagEngine Dashboard — Streamlit web interface."""

import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="RagEngine",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 RagEngine — RAG Engine")
st.markdown("*Ask questions about your documents*")

# Sidebar
with st.sidebar:
    st.header("Settings")
    try:
        resp = requests.get(f"{API_URL}/api/collections")
        collections = resp.json().get("collections", ["default"])
    except requests.ConnectionError:
        collections = ["default"]
    collection = st.selectbox("Collection Name", options=collections)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()  
    st.header("Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["txt", "md", "pdf", "docx"],
    )

    if uploaded_file and st.button("Upload"):
        with st.spinner("Uploading and processing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            try:
                response = requests.post(f"{API_URL}/api/upload", files=files)
                if response.status_code == 200:
                    st.success(f"✅ Uploaded: {response.json()['chunks_stored']} chunks stored")
                else:
                    st.error(f"Error: {response.text}")
            except requests.ConnectionError:
                st.error("❌ Cannot connect to API server")

# Main chat interface
st.header("💬 Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if not st.session_state.messages:
    st.info("👋 Welcome! Upload a document on the left, then ask me anything about it.")
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("Searching and generating answer..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/query",
                    json={
                        "question": prompt,
                        "collection": collection,
                    },
                )

                if response.status_code == 200:
                    data = response.json()
                    st.markdown(data["answer"])

                    # Show sources
                    if data.get("sources"):
                        with st.expander("📚 Sources"):
                            for i, source in enumerate(data["sources"], 1):
                                st.markdown(f"**Source {i}** (score: {source.get('score', 'N/A'):.2f})")
                                st.text(source.get("text", "")[:200] + "...")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["answer"],
                    })
                else:
                    st.error(f"Error: {response.text}")
            except requests.ConnectionError:
                st.error("❌ Cannot connect to API server. Make sure the backend is running.")
