import numpy as np
import pandas as pd
np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=100)
data = np.append(data, [120, 130, -20])
df = pd.DataFrame({"values": data})
mu = df["values"].mean()
sigma = df["values"].std()
print("Mean (μ):", mu)
print("Standard Deviation (σ):", sigma)
df["z_score"] = (df["values"] - mu) / sigma
print("\nDataset with Z-Scores:")
print(df)
outliers = df[abs(df["z_score"]) > 3]
print("\nOutliers (|Z| > 3):\n")
print(outliers)
print("Total Outliers found:",len(outliers))