import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Example dataset
data = {
    "SquareFootage": [800, 1000, 1200, 1500, 1800, 2000, 2200, 2500],
    "Price": [200000, 250000, 270000, 320000, 350000, 400000, 420000, 500000],
    "City": ["Bangalore", "Mysore", "Bangalore", "Delhi", "Delhi", "Mysore", "Bangalore", "Delhi"]
}

df = pd.DataFrame(data)

# Scatter plot
sns.scatterplot(x="SquareFootage", y="Price", data=df)
plt.title("Square Footage vs Price")
plt.show()

sns.boxplot(x="City", y="Price", data=df)
plt.title("City vs Price Distribution")
plt.show()
