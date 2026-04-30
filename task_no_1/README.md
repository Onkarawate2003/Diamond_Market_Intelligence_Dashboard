# Diamond Market Intelligence Dashboard

An interactive Streamlit application for exploring and analyzing diamond market data. This project provides insights into the relationships between diamond physical attributes (like carat weight) and their market prices.

## Project Structure (task_no_1)

All project components are organized within the `task_no_1` directory:

- **`app.py`**: The primary Streamlit dashboard application.
  - Features a robust data loading system with dynamic path handling.
  - Includes interactive sidebar filters for Price Range and Cut Quality.
  - Displays a high-visibility **Carat vs. Price Analysis** bar chart.
- **`diamonds.csv`**: The dataset containing records for ~54,000 diamonds.
- **`README.md`**: Project documentation and instructions.
- **`diamonds_eda.ipynb`**: Jupyter notebook containing the initial Exploratory Data Analysis.
- **`check_carat.py`**: A utility script for data validation and statistics.
- **`correlation_heatmap.png` & `price_distribution.png`**: Static visualizations from the EDA phase.

## Key Features

### Interactive Visualizations
- **Carat vs. Price Analysis**: A grouped bar chart that visualizes the average price distribution across various carat weight increments (rounded to the nearest 0.2).
- **Market Premium List**: A real-time updated table showing the Top 10 most expensive diamonds based on the user's active filters.

### Smart Data Handling
- **Cached Loading**: Uses `@st.cache_data` to ensure the dashboard remains fast and responsive.
- **Cleaned Data**: Automatically handles redundant index columns and missing headers in the source CSV.

## Getting Started

### Prerequisites
Ensure you have Python installed, then install the required dependencies:
```bash
pip install streamlit pandas plotly
```

### Running the App
From the root of the workspace, run the following command:
```bash
streamlit run task_no_1/app.py
```

Alternatively, you can navigate into the folder and run it directly:
```bash
cd task_no_1
streamlit run app.py
```

## Data Source
The dashboard uses the classic `diamonds.csv` dataset, which includes attributes such as carat, cut, color, clarity, depth, table, and price for over 50,000 diamonds.
