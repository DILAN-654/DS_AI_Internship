from sklearn.cluster import KMeans
import numpy as np

# 1. Generate data
X = np.random.randn(50, 2) + [2, 2]
X2 = np.random.randn(50, 2) + [-2, -2]
X_final = np.vstack([X, X2])

# 2. Fit K-Means
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_final)

# 3. Get Centroids
centers = kmeans.cluster_centers_

print(f"Total points: {len(X_final)}")
print(f"Centroid 1: {centers[0]}")
print(f"Centroid 2: {centers[1]}")
print("\nIn a real notebook, you would now use plt.scatter(X[:,0], X[:,1], c=labels)")