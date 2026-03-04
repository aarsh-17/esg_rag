import numpy as np
from backend.embeddings import get_embeddings

emb = get_embeddings()

vec = emb.embed_query("We are also working to reduce the emissions intensity of our LNG projects.")
print("Query vector norm:", np.linalg.norm(vec))