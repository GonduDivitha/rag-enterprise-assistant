import streamlit as st
import os
import sys

sys.path.append(
    os.path.abspath("src")
)

from rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Enterprise Knowledge Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

rag = RAGPipeline()

# Sidebar
with st.sidebar:

    st.header("📁 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf", "docx", "txt", "csv"],
        accept_multiple_files=True
    )

    if st.button("Process Documents"):

        if uploaded_files:

            file_paths = []

            for uploaded_file in uploaded_files:

                save_path = os.path.join(
                    "data",
                    uploaded_file.name
                )

                with open(
                    save_path,
                    "wb"
                ) as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )

                file_paths.append(
                    save_path
                )

            chunks = rag.ingest_documents(
                file_paths
            )

            st.success(
                f"Processed {chunks} chunks successfully!"
            )

# Display Chat History
for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# Chat Input
question = st.chat_input(
    "Ask a question about your documents..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    result = rag.ask(question)

    answer = result["answer"]

    sources = result["sources"]

    confidence = result["confidence"]

    response = f"""
{answer}

### Sources
{', '.join(sources)}

### Confidence
{confidence}
"""

    with st.chat_message("assistant"):

        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )