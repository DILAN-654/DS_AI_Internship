from sklearn.cluster import KMeans
import numpy as np

# Synthetic data
X = np.random.rand(100, 2)

inertia = []
K_range = range(1, 11)

for k in K_range:
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(X)
    inertia.append(model.inertia_)

print("K values tested: ", list(K_range))
print("Inertia values: ", [round(i, 2) for i in inertia])
print("\nLook for the 'elbow' where the drop in inertia slows down.")