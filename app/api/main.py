from fastapi import FastAPI, HTTPException, Query
from app.rag.engine import RAGEngine

app = FastAPI(title="RAG Application with LangChain")

rag_engine = RAGEngine()


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "RAG API with LangChain & Groq is up and running!",
        "docs": "/docs",
        "example_query": "/query?question=What is the main topic of this document?"
    }


@app.get("/query")
def query_documents(question: str = Query(..., description="User question")):
    """
    Return an LLM generated answer, grounded using the PDF content.
    """
    try:
        answer = rag_engine.generate_answer(question)
        return {
            "question": question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))