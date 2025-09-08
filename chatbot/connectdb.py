from langchain_chroma import Chroma
from embedd_model import get_bedrock_embedding
import sys

def settings(collection_name="rag_chunks"):
    """
    Settings for connecting to ChromaDB.
    """
    vectordb = Chroma(
    collection_name=collection_name,
    embedding_function=get_bedrock_embedding(),
    host="63.34.8.16",
    port=8000

    )
    return vectordb

def connect_to_chroma(collection_name ="rag_chunks"):
    """
    Connects to a remote ChromaDB instance via REST with error handling.
    """
    try:
        vectordb = settings()
        # Test connection (heartbeat)
        if vectordb._client.heartbeat():
            print(f"Connected to ChromaDB collection '{collection_name}'")
        else:
            print("Connection established, but heartbeat failed")
        return vectordb

    except Exception as e:
        print(f"Failed to connect to ChromaDB: {e}", file=sys.stderr)
        return None
    return vectordb
