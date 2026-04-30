# Diamond Analysis & Dashboard Project

This project provides a comprehensive analysis of the classic Diamonds dataset, including data cleaning, exploratory data analysis (EDA), and an interactive web dashboard for real-time exploration.

## Project Structure

- **`diamonds.csv`**: The primary dataset containing attributes of 53,940 diamonds (carat, cut, color, clarity, price, and dimensions).
- **`diamonds_eda.ipynb`**: A Jupyter Notebook containing the full EDA process:
  - Data cleaning and outlier handling.
  - Correlation analysis (identifying Carat and Dimensions as top price drivers).
  - Visualization of price distributions and feature relationships.
- **`app.py`**: A Streamlit-based interactive dashboard that allows users to:
  - Filter diamonds by price range and cut quality.
  - Visualize the relationship between Carat and Price using interactive Plotly charts.
  - View a dynamic table of the top 10 most expensive diamonds based on active filters.
- **`correlation_heatmap.png`**: A visualization showing the correlation between various diamond features.
- **`price_distribution.png`**: A chart showing the frequency distribution of diamond prices in the dataset.

## Features

### EDA Highlights
- **Outlier Handling**: Removed physically impossible diamonds (those with 0mm dimensions).
- **Ordinal Encoding**: Converted categorical qualities (Cut, Color, Clarity) into numerical values to quantify their impact on price.
- **Key Findings**: Confirmed that Carat weight is the strongest predictor of price (~0.92 correlation).

### Interactive Dashboard
- **Sidebar Controls**: Real-time filtering for deep dives into specific market segments.
- **Interactive Plotting**: Plotly-powered scatter plots with hover details.
- **Top 10 List**: Instant identification of premium diamonds within filtered criteria.

## Getting Started

### Prerequisites
Ensure you have the following Python libraries installed:
```bash
pip install streamlit pandas plotly seaborn matplotlib nbconvert ipykernel
```

### Running the Dashboard
To launch the interactive dashboard, navigate to this folder and run:
```bash
streamlit run app.py
```

### Viewing the EDA
You can view the pre-rendered analysis in `diamonds_eda.ipynb` using any Jupyter-compatible viewer or by opening it in VS Code.
