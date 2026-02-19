import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
skewed_data = np.random.exponential(scale=50000, size=10000)

sample_means = []
for i in range(1000):
    sample = np.random.choice(skewed_data, size=30, replace=True)
    sample_means.append(np.mean(sample))

sample_means = np.array(sample_means)

plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
sns.histplot(skewed_data, kde=True, bins=50)
plt.title("Original Skewed Data (Exponential Distribution)")

plt.subplot(1, 2, 2)
sns.histplot(sample_means, kde=True, bins=40)
plt.title("Distribution of Sample Means (Looks Normal!)")

plt.tight_layout()
plt.show()
print("Mean of Sample Means:", sample_means.mean())
print("Standard Deviation of Sample Means:", sample_means.std())