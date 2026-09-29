from __future__ import annotations
import math
from typing import Any
import numpy as np
import pandas as pd
import yfinance as yf

def _clean(value: Any) -> float | None:
    try:
        number = float(value)
        return round(number, 4) if math.isfinite(number) else None
    except (TypeError, ValueError):
        return None

def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean().replace(0, np.nan)
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def get_stock_analysis(ticker: str, period: str = "3mo") -> dict:
    symbol = ticker.strip().upper()
    if not symbol:
        raise ValueError("Ticker is required.")
    if period not in {"1mo", "3mo", "6mo", "1y", "2y"}:
        period = "3mo"
    history = yf.Ticker(symbol).history(period=period, auto_adjust=False)
    if history.empty:
        raise ValueError(f"No market data was returned for '{symbol}'. Check the ticker and try again.")
    df = history.reset_index()
    date_col = "Datetime" if "Datetime" in df.columns else "Date"
    df["date"] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")
    close = pd.to_numeric(df["Close"], errors="coerce")
    df["sma20"] = close.rolling(20).mean()
    df["ema20"] = close.ewm(span=20, adjust=False).mean()
    df["rsi14"] = _rsi(close)
    returns = close.pct_change()
    volatility = returns.std() * np.sqrt(252) if returns.notna().sum() > 1 else np.nan
    first_close = close.dropna().iloc[0]
    latest_close = close.iloc[-1]
    total_return = ((latest_close / first_close) - 1) * 100 if first_close else np.nan
    chart = [
        {"date": r["date"], "close": _clean(r["Close"]), "volume": _clean(r["Volume"]),
         "sma20": _clean(r["sma20"]), "ema20": _clean(r["ema20"]), "rsi14": _clean(r["rsi14"])}
        for _, r in df.tail(120).iterrows()
    ]
    return {"ticker": symbol, "period": period,
            "summary": {"latest_close": _clean(latest_close),
                        "period_return_pct": _clean(total_return),
                        "annualized_volatility_pct": _clean(volatility * 100),
                        "rsi14": _clean(df["rsi14"].iloc[-1])},
            "chart": chart}
