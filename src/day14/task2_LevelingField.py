import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler

data = {
    'Age': [22, 25, 30, 35, 40, 45, 50],
    'Salary': [20000, 25000, 30000, 35000, 40000, 45000, 50000]}
df = pd.DataFrame(data)
print("Original Data:")
print(df)

std_scaler = StandardScaler()
df_standardized = pd.DataFrame(
    std_scaler.fit_transform(df),
    columns=df.columns)
print("\nStandardized Data:")
print(df_standardized)

minmax_scaler = MinMaxScaler()
df_normalized = pd.DataFrame(
    minmax_scaler.fit_transform(df),
    columns=df.columns)
print("\nNormalized Data:")
print(df_normalized)

plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.hist(df['Salary'], bins=5)
plt.title("Original Salary")

plt.subplot(1,3,2)
plt.hist(df_standardized['Salary'], bins=5)
plt.title("Standardized Salary")

plt.subplot(1,3,3)
plt.hist(df_normalized['Salary'], bins=5)
plt.title("Normalized Salary")

plt.show()
