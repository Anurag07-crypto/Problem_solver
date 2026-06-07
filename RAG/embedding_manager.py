from sentence_transformers import SentenceTransformer
import numpy as np  
from typing import List
from logger import get_logger

logger = get_logger(__name__)

class EmbeddingManager:
    """EmbeddingManager: Manages the embeddings using SentenceTransformer"""
    
    def __init__(self, model_name:str="BAAI/bge-small-en-v1.5"):
        self.model_name=model_name
        self.model = None
        self.load_model()
        
    def load_model(self):
        """
        Loading Model

        Raises:
            RuntimeError: BAAI/bge-small-en-v1.5 model is not loaded
        """
        try:
            self.model = SentenceTransformer(model_name_or_path=self.model_name)
            logger.info("BAAI/bge-small-en-v1.5 model is loaded")
        except Exception as e:
            logger.error(f"BAAI/bge-small-en-v1.5 model is not loaded: {e}")
            raise RuntimeError(f"BAAI/bge-small-en-v1.5 model is not loaded: {e}") from e 
    
    def generate_embeddings(self, text:List[str])-> np.ndarray:
        """
            Generating Embeddings
        Args:
            text (List[str]): List of Documents

        Raises:
            ValueError: Cannot Generate Empty Embeddings
            RuntimeError: Embeddings not Generated

        Returns:
            np.ndarray: numpy array returns 
        """
        if not text:
            logger.critical("Cannot Generate Empty Embeddings")
            raise ValueError("Cannot Generate Empty Embeddings")
        
        try:
            embeddings = self.model.encode(text)
            logger.info("Embeddings Generated")
            return embeddings
        
        except Exception as e:
            logger.error(f"Embeddings not Generated: {e}")
            raise RuntimeError(f"Embeddings not Generated: {e}") from e
        