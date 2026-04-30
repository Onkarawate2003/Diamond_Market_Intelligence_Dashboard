import pandas as pd
import numpy as np
import os

# Load the dataset
# Using absolute paths for safety
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'ecommerce_customer_data.csv')
df = pd.read_csv(file_path)

print("--- Initial Data Info ---")
print(df.info())
print("\n--- Missing Values ---")
print(df.isnull().sum())
print("\n--- Duplicate Records ---")
print(df.duplicated().sum())

# 1. Handle missing values
missing_cols = df.columns[df.isnull().any()].tolist()
for col in missing_cols:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna(df[col].mode()[0])
    else:
        df[col] = df[col].fillna(df[col].median())

# 2. Remove duplicate records
df.drop_duplicates(inplace=True)

# 3. Ensure correct data types
if 'Gender' in df.columns:
    df['Gender'] = df['Gender'].astype('category')
if 'Churn' in df.columns:
    df['Churn'] = df['Churn'].astype('bool')

# 4. Perform basic preprocessing
# Normalize column names (all lowercase)
df.columns = [col.lower() for col in df.columns]

# Save the cleaned data
cleaned_file_path = os.path.join(script_dir, 'cleaned_ecommerce_customer_data.csv')
df.to_csv(cleaned_file_path, index=False)

print("\n--- Data Cleaning Complete ---")
print(f"Cleaned data saved to: {cleaned_file_path}")
print("\n--- Cleaned Data Info ---")
print(df.info())
