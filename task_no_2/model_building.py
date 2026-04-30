import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# Load featured data
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'featured_ecommerce_customer_data.csv')
df = pd.read_csv(file_path)

# Prepare Features (X) and Target (y)
# Target: 'churn' (Predicting if a customer will leave or stay)
# Predicting 'Churn' is the most relevant classification task for this dataset.
y = df['churn']

# Features: Drop identifiers and non-numeric categorical columns (keep encoded ones)
X = df.drop(columns=['customer_id', 'gender', 'age_group', 'churn'])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("--- Model Building ---")
print(f"Training set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")

# 1. Random Forest Classifier (Robust and high performing)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 2. Logistic Regression (Baseline)
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)

# Evaluation - Random Forest
rf_pred = rf_model.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

print("\n--- Random Forest Performance ---")
print(f"Accuracy: {rf_acc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, rf_pred))

# Save the best model
model_path = os.path.join(script_dir, 'churn_prediction_model.pkl')
joblib.dump(rf_model, model_path)

# Feature Importance
importances = pd.Series(rf_model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\n--- Top Feature Importances ---")
print(importances.head(5))

print(f"\nModel saved to: {model_path}")
