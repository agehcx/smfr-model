import numpy as np
import pandas as pd

class MACDStrategy:
    def __init__(self, short_window: int = 12, long_window: int = 26, signal_window: int = 9):
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window

    def calc_combined_signal(self, prices: pd.Series) -> pd.Series:
        """
        Calculate MACD signal by computing the difference between short and long EMAs,
        then subtracting the signal line (EMA of the MACD line).
        The result is normalized before being returned.
        """
        ema_short = prices.ewm(span=self.short_window, adjust=False).mean()
        ema_long = prices.ewm(span=self.long_window, adjust=False).mean()
        macd_line = ema_short - ema_long
        signal_line = macd_line.ewm(span=self.signal_window, adjust=False).mean()
        macd_signal = macd_line - signal_line
        # Normalize the signal
        std = macd_signal.std() if macd_signal.std() != 0 else 1
        normalized_signal = (macd_signal - macd_signal.mean()) / std
        return normalized_signal

def calc_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate log returns for a series of prices.
    """
    returns = np.log(prices / prices.shift(1))
    return returns.dropna()

def calc_trend_intermediate_strategy(prices: pd.Series, w: float) -> pd.Series:
    """
    Compute a blended trend following signal. Uses a simple moving average difference as trend,
    and a momentum component calculated from rolling sum of returns.
    The weight 'w' controls the blending between momentum and trend.
    """
    # Calculate trend component using difference between short and long moving averages
    ma_short = prices.rolling(window=20, min_periods=1).mean()
    ma_long = prices.rolling(window=100, min_periods=1).mean()
    trend = np.sign(ma_short - ma_long)
    
    # Calculate momentum component using rolling sum of returns
    momentum = calc_returns(prices).rolling(window=5, min_periods=1).sum()
    momentum = momentum.reindex(prices.index, method='ffill').fillna(0)
    
    # Blend the signals
    signal = (1 - w) * trend + w * momentum
    # Normalize the signal
    std = signal.std() if signal.std() != 0 else 1
    normalized_signal = (signal - signal.mean()) / std
    return normalized_signal

def calc_daily_vol(prices: pd.Series, window: int = 20) -> pd.Series:
    """
    Calculate daily volatility based on the rolling standard deviation of returns.
    """
    returns = calc_returns(prices)
    vol = returns.rolling(window=window, min_periods=1).std()
    return vol