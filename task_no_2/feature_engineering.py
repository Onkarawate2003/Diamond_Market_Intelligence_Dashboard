import pandas as pd
import numpy as np
import os

# Load cleaned data
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'cleaned_ecommerce_customer_data.csv')
df = pd.read_csv(file_path)

print("--- Initial Features ---")
print(df.columns.tolist())

# 1. Convert categorical variables into numerical format
# Encoding 'gender' (Male: 1, Female: 0)
df['gender_encoded'] = df['gender'].map({'Male': 1, 'Female': 0})

# 2. Create additional meaningful features
# A. Income per Online Purchase (Efficiency/Value indicator)
df['income_per_purchase'] = df['annual_income'] / (df['online_purchases'] + 1)

# B. Spending Score relative to Annual Income
df['spending_to_income_ratio'] = (df['spending_score'] * 1000) / df['annual_income']

# C. Total Engagement Score
df['engagement_score'] = df['membership_years'] * df['online_purchases']

# D. Discount Sensitivity (Hypothetical: Score influenced by discount usage)
df['discount_sensitivity'] = df['spending_score'] * df['discount_usage']

# E. Age Groups (Categorical binning for easier analysis)
df['age_group'] = pd.cut(df['age'], bins=[0, 25, 40, 60, 100], labels=['Gen Z', 'Millennials', 'Gen X', 'Seniors'])

# Save the featured data
featured_file_path = os.path.join(script_dir, 'featured_ecommerce_customer_data.csv')
df.to_csv(featured_file_path, index=False)

print("\n--- Feature Engineering Complete ---")
print(f"Featured data saved to: {featured_file_path}")
print("\n--- New Features Created ---")
print(df[['gender_encoded', 'income_per_purchase', 'spending_to_income_ratio', 'engagement_score', 'discount_sensitivity', 'age_group']].head())
