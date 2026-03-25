from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.datasets import load_iris

# Load and Scale
data = load_iris()
X = data.data

# 1. Standardization is MANDATORY
X_scaled = StandardScaler().fit_transform(X)

# 2. Fit PCA
pca = PCA()
pca.fit(X_scaled)

print(f"Original shape: {X.shape}")
print(f"Number of components found: {pca.n_components_}")
print("\nPrincipal Components (Eigenvectors):\n", pca.components_)