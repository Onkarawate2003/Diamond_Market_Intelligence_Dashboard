import pandas as pd
df = pd.read_csv('diamonds.csv')
print(df['carat'].describe())
