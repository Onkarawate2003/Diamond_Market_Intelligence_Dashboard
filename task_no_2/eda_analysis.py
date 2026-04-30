import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set(style="whitegrid")

# Load cleaned data
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'cleaned_ecommerce_customer_data.csv')
df = pd.read_csv(file_path)

# Create figures directory
figs_dir = os.path.join(script_dir, 'figures')
if not os.path.exists(figs_dir):
    os.makedirs(figs_dir)

# 1. Distribution of customers by age and gender
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='age', hue='gender', multiple='stack', bins=20, palette='viridis')
plt.title('Distribution of Customers by Age and Gender')
plt.xlabel('Age')
plt.ylabel('Count')
plt.savefig(os.path.join(figs_dir, 'age_gender_distribution.png'))
plt.close()

# 2. Relationship between income and spending score
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='annual_income', y='spending_score', hue='gender', alpha=0.6, palette='magma')
plt.title('Relationship between Annual Income and Spending Score')
plt.xlabel('Annual Income ($)')
plt.ylabel('Spending Score (1-100)')
plt.savefig(os.path.join(figs_dir, 'income_vs_spending.png'))
plt.close()

# 3. Purchase behavior analysis
# Let's look at average online purchases by gender and membership years
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='membership_years', y='online_purchases', hue='gender', ci=None, palette='rocket')
plt.title('Average Online Purchases by Membership Years and Gender')
plt.xlabel('Membership Years')
plt.ylabel('Average Online Purchases')
plt.savefig(os.path.join(figs_dir, 'purchase_behavior.png'))
plt.close()

# Bonus: Churn distribution
plt.figure(figsize=(8, 6))
df['churn'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#66b3ff','#ff9999'])
plt.title('Churn Rate Distribution')
plt.ylabel('')
plt.savefig(os.path.join(figs_dir, 'churn_rate.png'))
plt.close()

print(f"EDA complete. Visualizations saved to: {figs_dir}")
