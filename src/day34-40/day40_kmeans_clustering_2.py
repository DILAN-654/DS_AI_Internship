from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

# Synthetic data: 2 features
X = np.array([[1, 2], [1, 4], [1, 0], [10, 2], [10, 4], [10, 0]])

# 1. Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. Fit K-Means with K=2
kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)

print(f"Original Data:\n{X}")
print(f"\nCluster Labels: {labels}")
print(f"\nCentroids:\n{kmeans.cluster_centers_}")