from fastapi import APIRouter
from src.rag_pipeline import RAGPipeline

router = APIRouter()

rag = RAGPipeline()

@router.post("/chat")
def chat(question: str):

    try:

        print(f"Received Question: {question}")

        result = rag.ask(question)

        print("Answer Generated Successfully")

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