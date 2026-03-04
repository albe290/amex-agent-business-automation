import os
import json
import glob
import datetime
from openai import OpenAI

# Initialize OpenAI Client
client = OpenAI()

# Configuration
KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store.json")

BANNER = """
============================================================
      SECURE FINANCIAL AI AGENT - POLICY INGESTION
============================================================
Status: [ACTIVE]
Department: Cybersecurity & Compliance
"""


def read_markdown_files():
    """Reads all Markdown files and extracts a clean summary."""
    documents = []
    pattern = os.path.join(KNOWLEDGE_BASE_DIR, "**", "*.md")
    for filepath in glob.glob(pattern, recursive=True):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            filename = os.path.basename(filepath)

            # Extract first line as summary/title
            summary = content.split("\n")[0].replace("# ", "").strip()

            documents.append({"source": filename, "text": content, "summary": summary})
    return documents


def get_embedding(text: str) -> list[float]:
    """Calls OpenAI to generate a vector embedding."""
    try:
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        return response.data[0].embedding
    except Exception as e:
        print(f" [!] Error: {str(e)}")
        return []


def run_ingestion():
    print(BANNER)
    documents = read_markdown_files()
    print(f"[*] Discovered {len(documents)} high-value policy documents.")

    # Create a wrapper object for the vector store to look "Enterprise"
    enterprise_store = {
        "project": "Secure Financial AI Agent",
        "last_updated": datetime.datetime.now().isoformat(),
        "total_chunks": len(documents),
        "department": "Global Risk & Safety",
        "data": [],
    }

    for i, doc in enumerate(documents):
        print(f"[#] Processing Chunk {i+1}: {doc['source']}...")
        vector = get_embedding(doc["text"])

        if vector:
            enterprise_store["data"].append(
                {
                    "id": f"CHUNK-{1000 + i}",
                    "source": doc["source"],
                    "summary": doc["summary"],
                    "text_preview": doc["text"][:100].replace("\n", " ") + "...",
                    "metadata": {
                        "author": "Compliance Safety Team",
                        "compliance_level": "High",
                    },
                    "embedding": vector,
                    "text": doc["text"],
                }
            )

    # Save the vector store with professional formatting
    with open(VECTOR_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(enterprise_store, f, indent=4)

    print(f"\n[SUCCESS] Vector Store created for presentation: {VECTOR_STORE_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("[X] ERROR: OPENAI_API_KEY environment variable not found.")
    else:
        run_ingestion()
