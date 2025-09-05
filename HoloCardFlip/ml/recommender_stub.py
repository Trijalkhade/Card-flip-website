# Simple offline recommender prototype using cosine similarity
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# content embeddings (fake)
content_embeddings = np.array([
    [0.1, 0.2, 0.3],
    [0.05, 0.9, 0.1]
])
# user embedding example
user_emb = np.array([0.0, 1.0, 0.0]).reshape(1,-1)

scores = cosine_similarity(user_emb, content_embeddings).flatten()
ranked = scores.argsort()[::-1]
print('recommended content indices:', ranked.tolist())
