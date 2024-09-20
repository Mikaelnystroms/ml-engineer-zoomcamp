import pandas as pd

df = pd.read_csv('data/laptops.csv')

print(df.head())

print(df['Screen'].median())
print(df['Screen'].mode())
print(df['Screen'].fillna(df['Screen'].mode()[0]))
print(df['Screen'].median())