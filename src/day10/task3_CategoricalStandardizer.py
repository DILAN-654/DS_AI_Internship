import pandas as pd

df = pd.read_csv("D:/1_1_DS_AI_Internship/data/cleaned/customer_orders.csv")

print("Unique Locations BEFORE normalization:")
print(df["Location"].unique())

df["Location"] = df["Location"].str.strip().str.title()

df = df.drop_duplicates()

print("\nUnique Locations AFTER normalization:")
print(df["Location"].unique())
