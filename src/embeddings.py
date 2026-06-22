import logging
from typing import Optional

from langchain_community.embeddings import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)


class EmbeddingModel:
    """
    Handles embedding generation using
    BAAI/bge-small-en-v1.5.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
        device: str = "cpu"
    ):
        self.model_name = model_name
        self.device = device

        try:
            logger.info(
                f"Loading embedding model: {model_name}"
            )

            self.embeddings = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={
                    "device": device
                },
                encode_kwargs={
                    "normalize_embeddings": True
                }
            )

            logger.info(
                f"Embedding model loaded successfully: {model_name}"
            )

        except Exception as e:
            logger.error(
                f"Failed to load embedding model: {str(e)}"
            )
            raise

    def get_embeddings(self):
        """
        Returns LangChain embedding object.
        """
        return self.embeddings

    def get_embedding_dimension(self) -> Optional[int]:
        """
        Returns embedding vector dimension.
        Useful for FAISS validation.
        """

        try:
            sample_embedding = self.embeddings.embed_query(
                "test"
            )

            return len(sample_embedding)

        except Exception as e:
            logger.error(
                f"Failed to determine embedding dimension: {str(e)}"
            )
            return None

    def test_embedding(self):
        """
        Generate a test embedding to verify
        model functionality.
        """

        try:
            vector = self.embeddings.embed_query(
                "Hello world"
            )

            logger.info(
                f"Embedding generated successfully. "
                f"Dimension: {len(vector)}"
            )

            return vector

        except Exception as e:
            logger.error(
                f"Embedding test failed: {str(e)}"
            )
            raise