import chromadb
import uuid
from typing import List, Any
import os
import numpy as np
from pathlib import Path
from logger import get_logger
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

logger = get_logger(__name__)

persistant_path = Path(__file__).parent.parent / "database"

class VectorStore:
    """
    VectorStore: To Store the information in the vector database
    """
    
    def __init__(self, persistant_dir:str=persistant_path,
                 collection_name:str="text_files"):
        self.persistant_dir = persistant_dir
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self.initialize_store()
    
    def initialize_store(self):
        """
        Initializing Vector Store

        Raises:
            RuntimeError: Store Nor Initialized
        """
        
        try:
            os.makedirs(self.persistant_dir, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persistant_dir)
            self.collection = self.client.get_or_create_collection(
                self.collection_name,
                metadata={"description": "Text data"}
            )
            
            logger.info("Vector Store Initialized")
        
        except RuntimeError as e:
            logger.critical(f"Vector Store not Initialized: {e}")
            raise RuntimeError(f"Vector Store not Initialized: {e}") from e 
        
    def add_documents(self, documents:List[Any], embeddings:np.ndarray):
        """
        To adding documents in the store

        Args:
            documents (List[Any]): List of Documents
            embeddings (np.ndarray): Generated Embeddings from the EmbeddingManager

        Raises:
            RuntimeError: Length of Documents and Embeddings should be Same
            RuntimeError: Document Not Added Successfully
        """
        
        if len(documents) != len(embeddings):
            logger.error("Length of Documents and Embeddings should be Same")
            raise RuntimeError("Length of Documents and Embeddings should be Same")
        
        doc_ids = []
        metadatas = []
        document_texts = []
        embedding_lists = []
        
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            ids = f"doc_{uuid.uuid4().hex[:8]}_19"
            doc_ids.append(ids)
            metadata = dict(doc.metadata) 
            metadata["doc_index"] = i
            metadata["content_length"] = len(doc.page_content)
            metadatas.append(metadata)
            document_texts.append(doc.page_content)
            # Convert embedding to list if it's numpy array
            if isinstance(embedding, np.ndarray):
                embedding_lists.append(embedding.tolist())
            else:
                embedding_lists.append(embedding)

        try:
            self.collection.add(
                ids=doc_ids,
                embeddings=embedding_lists,
                metadatas=metadatas,
                documents=document_texts
            )
            
            logger.info("Document Added successfully")
        
        except RuntimeError as e:
            logger.critical(f"Document Not Added Successfully: {e}")
            raise RuntimeError(f"Document Not Added Successfully: {e}") from e 