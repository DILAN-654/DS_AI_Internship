import pandas as pd
from sklearn.preprocessing import LabelEncoder
# Sample dataset
data = {
    'Transmission': ['Automatic', 'Manual', 'Automatic', 'Manual'],
    'Color': ['Red', 'Blue', 'Green', 'Red']
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

le = LabelEncoder()
df['Transmission'] = le.fit_transform(df['Transmission'])

df = pd.get_dummies(df, columns=['Color'], drop_first=True)

print("\nEncoded Data:")
print(df)
