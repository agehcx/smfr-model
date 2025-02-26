import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the overall page configuration
st.set_page_config(page_title="Crypto Performance Metrics Dashboard", layout="wide")

# Sidebar navigation for pages
page = st.sidebar.radio("Navigate", ["Upload & Filter Data", "Coin Dashboard", "Coin Yearly Report"])

def load_data(file):
    df = pd.read_csv(file, sep='\t') if file.name.endswith('.tsv') else pd.read_csv(file)
    # Convert "Start" column to just the year and rename it to "Period"
    df["Period"] = pd.to_datetime(df["Start"]).dt.year.astype(str)
    # Convert "Max Drawdown Duration" to an integer by removing " days"
    df["Max Drawdown Duration"] = df["Max Drawdown Duration"].str.replace(" days", "").astype(int)
    return df

# Define metric groups
performance_metrics = {
    "Total Return [%]": "Total Return [%]",
    "Sharpe Ratio": "Sharpe Ratio",
    "Max Drawdown [%]": "Max Drawdown [%]"
}
additional_metrics = {
    "Benchmark Return [%]": "Benchmark Return [%]",
    "Win Rate [%]": "Win Rate [%]",
    "Average Win": "Avg Winning Trade [%]",
    "Average Loss": "Avg Losing Trade [%]"
}
extended_metrics = {
    "Start Value": "Start Value",
    "End Value": "End Value",
    # "Max Gross Exposure [%]": "Max Gross Exposure [%]",
    # "Total Fees Paid": "Total Fees Paid",
    "Profit Factor": "Profit Factor",
    "Expectancy": "Expectancy",
    "Calmar Ratio": "Calmar Ratio",
    "Omega Ratio": "Omega Ratio",
    "Sortino Ratio": "Sortino Ratio",
    "Max Drawdown Duration": "Max Drawdown Duration",
    "Total Trades": "Total Trades",
    "Total Closed Trades": "Total Closed Trades",
    # "Total Open Trades": "Total Open Trades",
    # "Open Trade PnL": "Open Trade PnL"
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
        period_options = df["Period"].unique().tolist()
        selected_periods = st.sidebar.multiselect("Select Periods", options=period_options, default=period_options)

        # Filter the dataframe based on sidebar selection
        filtered_df = df[(df["crypto"].isin(selected_cryptos)) & (df["Period"].isin(selected_periods))]
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

        st.markdown("### Performance Metrics")
        # Interactive graphs for performance metrics
        for title, metric in performance_metrics.items():
            fig = px.line(
                filtered_df, 
                x="Period", 
                y=metric, 
                color="crypto", 
                markers=True, 
                title=title,
                labels={metric: title, "Period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Additional Metrics")
        # Interactive graphs for additional metrics
        for title, metric in additional_metrics.items():
            fig = px.line(
                filtered_df, 
                x="Period", 
                y=metric, 
                color="crypto", 
                markers=True, 
                title=title,
                labels={metric: title, "Period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### Extended Metrics")
        # Interactive graphs for extended metrics
        for title, metric in extended_metrics.items():
            fig = px.line(
                filtered_df, 
                x="Period", 
                y=metric, 
                color="crypto", 
                markers=True, 
                title=title,
                labels={metric: title, "Period": "Period"}
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
        period_options = df["Period"].unique().tolist()
        selected_periods = st.sidebar.multiselect("Select Periods", options=period_options, default=period_options)

        # Filter the dataframe based only on the selected coin and periods
        filtered_df = df[(df["crypto"] == selected_coin) & (df["Period"].isin(selected_periods))]
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)

        st.markdown(f"### Performance Metrics for {selected_coin}")
        # Graphs for performance metrics for the selected coin
        for title, metric in performance_metrics.items():
            fig = px.line(
                filtered_df, 
                x="Period", 
                y=metric, 
                markers=True, 
                title=f"{title} for {selected_coin}",
                labels={metric: title, "Period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### Additional Metrics for {selected_coin}")
        # Graphs for additional metrics for the selected coin
        for title, metric in additional_metrics.items():
            fig = px.line(
                filtered_df, 
                x="Period", 
                y=metric, 
                markers=True, 
                title=f"{title} for {selected_coin}",
                labels={metric: title, "Period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### Extended Metrics for {selected_coin}")
        # Graphs for extended metrics for the selected coin
        for title, metric in extended_metrics.items():
            fig = px.line(
                filtered_df, 
                x="Period", 
                y=metric, 
                markers=True, 
                title=f"{title} for {selected_coin}",
                labels={metric: title, "Period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)

elif page == "Coin Yearly Report":
    st.title("Coin Yearly Report")
    st.write("Select a coin and a specific year to view the backtested results.")

    if "df" not in st.session_state:
        st.warning("No data found. Please go to the 'Upload & Filter Data' page to load a CSV file first.")
    else:
        df = st.session_state["df"]

        # Dropdown for coin selection
        coin_options = df["crypto"].unique().tolist()
        selected_coin = st.selectbox("Select a Coin", options=coin_options)

        # Dropdown for year selection
        year_options = df["Period"].unique().tolist()
        selected_year = st.selectbox("Select a Year", options=year_options)

        # Filter the dataframe based on selected coin and year
        filtered_df = df[(df["crypto"] == selected_coin) & (df["Period"] == selected_year)]
        st.subheader(f"Filtered Data for {selected_coin} in {selected_year}")
        st.dataframe(filtered_df)

        st.markdown(f"### Performance Metrics for {selected_coin} in {selected_year}")
        # Graphs for performance metrics for the selected coin and year
        for title, metric in performance_metrics.items():
            fig = px.line(
                filtered_df, 
                x="Period", 
                y=metric, 
                markers=True, 
                title=f"{title} for {selected_coin} in {selected_year}",
                labels={metric: title, "Period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### Additional Metrics for {selected_coin} in {selected_year}")
        # Graphs for additional metrics for the selected coin and year
        for title, metric in additional_metrics.items():
            fig = px.line(
                filtered_df, 
                x="Period", 
                y=metric, 
                markers=True, 
                title=f"{title} for {selected_coin} in {selected_year}",
                labels={metric: title, "Period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### Extended Metrics for {selected_coin} in {selected_year}")
        # Graphs for extended metrics for the selected coin and year
        for title, metric in extended_metrics.items():
            fig = px.line(
                filtered_df, 
                x="Period", 
                y=metric, 
                markers=True, 
                title=f"{title} for {selected_coin} in {selected_year}",
                labels={metric: title, "Period": "Period"}
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"### Summary Table for {selected_coin} in {selected_year}")
        # Display single value metrics as a table
        summary_data = filtered_df[[
            "Start Value", 
            "End Value", 
            "Total Return [%]", 
            "Benchmark Return [%]", 
            "Max Gross Exposure [%]", 
            "Total Fees Paid", 
            "Max Drawdown [%]", 
            "Max Drawdown Duration", 
            "Total Trades", 
            "Total Closed Trades", 
            "Total Open Trades", 
            "Open Trade PnL", 
            "Win Rate [%]", 
            "Profit Factor", 
            "Expectancy", 
            "Sharpe Ratio", 
            "Calmar Ratio", 
            "Omega Ratio", 
            "Sortino Ratio"
        ]].T
        summary_data.columns = ["Value"]
        st.table(summary_data)