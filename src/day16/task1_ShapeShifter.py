import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
np.random.seed(42)
heights = np.random.normal(loc=170, scale=10, size=5000)
incomes = np.random.exponential(scale=50000, size=5000)
scores = 100 - np.random.exponential(scale=10, size=5000)
scores = np.clip(scores, 0, 100)
df = pd.DataFrame({
    "Human Heights (Normal)": heights,
    "Household Incomes (Right-Skewed)": incomes,
    "Easy Exam Scores (Left-Skewed)": scores
})
plt.figure(figsize=(18, 5))
for i, col in enumerate(df.columns):
    plt.subplot(1, 3, i+1)
    sns.histplot(df[col], kde=True, bins=40)
    mean_val = df[col].mean()
    median_val = df[col].median()
    plt.axvline(mean_val, color="red", linestyle="--", label=f"Mean: {mean_val:.2f}")
    plt.axvline(median_val, color="blue", linestyle="-", label=f"Median: {median_val:.2f}")
    plt.title(col)
    plt.legend()
plt.tight_layout()
plt.show()
print("Mean vs Median Comparison:\n")
tolerance = 0.5 
for col in df.columns:
    mean_val = df[col].mean()
    median_val = df[col].median()
    print(col)
    print(f"Mean   = {mean_val:.2f}")
    print(f"Median = {median_val:.2f}")
    if abs(mean_val - median_val) <= tolerance:
        print("Normal / Symmetric (Mean ≈ Median)\n")
    elif mean_val > median_val:
        print("Right-Skewed (Mean > Median)\n")
    else:
        print("Left-Skewed (Mean < Median)\n")
        
        
        
        
        
        
        
        
        
        
        