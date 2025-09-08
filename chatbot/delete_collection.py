from connectdb import connect_to_chroma

def delete_collection(collection_name="rag_chunks"):
    try:
        vectordb = connect_to_chroma()
        vectordb.delete_collection()
        print(f"Collection '{collection_name}' and all embeddings have been deleted.")
    except Exception as e:
        print(f"Failed to delete collection '{collection_name}': {e}", file=sys.stderr)

if __name__ == "__main__":
    delete_collection("rag_chunks")