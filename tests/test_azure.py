import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from src.azure_storage import AzureBlobStorage

azure = AzureBlobStorage()

with open("data/sample.txt", "rb") as f:
    url = azure.upload_file(
        "sample.txt",
        f
    )

print("Uploaded Successfully")
print("Blob URL:", url)

print("Files in Azure:")
print(azure.list_files())