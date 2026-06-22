from embeddings import EmbeddingModel
from vector_store import VectorStore


embeddings = EmbeddingModel().get_embeddings()

vector_store = VectorStore(
    embeddings
)

db = vector_store.load_index()

results = db.similarity_search(
    "What is Retrieval Augmented Generation?",
    k=3
)

for i, result in enumerate(results):

    print(f"\nResult {i+1}")

    print(result.page_content)