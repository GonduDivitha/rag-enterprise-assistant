import logging

from src.document_loader import DocumentLoader
from src.text_chunker import TextChunker
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.retriever import Retriever
from src.llm_handler import LLMHandler

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Main RAG workflow:
    Upload -> Chunk -> Embed -> Store
    Retrieve -> Generate Answer
    """

    def __init__(self):

        logger.info(
            "Initializing RAG Pipeline..."
        )

        self.embeddings = (
            EmbeddingModel()
            .get_embeddings()
        )

        self.vector_store = VectorStore(
            self.embeddings
        )

        self.llm = LLMHandler()

        self.db = None
        chunks = None

        if self.vector_store.index_exists():
            try:

                print("\n========== DOCUMENTS ==========")

                if "chunks" in locals():
                    for chunk in chunks:
                        print(
                            chunk.metadata.get("source"),
                            "|",
                            chunk.page_content[:100]
                        )

                    print("===============================\n")

                self.db = (
                    self.vector_store.load_index()
                )

                logger.info(
                    "Existing FAISS index loaded."
                )

            except Exception as e:

                logger.error(
                    f"Failed to load FAISS index: {str(e)}"
                )

    def ingest_documents(
        self,
        file_paths
    ):

        logger.info(
            f"Processing {len(file_paths)} files."
        )

        all_documents = []

        for file_path in file_paths:

            documents = (
                DocumentLoader.load_document(
                    file_path
                )
            )

            print(
              "Loaded:",
               file_path,
               "Documents:",
               len(documents)
            )

            all_documents.extend(
                documents
            )

        chunker = TextChunker(
            chunk_size=800,
            chunk_overlap=150
        )

        chunks = (
            chunker.chunk_documents(
                all_documents
            )
        )

        logger.info(
            f"Generated {len(chunks)} chunks."
        )

        if self.db is None:

            self.db = (
                self.vector_store.create_index(
                    chunks
                )
            )

        else:

            self.db.add_documents(
                chunks
            )


        print(
           "Total vectors:",
            self.db.index.ntotal
        ) 

        self.vector_store.save_index(
            self.db
        )

        logger.info(
            "FAISS index saved successfully."
        )

        return len(chunks)

    def ask(
        self,
        question: str,
        chat_history: str = ""
    ):

        if self.db is None:

            if self.vector_store.index_exists():

                self.db = (
                    self.vector_store.load_index()
                )

            else:

                return {
                    "answer":
                    "No documents have been uploaded yet.",
                    "sources": [],
                    "source_details": [],
                    "confidence": 0
                }

        retriever = Retriever(
            self.db,
            top_k=2
        )

        retrieval_data = (
            retriever.retrieve_with_sources(
                question
            )
        )

        print("\n====== RETRIEVED DOCS ======")

        for doc, score in retrieval_data["results"]:
            print(
                doc.metadata.get("source"),
                score
            )

        print("===========================\n")

        context = retrieval_data["context"]
        sources = retrieval_data["sources"]

        answer = self.llm.generate_answer(
            question=question,
            context=context,
            chat_history=chat_history
        )

        confidence = 0

        if sources:

            confidence = float(
                round(
                    max(
                        source["confidence_score"]
                        for source in sources
                    ) * 100,
                    2
                )
            )

        source_details = []

        seen_sources = set()

        for doc, _ in retrieval_data["results"]:

            source_name = doc.metadata.get(
                "source",
                "Unknown"
            )

            if source_name not in seen_sources:

                source_details.append(
                    {
                        "source": source_name,
                        "page": doc.metadata.get(
                            "page",
                            "N/A"
                        ),
                        "chunk_id": doc.metadata.get(
                            "chunk_id",
                            "N/A"
                        ),
                        "preview": (
                            doc.page_content[:300]
                        )
                    }
                )

                seen_sources.add(
                    source_name
                )

        return {
            "answer": answer,
            "sources": list(
                set(
                    [
                        source["source"]
                        for source in sources
                    ]
                )
            ),
            "source_details": source_details,
            "confidence": confidence
        }