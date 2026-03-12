import json
import pickle
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PAGES_PATH = os.path.join(BASE_DIR, "data", "bis_pages.json")
CHUNKS_PATH = os.path.join(BASE_DIR, "data", "chunks.json")
VECTOR_PATH = os.path.join(BASE_DIR, "data", "embeddings.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "data", "vectorizer.pkl")

print("Loading raw BIS pages...")
with open(PAGES_PATH, "r", encoding="utf-8") as f:
    pages = json.load(f)

print(f"Loaded {len(pages)} pages")

chunks = []
metadata = []

print("Chunking content...")
for page in pages:
    content = page["content"]
    # Simple chunking by splitting into ~300 char chunks (matching existing data)
    for i in range(0, len(content), 350):
        chunk = content[i:i+350].strip()
        if len(chunk) > 50:  # Min length filter
            chunks.append(chunk)
            metadata.append({
                "title": page["title"],
                "source": page["source"]
            })

print(f"Created {len(chunks)} chunks")

# Vectorize
print("Fitting TF-IDF vectorizer...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
embeddings_sparse = vectorizer.fit_transform(chunks)
embeddings = embeddings_sparse.toarray().astype(np.float32)  # Dense for cosine sim

print(f"Embeddings shape: {embeddings.shape}")

# Save data
print("Saving files...")
with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
    json.dump({"chunks": chunks, "metadata": metadata}, f, ensure_ascii=False, indent=2)

with open(VECTOR_PATH, "wb") as f:
    pickle.dump((embeddings, None), f)  # Match pipeline.py load: embeddings, _

with open(VECTORIZER_PATH, "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Data generation complete! Files saved:")
print(f"  - {CHUNKS_PATH}")
print(f"  - {VECTOR_PATH}") 
print(f"  - {VECTORIZER_PATH}")
print(f"Ready for RAG pipeline.")
