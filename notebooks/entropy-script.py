import os
import asyncio
import pandas as pd
import numpy as np
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from collections import deque
import datetime as dt
from dotenv import load_dotenv

# Load environment variables
load_dotenv("../.env")
API_KEY = os.getenv("APCA_API_KEY_ID")
SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")

# Alpaca clients
data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
stream = StockDataStream(API_KEY, SECRET_KEY)
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

symbol = "AAPL"
window_size = 30
bars = deque(maxlen=window_size)

# Account state
account = trading_client.get_account()
cash = float(account.cash)
positions = trading_client.get_all_positions()
position = next((p for p in positions if p.symbol == symbol), None)
shares = int(position.qty) if position else 0
current_position = 1 if shares > 0 else 0
signal = 'HOLD'
current_entropy = 0

def calculate_entropy(price_series, bins=10):
    if len(price_series) < 2:
        return 0
    hist, _ = np.histogram(price_series, bins=bins, density=True)
    hist = hist[hist > 0]
    return -np.sum(hist * np.log2(hist))

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_dashboard(latest_price, entropy, signal, position, cash, shares):
    clear_terminal()
    print(f"{'='*40}")
    print(f"🚀 Live Trading Dashboard — {symbol}")
    print(f"{'='*40}")
    print(f"Last Price       : ${latest_price:.2f}")
    print(f"Entropy (H)      : {entropy:.4f}")
    print(f"Signal           : {signal}")
    print(f"Current Position : {'IN TRADE' if position else 'NO POSITION'}")
    print(f"Cash Available   : ${cash:.2f}")
    print(f"Shares Held      : {shares}")
    print(f"Portfolio Value  : ${cash + shares * latest_price:.2f}")
    print(f"{'='*40}")

def get_entropy_thresholds():
    end = dt.datetime.now()
    start = end - dt.timedelta(days=30)
    request = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Minute, start=start, end=end)
    df = data_client.get_stock_bars(request).df

    if isinstance(df.index, pd.MultiIndex):
        df = df.xs(symbol)

    df = df.sort_index()

    entropies = []
    for i in range(0, len(df) - window_size + 1):
        window = df['close'].iloc[i:i+window_size].values
        entropies.append(calculate_entropy(window))

    entropy_series = pd.Series(entropies)
    low_th = entropy_series.quantile(0.2)
    high_th = entropy_series.quantile(0.8)

    print(f"Low threshold: {low_th:.3f}, High threshold: {high_th:.3f}")
    return low_th, high_th

def create_handler(low_th, high_th):
    async def handle_bar(bar):
        nonlocal cash, shares, current_position, signal, current_entropy

        price = bar['c']  # correct for your SDK version (dictionary)
        bars.append(price)

        if len(bars) == window_size:
            entropy = calculate_entropy(list(bars))
            current_entropy = entropy
            signal = 'HOLD'

            if entropy < low_th and current_position == 0:
                signal = 'BUY'
                order = MarketOrderRequest(symbol=symbol, qty=1, side=OrderSide.BUY, type="market", time_in_force=TimeInForce.GTC)
                trading_client.submit_order(order)
                current_position = 1
                cash -= price
                shares += 1

            elif entropy > high_th and current_position == 1:
                signal = 'SELL'
                order = MarketOrderRequest(symbol=symbol, qty=1, side=OrderSide.SELL, type="market", time_in_force=TimeInForce.GTC)
                trading_client.submit_order(order)
                current_position = 0
                cash += price
                shares -= 1

        print_dashboard(price, current_entropy, signal, current_position, cash, shares)

    return handle_bar

async def main():
    low_th, high_th = get_entropy_thresholds()
    await stream.subscribe_bars(create_handler(low_th, high_th), symbol)
    await stream._run_forever()  # legacy SDK-compatible way

if __name__ == "__main__":
    asyncio.run(main())