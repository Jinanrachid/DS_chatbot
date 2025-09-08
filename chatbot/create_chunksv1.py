from langchain_experimental.text_splitter import SemanticChunker
import os
import sys

from embedd_model import get_bedrock_embedding

# Initialize embeddings
try:
    embeddings = get_bedrock_embedding()
except Exception as e:
    print(f"Failed to get embeddings: {e}", file=sys.stderr)
    sys.exit(1)

def split_text(text, embeddings, threshold_types="percentile"):
    """
    Splits the input text into semantically coherent chunks using SemanticChunker.
    """
    try:
        text_splitter = SemanticChunker(
            embeddings,
            breakpoint_threshold_type=threshold_types
        )
        docs = text_splitter.create_documents([text])
        return docs
    except Exception as e:
        print(f"Error splitting text: {e}", file=sys.stderr)
        return []

def save_chunks(docs, folder_path, file_name, base_filename="chunk"):
    """
    Save each document chunk in `docs` as a separate text file in `folder_path`.
    """
    if not docs:
        print(f"No chunks to save for file '{file_name}'")
        return

    try:
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
        file_name_no_ext = os.path.splitext(file_name)[0]

        for i, doc in enumerate(docs):
            # Clean text by replacing newlines with spaces
            content = doc.page_content.replace("\n", " ").strip()
            file_path = os.path.join(folder_path, f"{file_name_no_ext}_{base_filename}_{i}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"Saved {len(docs)} chunks to {folder_path} for file '{file_name}'")
    except Exception as e:
        print(f"Failed to save chunks for '{file_name}': {e}", file=sys.stderr)

def create_chunks(root_path, folder_path_chunks):
    """
    Traverse root_path, split all text files into chunks, and save them in folder_path_chunks.
    """
    if not os.path.exists(root_path):
        print(f"Root path '{root_path}' does not exist.", file=sys.stderr)
        return

    for folder_name in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder_name)

        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)

                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read().replace("\n", " ").strip()
                        documents = split_text(content, embeddings)
                        save_chunks(documents, folder_path_chunks, file_name, base_filename="chunk")
                    except Exception as e:
                        print(f"Failed to process file '{file_name}': {e}", file=sys.stderr)

if __name__ == "__main__":
    root_path = "C:\\Users\\Jinane Rachid\\Desktop\\internship\\week2\\DS_chatbot\\scraped_data_clean"
    chunks_path = "C:\\Users\\Jinane Rachid\\Desktop\\internship\\week2\\DS_chatbot\\chatbot\\chunks"
    create_chunks(root_path, chunks_path)
