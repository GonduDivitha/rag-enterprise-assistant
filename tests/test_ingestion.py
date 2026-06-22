import sys
import os

sys.path.append(
    os.path.abspath("src")
)

from rag_pipeline import RAGPipeline


rag = RAGPipeline()

chunks = rag.ingest_documents(
    ["data/sample.txt"]
)

print(
    f"Chunks Created: {chunks}"
)