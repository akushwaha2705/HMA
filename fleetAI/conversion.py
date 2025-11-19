from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from fleetAI.db import connect_to_quadrant
from secure import KEY


class DocumentProcessor:

    def __init__(self, collection, document):
        self.collection = collection
        self.document = f"knowledge-base/{document}"
        self.vector_db = self.connect_to_database()
        self.docs = self.load_documents()
        self.all_splits = self.split_text()
        self.store_embeddings()

    def connect_to_database(self):
        return connect_to_quadrant(self.collection)

    def load_documents(self):
        loader = UnstructuredPDFLoader(
            self.document, mode="elements", strategy="fast",
        )
        return loader.load()

    def split_text(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=40)
        return text_splitter.split_documents(self.docs)

    def store_embeddings(self):
        embeddings = OpenAIEmbeddings(openai_api_key=KEY)
        self.vector_db.from_documents(self.all_splits, embeddings, url="http://qdrant:6333", collection_name=self.collection)
