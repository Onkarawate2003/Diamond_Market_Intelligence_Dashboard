import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Diamond Explorer Dashboard", layout="wide")

# App Header
st.title("💎 Diamond Explorer Dashboard")
st.markdown("Explore the diamonds dataset with interactive filters and visualizations.")

import os

# Data Loading (Cached for performance)
@st.cache_data
def load_data():
    # Construct path relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "diamonds.csv")
    
    df = pd.read_csv(data_path)
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)
    elif df.columns[0] == '':
        df.drop(columns=[df.columns[0]], inplace=True)
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Price Range Slider
min_price = int(df['price'].min())
max_price = int(df['price'].max())
price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Cut Quality Dropdown
all_cuts = sorted(df['cut'].unique())
selected_cut = st.sidebar.selectbox(
    "Select Cut Quality",
    options=["All"] + list(all_cuts)
)

# --- Apply Filters ---
filtered_df = df[
    (df['price'] >= price_range[0]) & 
    (df['price'] <= price_range[1])
]

if selected_cut != "All":
    filtered_df = filtered_df[filtered_df['cut'] == selected_cut]

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Carat vs. Price Analysis")
    if not filtered_df.empty:
        # Group carats by rounding to nearest 0.2 to create distinct, visible columns
        filtered_df['carat_group'] = (filtered_df['carat'] * 5).round() / 5
        # Calculate average price per group for a clear visualization
        visible_df = filtered_df.groupby('carat_group')['price'].mean().reset_index()
        # Convert to string to ensure discrete bars on the x-axis
        visible_df['carat_group'] = visible_df['carat_group'].astype(str)
        
        fig = px.bar(
            visible_df,
            x="carat_group",
            y="price",
            color="price",
            title="Average Price by Carat Weight (Grouped)",
            labels={"carat_group": "Carat Weight", "price": "Average Price ($)"},
            template="plotly_white",
            color_continuous_scale="Reds"
        )
        # Force the bars to be wider and more visible
        fig.update_layout(bargap=0.2)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data matches the selected filters.")

with col2:
    st.subheader("Top 10 Most Expensive")
    top_10 = filtered_df.sort_values(by='price', ascending=False).head(10)
    if not top_10.empty:
        st.table(top_10[['carat', 'cut', 'color', 'clarity', 'price']])
    else:
        st.info("No diamonds to display.")

# Footer
st.divider()
st.caption("Data source: diamonds.csv")
