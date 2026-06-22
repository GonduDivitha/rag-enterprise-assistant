from document_loader import DocumentLoader
from text_chunker import TextChunker

documents = DocumentLoader.load_document(
    "data/sample.txt"
)

chunker = TextChunker(
    chunk_size=50,
    chunk_overlap=10
)

chunks = chunker.chunk_documents(documents)

print(f"Total Chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print(chunk.page_content)