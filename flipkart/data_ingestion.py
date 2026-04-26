from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from flipkart.data_converter import DataConverter
from flipkart.config import Config

class DataIngestor:

    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(model=Config.EMBEDDING_MODEL)

        self.persist_directory = "chroma_db"

        self.vstore = Chroma(
            collection_name="flipkart_database",
            embedding_function=self.embedding,
            persist_directory=self.persist_directory
        )

    def ingest(self,load_existing=True):
        
        db_path = Path(self.persist_directory)

        if load_existing and db_path.exists() and any(db_path.iterdir()):
            return self.vstore

        docs = DataConverter("data/flipkart_product_review.csv").convert()
        self.vstore.add_documents(docs)

        return self.vstore


