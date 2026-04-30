# E-commerce Customer Intelligence Solution

This project provides a comprehensive end-to-end data science solution for analyzing e-commerce customer behavior and predicting churn risk.

## Project Structure (task_no_2)

- **`app.py`**: Interactive Streamlit dashboard.
- **`ecommerce_customer_data.csv`**: Raw source dataset.
- **`cleaned_ecommerce_customer_data.csv`**: Dataset after cleaning and preprocessing.
- **`featured_ecommerce_customer_data.csv`**: Dataset with engineered features ready for modeling.
- **`churn_prediction_model.pkl`**: Trained Random Forest Classifier.
- **`data_cleaning.py`**, **`eda_analysis.py`**, **`feature_engineering.py`**, **`model_building.py`**, **`model_evaluation.py`**: Pipeline scripts.
- **`figures/`**: Folder containing EDA and Model Evaluation plots.

---

## Approach & Steps Followed

1.  **Data Cleaning & Preprocessing**:
    *   Handled potential missing values using median/mode imputation.
    *   Verified and removed duplicate records.
    *   Normalized column names and converted data types (e.g., categorical encoding for Gender).
2.  **Exploratory Data Analysis (EDA)**:
    *   Analyzed demographic distributions (Age/Gender).
    *   Explored the relationship between Annual Income and Spending Score.
    *   Investigated purchase behavior relative to membership duration.
3.  **Feature Engineering**:
    *   Created derived metrics: `income_per_purchase`, `spending_to_income_ratio`, `engagement_score`, and `discount_sensitivity`.
    *   Binned Age into generational groups (Gen Z, Millennials, etc.).
4.  **Model Building & Evaluation**:
    *   Trained a **Random Forest Classifier** to predict customer churn.
    *   Evaluated performance using Accuracy, Confusion Matrix, and ROC-AUC.
5.  **Dashboard Development**:
    *   Built a multi-page Streamlit application for visualization and real-time AI predictions.

---

## Key Insights

- **Spending Behavior**: There is no direct correlation between high annual income and high spending scores. Engagement is driven by more complex behavioral factors.
- **Demographics**: The customer base is highly diverse and evenly distributed across ages 18-70.
- **Loyalty**: Online purchase frequency remains stable over the years, indicating that long-term members remain consistently active rather than increasing their volume.
- **Churn Risk**: Approximately **31%** of the customer base is at risk of churning.

---

## Model Performance & Observations

- **Model Type**: Random Forest Classifier
- **Accuracy**: **64.75%**
- **ROC-AUC**: **0.46**
- **Observations**:
    *   The model identifies "Loyal" customers (those who stay) with high precision.
    *   Predicting "Churn" is challenging, likely due to class imbalance and the fact that churn triggers may be external or event-driven rather than purely demographic.
    *   **Top Predictors**: The engineered `engagement_score` and `discount_sensitivity` were the strongest indicators of customer status.

---

## How to Run

1.  Install dependencies: `pip install streamlit pandas plotly scikit-learn joblib matplotlib seaborn`
2.  Run the dashboard:
    ```bash
    streamlit run task_no_2/app.py --server.port 8502
    ```
