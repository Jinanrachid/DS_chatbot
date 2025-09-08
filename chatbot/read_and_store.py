from langchain.docstore.document import Document
import os
import sys
from connectdb import connect_to_chroma

CHUNKS_DIR = "chunks"

def load_documents(chunks_dir=CHUNKS_DIR):
    """
    Load all text files from the chunks directory into LangChain Documents.
    """
    docs = []
    if not os.path.exists(chunks_dir):
        print(f"Chunks directory '{chunks_dir}' does not exist.", file=sys.stderr)
        return docs

    files = os.listdir(chunks_dir)
    if not files:
        print(f"No files found in '{chunks_dir}'")
        return docs

    for filename in files:
        file_path = os.path.join(chunks_dir, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                docs.append(Document(page_content=text, metadata={"source": filename}))
        except Exception as e:
            print(f"Failed to read '{filename}': {e}", file=sys.stderr)

    return docs

if __name__ == "__main__":
    # Load documents
    docs = load_documents()
    if not docs:
        print("No documents to add. Exiting.")
        sys.exit(1)

    # Connect to Chroma
    vectordb = connect_to_chroma()
    if vectordb is None:
        print("Could not connect to ChromaDB. Exiting.")
        sys.exit(1)

    # Add documents
    try:
        vectordb.add_documents(docs)
        print(f"Successfully added {len(docs)} documents to ChromaDB")
    except Exception as e:
        print(f"Failed to add documents: {e}", file=sys.stderr)
        sys.exit(1)
