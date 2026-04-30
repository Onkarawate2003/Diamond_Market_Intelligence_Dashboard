import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, roc_curve, auc

# Load featured data
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'featured_ecommerce_customer_data.csv')
df = pd.read_csv(file_path)

# Prepare Features (X) and Target (y)
y = df['churn']
X = df.drop(columns=['customer_id', 'gender', 'age_group', 'churn'])

# Split the data (same split as training)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load the model
model_path = os.path.join(script_dir, 'churn_prediction_model.pkl')
model = joblib.load(model_path)

# Predictions
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# 1. Accuracy
acc = accuracy_score(y_test, y_pred)

# 2. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# 3. Visualization directory
figs_dir = os.path.join(script_dir, 'figures')
if not os.path.exists(figs_dir):
    os.makedirs(figs_dir)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Stay', 'Churn'], yticklabels=['Stay', 'Churn'])
plt.title(f'Confusion Matrix (Accuracy: {acc:.2f})')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig(os.path.join(figs_dir, 'confusion_matrix.png'))
plt.close()

# 4. ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc="lower right")
plt.savefig(os.path.join(figs_dir, 'roc_curve.png'))
plt.close()

# 5. Metrics Report
report = classification_report(y_test, y_pred)

print("--- Model Evaluation ---")
print(f"Accuracy: {acc:.4f}")
print(f"ROC-AUC: {roc_auc:.4f}")
print("\nClassification Report:")
print(report)
print(f"\nEvaluation plots saved to: {figs_dir}")
