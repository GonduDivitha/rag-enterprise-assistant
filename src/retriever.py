import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class Retriever:
    """
    Handles semantic retrieval from FAISS.
    """

    def __init__(
        self,
        vector_db,
        top_k: int = 5
    ):
        self.vector_db = vector_db
        self.top_k = top_k

    def retrieve(
        self,
        query: str
    ):
        """
        Retrieve relevant documents with similarity scores.
        """

        try:

            results = self.vector_db.similarity_search_with_score(
                query,
                k=self.top_k
            )

            logger.info(
                f"Retrieved {len(results)} documents "
                f"for query: {query}"
            )

            return results

        except Exception as e:
            logger.error(
                f"Retrieval failed: {str(e)}"
            )
            raise

    def get_context(
        self,
        query: str
    ) -> str:
        """
        Create context string for LLM.
        """

        results = self.retrieve(query)

        context_parts = []

        for doc, _ in results:
            context_parts.append(
                doc.page_content
            )

        return "\n\n".join(context_parts)

    def get_sources(
        self,
        results
    ) -> List[Dict[str, Any]]:
        """
        Extract source metadata and confidence score.
        """

        sources = []

        for doc, score in results:

            metadata = doc.metadata

            confidence = round(
                1 / (1 + score),
                4
            )

            sources.append(
                {
                    "source": metadata.get(
                        "source",
                        "Unknown"
                    ),
                    "page": metadata.get(
                        "page",
                        "N/A"
                    ),
                    "chunk_id": metadata.get(
                        "chunk_id",
                        "N/A"
                    ),
                    "confidence_score": confidence
                }
            )

        return sources

    def retrieve_with_sources(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Complete retrieval package for RAG pipeline.
        """

        results = self.retrieve(query)

        context = "\n\n".join(
            [
                doc.page_content
                for doc, _ in results
            ]
        )

        sources = self.get_sources(
            results
        )

        return {
            "context": context,
            "sources": sources,
            "results": results
        }