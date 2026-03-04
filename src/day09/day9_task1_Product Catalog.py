import pandas as pd

products = pd.Series([700, 150, 300], index=['Laptop', 'Mouse', 'Keyboard'])
laptop_price = products['Laptop']
first_two_products = products[:2]

print("Product Prices:")
print(products)
print("\nPrice of Laptop:")
print(laptop_price)
print("\nFirst Two Products (Positional Slicing):")
print(first_two_products)
