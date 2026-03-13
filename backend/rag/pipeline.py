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
    # Dynamic query expansion instead of fixed BIS prefix
    expansions = {
        'certification': 'ISI mark product certification licence process',
        'hallmark': 'gold silver jewellery hallmarking HUID licence',
        'standard': 'Indian Standard IS development formulation',
        'laboratory': 'testing calibration BIS lab recognition',
    }
    expanded_query = query
    for key, expansion in expansions.items():
        if key in query.lower():
            expanded_query = f"{query} {expansion}"
            break
    else:
        expanded_query = f"{query} BIS standards"
    
    print(f'Search debug: query="{query}" -> expanded="{expanded_query}"')
    query_vector = vectorizer.transform([expanded_query]).toarray()
    similarities = cosine_similarity_numpy(query_vector, embeddings)
    
    # Get top 2*top_k for MMR diversity
    candidate_indices = np.argsort(similarities)[::-1][:top_k*2]
    
    # Simple MMR (Maximal Marginal Relevance) for diversity
    selected_indices = []
    lambda_diversity = 0.5
    
    for cand_idx in candidate_indices:
        if len(selected_indices) >= top_k:
            break
        if not selected_indices:
            selected_indices.append(cand_idx)
            continue
            
        # Diversity score - fix scalar indexing
        diversity_score = 0
        for sel_idx in selected_indices:
            emb1 = embeddings[[cand_idx]]
            emb2 = embeddings[[sel_idx]]
            div_sim = cosine_similarity_numpy(emb1, emb2)[0]
            diversity_score += div_sim
        avg_diversity = diversity_score / len(selected_indices)
        
        marginal_relevance = similarities[cand_idx] * (1 - lambda_diversity) + lambda_diversity * (1 - avg_diversity)
        
        if marginal_relevance > similarities[selected_indices[-1]]:
            selected_indices.append(cand_idx)
    
    top_indices = selected_indices

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

