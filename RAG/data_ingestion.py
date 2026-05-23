from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger

logger = get_logger(__name__)

def Ingestion():
    """ Ingesting the Docs into RAG Pipeline """
    
    Dir_path = Path(__file__).parent.parent / "Docs"
    loader = DirectoryLoader(
        path=Dir_path,
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    
    load_file = loader.load()
    logger.info("Directory ingested")
    return load_file

def Splitter(list_of_docs, chunk_size:int = 1000 ,chunk_overlap:int=200):
    """ Splitting the ingested Docs into Chunks """
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_fun= len,
        separators=["\n\n\n", "\n\n", "\n", ""]
    )

    chunks = text_splitter.split(list_of_docs)
    logger.info("Docs_splitted_successfully")
    return chunks