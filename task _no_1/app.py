import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Diamond Explorer Dashboard", layout="wide")

# App Header
st.title("💎 Diamond Explorer Dashboard")
st.markdown("Explore the diamonds dataset with interactive filters and visualizations.")

# Data Loading (Cached for performance)
@st.cache_data
def load_data():
    df = pd.read_csv("diamonds.csv")
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
    st.subheader("Average Price by Cut")
    if not filtered_df.empty:
        # Calculate average price by cut for the column chart
        avg_price_df = filtered_df.groupby('cut')['price'].mean().sort_values(ascending=False).reset_index()
        
        fig = px.bar(
            avg_price_df,
            x="cut",
            y="price",
            color="cut",
            title=f"Average Price by Cut (Filtered: {len(filtered_df)} diamonds)",
            labels={"cut": "Cut Quality", "price": "Average Price ($)"},
            template="plotly_white"
        )
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
