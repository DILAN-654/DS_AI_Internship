# Creating a Series
import pandas as pd
data=pd.Series([10,None,30,None])
print(data.isnull())
print(data.fillna(0))

names=pd.Series(['Alice','bob','CHARLIE'])
res=names.str.lower()
print(res)
print(res.str.contains('a'))
print(names.str.upper())

s1 = pd.Series([10, 20, 30, 40])
s2 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print("creating Series")
print("s1:\n", s1)
print("\ns2:", s2)

# Accessing elements in a Series
print("Acccesing elements:")
marks = pd.Series([85, 90, 78], index=['Math', 'Physics', 'Chemistry'])
print("\nmarks['Math']:\n", marks['Math'])
print("\nmarks[['Math', 'Chemistry']]:\n", marks[['Math', 'Chemistry']])

# Performing operations on Series
print("Performing operations on series:")
scores = pd.Series([45, 67, 89, 34, 90])
passed = scores[scores > 60]
print("\npassed:\n", passed)

# Handling missing data
print("handling missing data:")
data = pd.Series([10, None, 30, None])
print("\ndata.isnull():\n", data.isnull())
print("\ndata.fillna(0):\n", data.fillna(0))
