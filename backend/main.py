from fastapi import FastAPI
from backend.routes.chat import router as chat_router
from backend.routes.upload import router as upload_router

app = FastAPI(
    title="Enterprise RAG API",
    version="1.0.0"
)

app.include_router(chat_router)
app.include_router(upload_router)

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "Enterprise RAG API"
    }