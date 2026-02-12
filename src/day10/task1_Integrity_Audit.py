import pandas as pd

df = pd.read_csv("D:/1_1_DS_AI_Internship/data/customer_orders.csv")

print("Shape before cleaning:", df.shape)

print("\nMissing values report:")
print(df.isna().sum())

numeric_cols = df.select_dtypes(include="number").columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

df_cleaned = df.drop_duplicates()

print("\nShape after cleaning:", df_cleaned.shape)
df_cleaned.to_csv("D:/1_1_DS_AI_Internship/data/cleaned/customer_orders.csv",index=False)