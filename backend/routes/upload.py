from src.rag_pipeline import RAGPipeline
from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()
rag = RAGPipeline()

UPLOAD_DIR = "data"

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:

        content = await file.read()

        f.write(content)

    chunks = rag.ingest_documents(
        [file_path]
    )

    return {
        "message":
            "File uploaded and indexed",

        "filename":
            file.filename,

        "chunks":
            chunks
    }