from document_loader import DocumentLoader
from text_chunker import TextChunker
from embeddings import EmbeddingModel
from vector_store import VectorStore


documents = DocumentLoader.load_document(
    "data/sample.txt"
)

chunker = TextChunker(
    chunk_size=100,
    chunk_overlap=20
)

chunks = chunker.chunk_documents(
    documents
)

embedding_model = EmbeddingModel()

embeddings = embedding_model.get_embeddings()

vector_store = VectorStore(
    embeddings
)

db = vector_store.create_index(
    chunks
)

vector_store.save_index(
    db
)

print("FAISS Index Saved Successfully")