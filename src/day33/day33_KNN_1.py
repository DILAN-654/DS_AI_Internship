import numpy as np

point1 = np.array([2, 3])
point2 = np.array([5, 7])

# Euclidean Distance
euclidean = np.linalg.norm(point1 - point2)

# Manhattan Distance
manhattan = np.sum(np.abs(point1 - point2))

print(f"Point 1: {point1}")
print(f"Point 2: {point2}")
print(f"Euclidean: {euclidean:.4f}")
print(f"Manhattan: {manhattan}")