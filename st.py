import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page configuration
st.set_page_config(page_title="Crypto Performance Metrics Dashboard", layout="wide")

# Sidebar navigation for pages
page = st.sidebar.radio("Navigate", ["Upload & Filter Data", "Coin Dashboard"])

def load_data(file):
    df = pd.read_csv(file)
    df["period"] = df["period"].astype(str)
    return df

if page == "Upload & Filter Data":
    st.title("Crypto Performance Metrics Dashboard")
    st.write("Upload a CSV file containing the crypto backtest results.")

    # File uploader for CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.session_state["df"] = df  # store dataframe in session state

        st.subheader("Data Preview")
        st.dataframe(df)

        # Sidebar filtering options on this page
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

elif page == "Coin Dashboard":
    st.title("Coin Dashboard")
    st.write("This page lets you select a coin from the dropdown and view interactive graphs for all metrics.")

    if "df" not in st.session_state:
        st.warning("No data found. Please go to the 'Upload & Filter Data' page to load a CSV file first.")
    else:
        df = st.session_state["df"]

        # Create a dropdown for coin selection directly on the main page
        coin_options = df["crypto"].unique().tolist()
        selected_coin = st.selectbox("Select a Coin", options=coin_options)

        # Sidebar filtering options for period selection (coin selection is handled by dropdown above)
        st.sidebar.header("Filter Options")
        period_options = df["period"].unique().tolist()
        selected_periods = st.sidebar.multiselect("Select Periods", options=period_options, default=period_options)

        # Filter the dataframe based on the selected coin and periods
        filtered_df = df[(df["crypto"] == selected_coin) & (df["period"].isin(selected_periods))]
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
                markers=True, 
                title=f"{title} for {selected_coin}",
                labels={metric: title, "period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)