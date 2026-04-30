import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import numpy as np

# Set page config
st.set_page_config(page_title="E-commerce Customer Insights", layout="wide")

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Load data and model
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'featured_ecommerce_customer_data.csv')
    return pd.read_csv(file_path)

@st.cache_resource
def load_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'churn_prediction_model.pkl')
    return joblib.load(model_path)

df = load_data()
model = load_model()

# Header
st.title("🛒 E-commerce Customer Intelligence Dashboard")
st.markdown("Analyze customer behavior, spending patterns, and predict churn risk.")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Market Overview", "Customer Segmentation", "Churn Prediction"])

st.sidebar.divider()
st.sidebar.subheader("Global Filters")
gender_filter = st.sidebar.multiselect("Gender", options=df['gender'].unique(), default=df['gender'].unique())
age_filter = st.sidebar.slider("Age Range", int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))

# Filter data
filtered_df = df[
    (df['gender'].isin(gender_filter)) & 
    (df['age'] >= age_filter[0]) & 
    (df['age'] <= age_filter[1])
]

if page == "Market Overview":
    st.header("📈 Market Overview")
    
    # Key Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Customers", len(filtered_df))
    m2.metric("Avg. Annual Income", f"${filtered_df['annual_income'].mean():,.0f}")
    m3.metric("Avg. Spending Score", f"{filtered_df['spending_score'].mean():.1f}")
    m4.metric("Churn Rate", f"{(filtered_df['churn'].mean() * 100):.1f}%")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Demographic Distribution")
        fig_age = px.histogram(filtered_df, x="age", color="gender", nbins=20, 
                               title="Age Distribution by Gender",
                               color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col2:
        st.subheader("Spending vs Income")
        fig_scatter = px.scatter(filtered_df, x="annual_income", y="spending_score", 
                                 color="gender", size="online_purchases",
                                 title="Income vs Spending Score (Bubble size = Purchases)",
                                 template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)

elif page == "Customer Segmentation":
    st.header("👥 Customer Segmentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Engagement by Membership Tier")
        # Using rounded membership years for better grouping
        filtered_df['mem_rounded'] = filtered_df['membership_years'].round()
        fig_eng = px.bar(filtered_df.groupby('mem_rounded')['online_purchases'].mean().reset_index(),
                         x="mem_rounded", y="online_purchases", 
                         title="Avg Purchases by Membership Years",
                         labels={"mem_rounded": "Years", "online_purchases": "Avg Purchases"},
                         color_discrete_sequence=['#ff7f0e'])
        st.plotly_chart(fig_eng, use_container_width=True)
        
    with col2:
        st.subheader("Discount Sensitivity")
        fig_box = px.box(filtered_df, x="gender", y="discount_usage", color="gender",
                         title="Discount Usage Distribution",
                         points="all")
        st.plotly_chart(fig_box, use_container_width=True)
        
    st.subheader("High Value Customers (Top 10)")
    top_customers = filtered_df.sort_values('engagement_score', ascending=False).head(10)
    st.dataframe(top_customers[['customer_id', 'age', 'gender', 'annual_income', 'engagement_score', 'churn']], use_container_width=True)

elif page == "Churn Prediction":
    st.header("🔮 Churn Prediction AI")
    st.markdown("Input customer details to estimate their probability of leaving.")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        in_age = st.number_input("Age", 18, 100, 35)
        in_gender = st.selectbox("Gender", ["Male", "Female"])
        in_income = st.number_input("Annual Income ($)", 10000, 200000, 50000)
    
    with c2:
        in_score = st.slider("Spending Score (1-100)", 1, 100, 50)
        in_years = st.slider("Membership Years", 0.0, 10.0, 2.0)
        in_purchases = st.number_input("Online Purchases", 0, 500, 50)
        
    with c3:
        in_discount = st.slider("Discount Usage (0.0 - 1.0)", 0.0, 1.0, 0.2)
    
    # Preprocess inputs for model
    gen_encoded = 1 if in_gender == "Male" else 0
    inc_per_pur = in_income / (in_purchases + 1)
    sp_to_inc = (in_score * 1000) / in_income
    eng_score = in_years * in_purchases
    dis_sens = in_score * in_discount
    
    # Feature order must match X_train: 
    # ['age', 'annual_income', 'spending_score', 'membership_years', 'online_purchases', 'discount_usage', 
    #  'gender_encoded', 'income_per_purchase', 'spending_to_income_ratio', 'engagement_score', 'discount_sensitivity']
    input_data = np.array([[in_age, in_income, in_score, in_years, in_purchases, in_discount, 
                            gen_encoded, inc_per_pur, sp_to_inc, eng_score, dis_sens]])
    
    if st.button("Predict Churn Risk", type="primary"):
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
        
        st.divider()
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            if prediction:
                st.error("### ⚠️ HIGH RISK: LIKELY TO CHURN")
            else:
                st.success("### ✅ LOW RISK: LIKELY TO STAY")
            st.metric("Churn Probability", f"{probability*100:.1f}%")
            
        with res_col2:
            # Gauge chart for probability
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = probability * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Churn Probability %"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkred" if prediction else "darkgreen"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgreen"},
                        {'range': [50, 80], 'color': "orange"},
                        {'range': [80, 100], 'color': "red"}],
                }
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)

# Footer
st.divider()
st.caption("Developed by Antigravity AI | E-commerce Intelligence Solution")
