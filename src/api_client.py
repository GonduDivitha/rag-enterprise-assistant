import requests

API_URL = "http://127.0.0.1:8000"


class APIClient:
    @staticmethod
    def ask(question):
        """Send a question to the backend /chat endpoint and return JSON response."""
        response = requests.post(
            f"{API_URL}/chat",
            params={"question": question},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def upload(file_path):
        """Upload a file to the backend /upload endpoint and return JSON response."""
        with open(file_path, "rb") as file:
            response = requests.post(
                f"{API_URL}/upload",
                files={"file": file},
            )
        response.raise_for_status()
        return response.json()