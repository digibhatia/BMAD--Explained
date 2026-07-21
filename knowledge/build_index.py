"""
Build the ChromaDB vector store from the knowledge/ folder.

Run this once (and again whenever the source documents change):
    python knowledge/build_index.py
"""

import os
import chromadb

KNOWLEDGE_DIR = os.path.dirname(__file__)
STORE_PATH = os.path.join(os.path.dirname(KNOWLEDGE_DIR), "vector_store", "chroma")


def chunk(text, chunk_size=400):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def build_index():
    client = chromadb.PersistentClient(path=STORE_PATH)
    collection = client.get_or_create_collection("billing_policy")

    doc_id = 0
    for filename in ("billing_policy.txt", "faq.txt"):
        path = os.path.join(KNOWLEDGE_DIR, filename)
        with open(path, "r") as f:
            text = f.read()
        for c in chunk(text):
            collection.add(documents=[c], ids=[f"{filename}_{doc_id}"])
            doc_id += 1

    print(f"Indexed {doc_id} chunks into '{collection.name}' at {STORE_PATH}")


if __name__ == "__main__":
    build_index()
