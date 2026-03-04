import os
import json
import glob
from openai import OpenAI

# Initialize OpenAI Client
client = OpenAI()

# Configuration
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store.json")


def read_markdown_files():
    """Reads all Markdown files in the knowledge base directory."""
    documents = []
    # Search all subdirectories for .md
    pattern = os.path.join(KNOWLEDGE_BASE_DIR, "**", "*.md")
    for filepath in glob.glob(pattern, recursive=True):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            # For this simple prototype, we treat each file as one chunk.
            # In a production system, you would split by paragraphs/headers.
            filename = os.path.basename(filepath)
            documents.append({"source": filename, "text": content})
    return documents


def get_embedding(text: str) -> list[float]:
    """Calls OpenAI to generate a vector embedding for the text."""
    try:
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        return response.data[0].embedding
    except Exception as e:
        print(f"[Error] Failed to embed text: {str(e)}")
        return []


def run_ingestion():
    print("Starting Policy Ingestion Pipeline...")
    documents = read_markdown_files()
    print(f"Discovered {len(documents)} policy files.")

    vector_store = []

    for doc in documents:
        print(f"Embedding file: {doc['source']}...")
        vector = get_embedding(doc["text"])

        if vector:
            vector_store.append(
                {"source": doc["source"], "text": doc["text"], "embedding": vector}
            )

    # Save the vector store flat file
    with open(VECTOR_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(vector_store, f)

    print(f"Successfully generated vector store at {VECTOR_STORE_PATH}")


if __name__ == "__main__":
    # Ensure OPENAI_API_KEY is available in the environment
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OPENAI_API_KEY first.")
    else:
        run_ingestion()
