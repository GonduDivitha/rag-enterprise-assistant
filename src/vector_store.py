from pathlib import Path
from typing import List
import logging

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Handles FAISS vector database operations:
    - Create index
    - Save index
    - Load index
    """

    def __init__(self, embeddings):
        self.embeddings = embeddings

    def create_index(
        self,
        documents: List[Document]
    ):
        """
        Create FAISS index from documents.
        """

        if not documents:
            raise ValueError(
                "No documents provided for indexing."
            )

        try:

            logger.info(
                f"Creating FAISS index with "
                f"{len(documents)} chunks."
            )

            vector_db = FAISS.from_documents(
                documents,
                self.embeddings
            )

            logger.info(
                "FAISS index created successfully."
            )

            return vector_db

        except Exception as e:
            logger.error(
                f"Failed to create FAISS index: {str(e)}"
            )
            raise

    def save_index(
        self,
        vector_db,
        save_path: str = "vector_db/faiss_index"
    ):
        """
        Save FAISS index locally.
        """

        try:

            Path(save_path).parent.mkdir(
                parents=True,
                exist_ok=True
            )

            vector_db.save_local(
                save_path
            )

            logger.info(
                f"FAISS index saved at: {save_path}"
            )

        except Exception as e:
            logger.error(
                f"Failed to save FAISS index: {str(e)}"
            )
            raise

    def load_index(
        self,
        save_path: str = "vector_db/faiss_index"
    ):
        """
        Load existing FAISS index.
        """

        try:

            index_file = Path(save_path)

            if not index_file.exists():
                raise FileNotFoundError(
                    f"FAISS index not found: {save_path}"
                )

            logger.info(
                f"Loading FAISS index from: {save_path}"
            )

            vector_db = FAISS.load_local(
                save_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )

            logger.info(
                "FAISS index loaded successfully."
            )

            return vector_db

        except Exception as e:
            logger.error(
                f"Failed to load FAISS index: {str(e)}"
            )
            raise

    def index_exists(
        self,
        save_path: str = "vector_db/faiss_index"
    ) -> bool:
        """
        Check whether FAISS index exists.
        """

        return Path(save_path).exists()

    def get_document_count(
        self,
        vector_db
    ) -> int:
        """
        Returns total vectors stored in FAISS.
        """

        try:
            return vector_db.index.ntotal

        except Exception:
            return 0