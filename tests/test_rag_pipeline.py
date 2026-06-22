from rag_pipeline import RAGPipeline

rag = RAGPipeline()

result = rag.ask(
    "What is Retrieval Augmented Generation?"
)

print("\nANSWER:\n")

print(result["answer"])

print("\nSOURCES:\n")

print(result["sources"])