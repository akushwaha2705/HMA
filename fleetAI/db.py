from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from secure import KEY


def connect_to_quadrant(collection):
    """
    Connect to the QDrant instance and return the QDrant object.

    :param embedding_function: The embedding function for processing the text. 
                               Default is None, which means no embedding function will be used.
    :param connection_args: Dictionary containing connection details like host and port.
    :return: QDrant object
    """
    embedding_function = OpenAIEmbeddings(openai_api_key=KEY)

    client = QdrantClient(url="http://127.0.0.1:6333")
    return Qdrant(client, 
                  collection, 
                  embedding_function)
