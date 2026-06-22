

import streamlit as st
import os
import sys
import logging



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
# ==========================================
# Configure Python Path
# ==========================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ==========================================
# Import RAG Pipeline
# ==========================================

from src.rag_pipeline import RAGPipeline
from src.pdf_export import PDFExporter
from src.azure_storage import AzureBlobStorage
from src.api_client import APIClient

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# Load CSS
# ==========================================

css_path = os.path.join(
    CURRENT_DIR,
    "assets",
    "style.css"
)

if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ==========================================
# Session State
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []
current_question = st.chat_input(
    "Ask a question about your documents..."
)





# ==========================================
# Initialize RAG Pipeline
# ==========================================

if "rag_pipeline" not in st.session_state:
    try:
        st.session_state.rag_pipeline = RAGPipeline()
    except Exception as e:
        st.error(
            f"Failed to initialize RAG Pipeline: {e}"
        )
        st.stop()

rag = st.session_state.rag_pipeline
azure = AzureBlobStorage()
try:
    azure_file_count = len(
        azure.list_files()
    )
except:
    azure_file_count = 0


# ==========================================
# Header
# ==========================================

st.markdown("""
<div style="
background: linear-gradient(135deg,#1e293b,#172554);
padding:25px;
border-radius:18px;
margin-bottom:20px;
border:1px solid #334155;
text-align:center;
">
<h1 style="
margin:0;
font-size:2.8rem;
color:white;
font-weight:800;
">
🤖 Enterprise Knowledge Assistant
</h1>

<p style="
margin-top:10px;
color:#94A3B8;
font-size:1.1rem;
">
AI-Powered Enterprise Knowledge Retrieval System
</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# Data Directory
# ==========================================

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# ==========================================
# Metrics
# ==========================================

document_count = len([
    f for f in os.listdir(DATA_DIR)
    if os.path.isfile(os.path.join(DATA_DIR, f))
])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h4>📄 Documents</h4>
        <h2>{document_count}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
      <h4>☁️ Azure Files</h4>
      <h2>{azure_file_count}</h2>
    </div>
    """, unsafe_allow_html=True)
    
with col3:

    user_questions = sum(
        1
        for msg in st.session_state.messages
        if msg.get("role") == "user"
    )

    if current_question:
        user_questions += 1

    st.markdown(f"""
    <div class="metric-card">
      <h4>💬 Questions</h4>
      <h2>{user_questions}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h4>⚡ Model</h4>
        <h2>Llama 3.2</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="status-banner">
🟢 Ollama Connected &nbsp;&nbsp;|&nbsp;&nbsp;
🟢 FAISS Ready &nbsp;&nbsp;|&nbsp;&nbsp;
🟢 Enterprise RAG Active
</div>
""", unsafe_allow_html=True)

# ==========================================
# Sidebar
# ==========================================



with st.sidebar:

    st.header("📂 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload Files",
        type=["pdf", "docx", "txt", "csv"],
        accept_multiple_files=True
    )

    if st.button("🚀 Process Documents"):

        if uploaded_files:
            try:
                with st.spinner(
                    "Uploading and indexing documents..."
                ):

                    uploaded_count = 0
                    file_paths = []

                    for uploaded_file in uploaded_files:

                        save_path = os.path.join(
                            DATA_DIR,
                            uploaded_file.name
                        )

                        with open(save_path, "wb") as f:
                            f.write(
                                uploaded_file.getbuffer()
                            )

                        with open(save_path, "rb") as file_data:
                            azure.upload_file(
                                uploaded_file.name,
                                file_data
                            )

                        file_paths.append(save_path)

                        result = APIClient.upload(
                            save_path
                        )

                        uploaded_count += 1

                st.success(
                    f"Successfully uploaded and indexed "
                    f"{uploaded_count} file(s)."
                )

            except Exception as e:

                st.error(
                    f"Upload failed: {e}"
                )
    st.markdown("---")

# ==========================================
# Download Chat PDF
# ==========================================

    if st.session_state.messages:
        pdf_file = PDFExporter.create_chat_pdf(
            st.session_state.messages
        )

        with open(pdf_file, "rb") as file:
            st.download_button(
                label="📥 Download Chat PDF",
                data=file.read(),
                file_name="chat_history.pdf",
                mime="application/pdf"
            )

# ==========================================
# Clear Chat
# ==========================================

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []

        st.rerun()

# ==========================================
# Chat History
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# Chat Input
# ==========================================


if current_question:

    

    st.session_state.messages.append(
    {
        "role": "user",
        "content": current_question
    }
)

    with st.chat_message("user"):
        st.markdown(current_question)

    with st.spinner("🤖 Searching documents..."):
        try:
            chat_history = ""

            for msg in st.session_state.messages[-20:]:
                role = msg["role"]

                content = msg["content"]

                chat_history += (
                f"{role}: {content}\n"
            )

            result = APIClient.ask(
             current_question
            )

            answer = result.get(
            "answer",
            "No answer found."
            )

            confidence = result.get(
            "confidence",
            0.0
            )

            sources = result.get(
            "sources",
            []
            )

            source_details = []

        except Exception as e:
            answer = f"Error: {e}"

            confidence = 0.0

            sources = []

            source_details = []

    with st.chat_message("assistant"):

        st.markdown(answer)

        # ==================================
        # Source Documents
        # ==================================

        if source_details:

            st.markdown("### 📄 Sources")

            for item in source_details:

                with st.expander(
                    f"📄 {item['source']}"
                ):

                    st.write(
                         f"Page: {item.get('page', 'N/A')}"
                    )

                    st.write(
                         f"Chunk ID: {item.get('chunk_id', 'N/A')}"
                    )

                    st.write(
                        item["preview"]
                    )

        elif sources:

            st.markdown("### 📄 Sources")

            for source in sources:

                st.info(source)

        # ==================================
        # Confidence
        # ==================================

        st.markdown("### 🎯 Confidence")

        confidence = float(
            max(
                0,
                min(
                    confidence,
                    100
                )
            )
        )

        st.progress(
            confidence / 100
        )

        if confidence >= 80:

            st.success(
                f"High Confidence ({confidence:.2f}%)"
            )

        elif confidence >= 50:

            st.warning(
                f"Medium Confidence ({confidence:.2f}%)"
            )

        else:

            st.error(
                f"Low Confidence ({confidence:.2f}%)"
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.session_state.pdf_file = (
     PDFExporter.create_chat_pdf(
        st.session_state.messages
    )
)

# ==========================================
# Footer
# ==========================================

