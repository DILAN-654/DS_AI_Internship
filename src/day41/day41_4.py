from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import pandas as pd

# Load
iris = load_iris()
X_scaled = StandardScaler().fit_transform(iris.data)

# Reduce to 2 Components
pca_2 = PCA(n_components=2)
X_reduced = pca_2.fit_transform(X_scaled)

print(f"Original shape: {X_scaled.shape}")
print(f"Reduced shape: {X_reduced.shape}")
print("\nFirst 5 rows of reduced data (PC1, PC2):")
print(X_reduced[:5])

# In a real notebook, you would now use:
# plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=iris.target)