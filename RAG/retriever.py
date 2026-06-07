import sys 
from pathlib import Path
from typing import List, Dict, Any
from groq import Client
import os
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from RAG.data_ingestion import Splitter, Ingestion
from RAG.embedding_manager import EmbeddingManager
from RAG.vector_store import VectorStore
from logger import get_logger

logger = get_logger(__name__)

class Retriever:
    """
    Retriever: Mechanism to getting the RAG response out
    Uses lazy initialization - only loads models/docs when first query is made
    """
    def __init__(self,
                 vector_store:VectorStore=None,
                 embedding_manager:EmbeddingManager=None):
        self._initialized = False
        self._embedding_manager = embedding_manager
        self._vector_store = vector_store
    
    def _ensure_initialized(self):
        """Lazy initialization on first use"""
        if self._initialized:
            return
        
        logger.info("🔄 Initializing RAG components on first query...")
        try:
            embedding_manager, vector_store = get_rag_components()
            self._embedding_manager = embedding_manager
            self._vector_store = vector_store
            self._initialized = True
            logger.info("✓ RAG components ready")
        except Exception as e:
            logger.error(f"Failed to initialize RAG: {e}", exc_info=True)
            raise
    
    @property
    def embedding_manager(self):
        self._ensure_initialized()
        return self._embedding_manager
    
    @property
    def vector_store(self):
        self._ensure_initialized()
        return self._vector_store
    
    def retrieve(self, query:str, top_k:int = 5, threshold=0.3)->List[Dict[str, Any]]:
        """
        Retrieving RAG Docs

        Args:
            query (str): Qurey By user
            top_k (int, optional): Number of results. Defaults to 5.
            threshold (float, optional): scoring value. Defaults to 0.3.

        Raises:
            FileNotFoundError: File Not found

        Returns:
            List[Dict[str, Any]]: Retrieved_Docs
        """
        try:
             embeddings = self.embedding_manager.generate_embeddings([query])[0]
             results = self.vector_store.collection.query(
                 embeddings,
                 n_results=top_k,
                 include= ["metadatas", "documents", "distances"]
             )      
             
             retrieved_docs = []
             
             if results["documents"] and len(results["documents"]) > 0 and len(results["documents"]) > 0:
                documents = results["documents"][0]
                metadatas = results["metadatas"][0]
                distances = results["distances"][0]
                ids = results["ids"][0]
                
                for i,(doc, metadata, distance, doc_id) in enumerate(
                    zip(
                        documents,metadatas, distances, ids
                    )
                ):
                     
                    similarity_socre = 1 - distance
                    
                    if similarity_socre < threshold:
                        continue
                    
                    retrieved_docs.append(
                        {
                            "id": doc_id,
                            "metadata": metadata,
                            "distance": distance,
                            "similarity_score": similarity_socre,
                            "rank": i
                        }
                    )
                    
                    if not retrieved_docs:
                        logger.warning("No relevant documents found for query")
                        return []
 
                    logger.info(
                                f"Retrieved {len(retrieved_docs)} documents"
                                )
                    return retrieved_docs
        
        except FileNotFoundError as e:
            logger.critical(F"File not Retrieved: {e}")
            raise FileNotFoundError(f"File not Retrieved: {e}") from e


def initialize_rag():
    """Initialize RAG components - loads docs, chunks them, and stores embeddings"""
    try:
        logger.info("Starting RAG initialization...")
        data = Ingestion()
        if not data:
            logger.warning("No documents found in text_docs directory")
            return None, None, None

        embedding_manager = EmbeddingManager()
        vector_store = VectorStore()     

        chunks = Splitter(data)
        logger.info(f"Generated {len(chunks)} chunks")
        
        # ✅ Store chunks in vector store with embeddings
        if chunks:
            logger.info("Storing chunks in vector store...")
            for i, chunk in enumerate(chunks):
                chunk_id = f"chunk_{i}"
                # Generate embedding for this chunk
                embedding = embedding_manager.generate_embeddings([chunk.page_content])[0]
                
                # Add to vector store
                vector_store.collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding.tolist()],  # Convert numpy array to list
                    documents=[chunk.page_content],
                    metadatas=[{
                        "source": chunk.metadata.get("source", "unknown"),
                        "chunk_index": i
                    }]
                )
            logger.info(f"Successfully stored {len(chunks)} chunks in vector store")
        
        logger.info("RAG initialization completed successfully")
        return embedding_manager, vector_store, chunks
    except Exception as e:
        logger.error(f"Error during RAG initialization: {e}", exc_info=True)
        raise

_rag_initialized = False
_embedding_manager = None
_vector_store = None

def get_rag_components():
    """Get or initialize RAG components (blocks on first call only)"""
    global _rag_initialized, _embedding_manager, _vector_store
    
    if _rag_initialized:
        return _embedding_manager, _vector_store
    
    logger.info("📊 Initializing RAG components...")
    logger.info("⏳ First run may take 5-15 minutes (downloading 100MB model, processing documents)")
    
    _embedding_manager, _vector_store, chunks = initialize_rag()
    _rag_initialized = True
    logger.info(f"✓ RAG ready with {len(chunks) if chunks else 0} chunks")
    
    return _embedding_manager, _vector_store

                   
def llm_response(query:str, retriever:Retriever):
    """
    For Getting LLM Response
    Query(Str): User Query
    Retriever: Retriever Class
    """    
    load_dotenv()
    API_KEY = os.getenv("GROQ_API_KEY")
    context = retriever.retrieve(query=query)
    
    Prompt = f"""
    You are a professional Data representator use the below context and query to give answer
    Query:-
    {query}
    Context:-
    {context}
    Some points to ensure before giving Answers:-
    1.Don't give anything out of the context 
    2.Reconstruct and give answer in professional prompt
    3.Only I need Proper answer
    Restrictions
    1.Don't Give extra knowledge
    2.Use only given context
    example:-
    user query- what is shortcut key for pasting
    bot response - Ctrl + V is used for pasting 
    """
    
    llm = Client(api_key=API_KEY)
    chat_completion = llm.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": Prompt,
        }
    ],
    model="llama-3.3-70b-versatile",
)
    
    response = chat_completion.choices[0].message.content
    return response
    