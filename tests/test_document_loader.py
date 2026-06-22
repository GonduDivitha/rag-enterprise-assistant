from document_loader import DocumentLoader

documents = DocumentLoader.load_document(
    "data/sample.txt"
)

print(documents[0].page_content[:200])
print(documents[0].metadata)