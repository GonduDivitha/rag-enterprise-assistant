from embeddings import EmbeddingModel

embedding_model = EmbeddingModel()

embeddings = embedding_model.get_embeddings()

vector = embeddings.embed_query(
    "What is Retrieval Augmented Generation?"
)

print("Embedding Length:", len(vector))

print("First 10 Values:")

print(vector[:10])