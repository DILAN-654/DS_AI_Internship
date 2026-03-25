import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

# Load dataset
data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)

# Calculate Variance for each feature
variances = df.var()

print("Feature Variances:")
print(variances)
print("\nFeature with highest variance:", variances.idxmax())
print("Feature with lowest variance:", variances.idxmin())