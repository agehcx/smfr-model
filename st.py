import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the web page configuration
st.set_page_config(page_title="Crypto Performance Metrics Dashboard", layout="wide")

st.title("Crypto Performance Metrics Dashboard")
st.write("Upload a CSV file containing the crypto backtest results.")

# File uploader for CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df["period"] = df["period"].astype(str)
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.subheader("Data Preview")
    st.dataframe(df)

    # Sidebar filtering options
    st.sidebar.header("Filter Options")
    crypto_options = df["crypto"].unique().tolist()
    selected_cryptos = st.sidebar.multiselect("Select Cryptos", options=crypto_options, default=crypto_options)
    period_options = df["period"].unique().tolist()
    selected_periods = st.sidebar.multiselect("Select Periods", options=period_options, default=period_options)

    filtered_df = df[(df["crypto"].isin(selected_cryptos)) & (df["period"].isin(selected_periods))]

    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    # Interactive graphs using Plotly Express for each metric
    metrics = ["total_return", "sharpe_ratio", "max_drawdown"]
    titles = ["Total Return", "Sharpe Ratio", "Max Drawdown"]

    for metric, title in zip(metrics, titles):
        fig = px.line(
            filtered_df, 
            x="period", 
            y=metric, 
            color="crypto", 
            markers=True, 
            title=title,
            labels={metric: title, "period": "Period"}
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Please upload a CSV file to get started.")