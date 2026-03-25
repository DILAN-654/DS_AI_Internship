import numpy as np

# Define some points in a cluster
points = np.array([[1, 2], [1, 4], [5, 8]])

# Calculate the centroid (mean along axis 0)
centroid = points.mean(axis=0)

print(f"Points:\n{points}")
print(f"\nCalculated Centroid: {centroid}")