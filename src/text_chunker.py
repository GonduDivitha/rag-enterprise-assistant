from typing import List
import logging

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Splits documents into smaller chunks suitable for
    embedding generation and semantic retrieval.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def chunk_documents(
        self,
        documents: List[Document]
    ) -> List[Document]:
        """
        Split documents into chunks while preserving metadata.
        """

        if not documents:
            logger.warning(
                "No documents provided for chunking."
            )
            return []

        try:
            chunks = self.splitter.split_documents(
                documents
            )

            for idx, chunk in enumerate(chunks):
                chunk.metadata["chunk_id"] = idx + 1

            logger.info(
                f"Chunking completed. "
                f"Documents: {len(documents)} | "
                f"Chunks: {len(chunks)}"
            )

            return chunks

        except Exception as e:
            logger.error(
                f"Error while chunking documents: {str(e)}"
            )
            raise

    def get_chunk_statistics(
        self,
        chunks: List[Document]
    ) -> dict:
        """
        Returns chunking statistics for monitoring
        and debugging.
        """

        if not chunks:
            return {
                "total_chunks": 0,
                "average_chunk_length": 0,
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap
            }

        total_chunks = len(chunks)

        average_length = (
            sum(
                len(chunk.page_content)
                for chunk in chunks
            )
            / total_chunks
        )

        return {
            "total_chunks": total_chunks,
            "average_chunk_length": round(
                average_length,
                2
            ),
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap
        }