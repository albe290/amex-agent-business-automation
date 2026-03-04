import os
import json
import numpy as np
from openai import OpenAI
from typing import List


class PolicyRetriever:
    def __init__(self):
        self.client = OpenAI()
        self.vector_store_path = os.path.join(
            os.path.dirname(__file__), "vector_store.json"
        )
        self.documents = self._load_vector_store()

    def _load_vector_store(self) -> List[dict]:
        """Loads the pre-computed embeddings from the local JSON store."""
        if not os.path.exists(self.vector_store_path):
            print(
                f"[Warning] Vector store not found at {self.vector_store_path}. RAG will be empty."
            )
            return []

        with open(self.vector_store_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculates cosine similarity between two vectors."""
        a_np = np.array(a)
        b_np = np.array(b)
        return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))

    def search(self, query: str, top_k: int = 1) -> List[str]:
        """
        Embeds the incoming query and performs a cosine similarity search against the DB.
        Returns the top_k matching text chunks.
        """
        if not self.documents:
            return ["No policies retrieved (vector store empty)."]

        try:
            # 1. Embed the search query
            response = self.client.embeddings.create(
                input=query, model="text-embedding-3-small"
            )
            query_embedding = response.data[0].embedding

            # 2. Score all documents
            scored_docs = []
            for doc in self.documents:
                similarity = self._cosine_similarity(query_embedding, doc["embedding"])
                scored_docs.append(
                    {"score": similarity, "text": doc["text"], "source": doc["source"]}
                )

            # 3. Sort by highest similarity
            scored_docs.sort(key=lambda x: x["score"], reverse=True)

            # 4. Return the formatting top K
            results = []
            for i, doc in enumerate(scored_docs[:top_k]):
                results.append(
                    f"--- SOURCE: {doc['source']} (Relevance: {doc['score']:.2f}) ---\n{doc['text']}"
                )

            return results

        except Exception as e:
            print(f"[Error] Retrieval failed: {str(e)}")
            return ["Policy retrieval failed due to an internal error."]
