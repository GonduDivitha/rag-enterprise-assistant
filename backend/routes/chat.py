from fastapi import APIRouter
from src.rag_pipeline import RAGPipeline

router = APIRouter()

rag = RAGPipeline()

@router.post("/chat")
def chat(question: str):

    try:

        result = rag.ask(question)

        return {
         "question": str(question),
         "answer": str(result["answer"]),
         "confidence": float(result["confidence"]),
         "sources": [str(s) for s in result["sources"]]
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
    print(type(result["confidence"]))
    print(result)