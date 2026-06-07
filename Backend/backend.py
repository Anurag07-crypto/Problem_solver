import sys 
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
import uvicorn
from RAG.retriever import Retriever, llm_response
from pydantic import BaseModel
from logger import get_logger

logger = get_logger(__name__)

class Request(BaseModel):
    query: str

app = FastAPI(title="Problem Solver RAG API")

@app.get("/health")
def health_check():
    """Quick health check endpoint"""
    return {"status": "healthy", "service": "Problem Solver"}

@app.get("/status")
def status():
    """Get initialization status"""
    # TODO: You can add RAG status checking here
    return {
        "status": "ready",
        "message": "RAG system will initialize on first request"
    }

@app.post("/chat")
def chat(request: Request):
    
    """Handle incoming chat queries through RAG pipeline.

    Args:
        request (Request): Request object containing the user query

    Raises:
        HTTPException: On runtime or unexpected errors

    Returns:
        Dict with 'response' key containing the agent's answer
    """
    
    try:
        logger.info(f"Received query: {request.query[:100]}...")
        
        # Create retriever instance - will lazy-load RAG components on first use
        retriever_instance = Retriever()
        response = llm_response(request.query, retriever=retriever_instance)
        logger.info("Request processed successfully")        
   
        return {"response": response}
    except RuntimeError as e:
        logger.error(f"Runtime error in /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except UnicodeEncodeError as e:
        logger.error(f"Unicode encoding error in /chat: {e}")
        raise HTTPException(status_code=500, detail="Error processing response with special characters")
    except Exception as e:
        logger.error(f"Unexpected error in /chat: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong. please try again")
        # raise HTTPException(
        #     status_code=500,
        #     detail="Something went wrong. please try again")

if __name__ == "__main__":
    
    uvicorn.run("backend:app", port=8000, host="0.0.0.0", reload=False)