import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = {
    "Price": [100000, 150000, 200000, 250000, 300000, 
              120000, 180000, 500000],
    "City": ["Bangalore", "Mysore", "Bangalore", "Delhi", 
             "Delhi", "Mysore", "Bangalore", "Delhi"]
}

df = pd.DataFrame(data)

sns.histplot(df["Price"], kde=True)
plt.title("Distribution of Housing Prices")
plt.xlabel("Price")
plt.show()

skewness = df["Price"].skew()
kurtosis = df["Price"].kurt()

print("Skewness:", skewness)
print("Kurtosis:", kurtosis)

sns.countplot(x="City", data=df)
plt.title("City Frequency")
plt.show()
