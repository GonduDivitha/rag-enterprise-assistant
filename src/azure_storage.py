import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()


class AzureBlobStorage:
    def __init__(self):
        self.connection_string = os.getenv(
            "AZURE_STORAGE_CONNECTION_STRING"
        )

        self.container_name = os.getenv(
            "AZURE_CONTAINER_NAME",
            "documents"
        )

        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )

        self.container_client = self.blob_service_client.get_container_client(
            self.container_name
        )

    def upload_file(self, file_name, file_data):
        """
        Upload file to Azure Blob Storage
        """

        blob_client = self.container_client.get_blob_client(
            blob=file_name
        )

        blob_client.upload_blob(
            file_data,
            overwrite=True
        )

        return blob_client.url

    def list_files(self):
        """
        List all blobs in container
        """

        return [
            blob.name
            for blob in self.container_client.list_blobs()
        ]

    def delete_file(self, file_name):
        """
        Delete blob
        """

        self.container_client.delete_blob(file_name)

    def download_file(self, file_name):
        """
        Download blob content
        """

        blob_client = self.container_client.get_blob_client(
            file_name
        )

        return blob_client.download_blob().readall()