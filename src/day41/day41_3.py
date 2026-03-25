from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import numpy as np

# Setup
X = load_iris().data
X_scaled = StandardScaler().fit_transform(X)

# Fit PCA
pca = PCA()
pca.fit(X_scaled)

# Ratios
ratios = pca.explained_variance_ratio_
cumulative = np.cumsum(ratios)

print("Variance explained by each component:")
for i, r in enumerate(ratios):
    print(f"PC{i+1}: {r:.4f} ({r*100:.1f}%)")

print("\nCumulative Variance:")
print(cumulative)
print(f"\nFirst 2 components capture {cumulative[1]*100:.1f}% of the data!")
