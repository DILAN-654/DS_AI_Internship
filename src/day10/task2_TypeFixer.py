import pandas as pd

df = pd.read_csv("D:/1_1_DS_AI_Internship/data/cleaned/customer_orders.csv")

print("Initial data types:")
print(df.dtypes)

# Convert Price to float
df["Price"] = df["Price"].str.replace("$", "", regex=False).astype(float)

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

print("\nUpdated data types:")
print(df.dtypes)
