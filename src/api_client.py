import os
import requests

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


class APIClient:
    @staticmethod
    def ask(question):
        response = requests.post(
            f"{API_URL}/chat",
            params={"question": question},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def upload(file_path):
        with open(file_path, "rb") as file:
            response = requests.post(
                f"{API_URL}/upload",
                files={"file": file},
            )
        response.raise_for_status()
        return response.json()