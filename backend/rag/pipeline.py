import json
import pickle
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CHUNKS_PATH = os.path.join(BASE_DIR, "data", "chunks.json")
VECTOR_PATH = os.path.join(BASE_DIR, "data", "embeddings.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "data", "vectorizer.pkl")

with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

chunks = data["chunks"]
metadata = data["metadata"]

with open(VECTOR_PATH, "rb") as f:
    embeddings, _ = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)


def cosine_similarity_numpy(query_vec, embeddings):
    dots = np.dot(query_vec, embeddings.T).flatten()
    query_norm = np.linalg.norm(query_vec)
    doc_norms = np.linalg.norm(embeddings, axis=1)
    similarities = dots / (query_norm * doc_norms + 1e-8)  # avoid div0
    return similarities


def search(query, top_k=5):
    print(f'Search debug: query="{query}", vectorizer shape={vectorizer.shape if hasattr(vectorizer, "shape") else "no shape"}, embeddings shape={embeddings.shape}')
    query_vector = vectorizer.transform([query]).toarray()
    similarities = cosine_similarity_numpy(query_vector, embeddings)
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "content": chunks[idx],
            "title": metadata[idx]["title"],
            "source": metadata[idx]["source"],
            "score": float(similarities[idx])
        })
    print(f'Returning {len(results)} results, top score: {results[0]["score"] if results else "no results"}')
    return results

