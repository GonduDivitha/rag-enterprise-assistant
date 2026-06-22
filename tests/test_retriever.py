from embeddings import EmbeddingModel
from vector_store import VectorStore
from retriever import Retriever


embeddings = EmbeddingModel().get_embeddings()

vector_store = VectorStore(
    embeddings
)

db = vector_store.load_index()

retriever = Retriever(
    db,
    top_k=3
)

results = retriever.retrieve(
    "What is Retrieval Augmented Generation?"
)

for doc, score in results:

    print("\nScore:", score)

    print(doc.page_content)

    print(doc.metadata)