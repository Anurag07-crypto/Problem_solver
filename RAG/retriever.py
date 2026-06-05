import sys 
from pathlib import Path
from typing_extensions import List, Dict, Any
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
    """
    def __init__(self,
                 vector_store:VectorStore=None,
                 embedding_manager:EmbeddingManager=None):
        self.vector_store = vector_store if vector_store is not None else VectorStore()
        self.embedding_manager = embedding_manager if embedding_manager is not None else EmbeddingManager()
    
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
        

data = Ingestion()
if not data:
    logger.warning("No documents found in text_docs directory")

embedding_manager = EmbeddingManager()
vector_store = VectorStore()     

chunks = Splitter(data)
texts = [doc.page_content for doc in chunks]
embeddings = embedding_manager.generate_embeddings(texts)
vector_store.add_documents(chunks, embeddings)
logger.info(f"DATA LOADED successfully: {len(chunks)} chunks indexed")

                   
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
    