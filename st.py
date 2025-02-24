import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the overall page configuration
st.set_page_config(page_title="Crypto Performance Metrics Dashboard", layout="wide")

# Sidebar navigation for pages
page = st.sidebar.radio("Navigate", ["Upload & Filter Data", "Coin Dashboard"])

def load_data(file):
    df = pd.read_csv(file, sep='\t') if file.name.endswith('.tsv') else pd.read_csv(file)
    # Ensure period column is treated as a string
    df["period"] = df["period"].astype(str)
    return df

# Define metric groups
performance_metrics = {
    "Total Return": "total_return",
    "Sharpe Ratio": "sharpe_ratio",
    "Max Drawdown": "max_drawdown"
}
additional_metrics = {
    "Benchmark Return": "benchmark_return",
    "Win Rate": "win_rate",
    "Average Win": "avg_win",
    "Average Loss": "avg_loss"
}

if page == "Upload & Filter Data":
    st.title("Crypto Performance Metrics Dashboard")
    st.write("Upload a CSV file containing the crypto backtest results including additional parameters.")

    # File uploader for CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv", "tsv"])
    
    if uploaded_file is not None:
        # Load the data and store it in the session state
        df = load_data(uploaded_file)
        st.session_state["df"] = df

        st.subheader("Data Preview")
        st.dataframe(df)

        # Sidebar filtering options for the Upload & Filter Data page
        st.sidebar.header("Filter Options")
        crypto_options = df["crypto"].unique().tolist()
        selected_cryptos = st.sidebar.multiselect("Select Cryptos", options=crypto_options, default=crypto_options)
        period_options = df["period"].unique().tolist()
        selected_periods = st.sidebar.multiselect("Select Periods", options=period_options, default=period_options)

        # Filter the dataframe based on sidebar selection
        filtered_df = df[(df["crypto"].isin(selected_cryptos)) & (df["period"].isin(selected_periods))]
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

        st.markdown("### Performance Metrics")
        # Interactive graphs for performance metrics
        for title, metric in performance_metrics.items():
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

        st.markdown("### Additional Metrics")
        # Interactive graphs for additional metrics
        for title, metric in additional_metrics.items():
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
    st.write("Select a coin from the dropdown to view interactive graphs for all metrics.")

    if "df" not in st.session_state:
        st.warning("No data found. Please go to the 'Upload & Filter Data' page to load a CSV file first.")
    else:
        df = st.session_state["df"]

        # Dropdown for coin selection on the main page (no coin selection on sidebar in this view)
        coin_options = df["crypto"].unique().tolist()
        selected_coin = st.selectbox("Select a Coin", options=coin_options)

        # Sidebar filtering options for period selection
        st.sidebar.header("Filter Options")
        period_options = df["period"].unique().tolist()
        selected_periods = st.sidebar.multiselect("Select Periods", options=period_options, default=period_options)

        # Filter the dataframe based only on the selected coin and periods
        filtered_df = df[(df["crypto"] == selected_coin) & (df["period"].isin(selected_periods))]
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

        st.markdown(f"### Performance Metrics for {selected_coin}")
        # Graphs for performance metrics for the selected coin
        for title, metric in performance_metrics.items():
            fig = px.line(
                filtered_df, 
                x="period", 
                y=metric, 
                markers=True, 
                title=f"{title} for {selected_coin}",
                labels={metric: title, "period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### Additional Metrics for {selected_coin}")
        # Graphs for additional metrics for the selected coin
        for title, metric in additional_metrics.items():
            fig = px.line(
                filtered_df, 
                x="period", 
                y=metric, 
                markers=True, 
                title=f"{title} for {selected_coin}",
                labels={metric: title, "period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)