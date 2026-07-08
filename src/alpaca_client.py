import alpaca_trade_api as tradeapi
import pandas as pd
from config import Config
from logger import logger

class AlpacaClient:
    def __init__(self):
        self.api = tradeapi.REST(
            Config.ALPACA_API_KEY,
            Config.ALPACA_SECRET_KEY,
            base_url='https://paper-api.alpaca.markets'
        )
        logger.info("Alpaca client initialized")
        
    def get_ohlc(self, symbol, timeframe, limit=1000):
        """Fetch and standardize OHLC data with robust error handling"""
        try:
            # Get raw bars
            bars = self.api.get_bars(symbol, timeframe, limit=limit).df
            if bars.empty:
                logger.warning(f"No data returned for {symbol} {timeframe}")
                return pd.DataFrame()

            # Standardize column names (handles all Alpaca API versions)
            columns_map = {
                'open': 'open_price',
                'high': 'high_price',
                'low': 'low_price',
                'close': 'close_price',
                'volume': 'volume',
                'Open': 'open_price',
                'High': 'high_price',
                'Low': 'low_price',
                'Close': 'close_price',
                'Volume': 'volume'
            }
            bars = bars.rename(columns=columns_map)
            
            # Ensure we have required columns
            required_cols = ['open_price', 'high_price', 'low_price', 'close_price']
            missing_cols = [col for col in required_cols if col not in bars.columns]
            if missing_cols:
                raise ValueError(f"Missing columns: {missing_cols}")

            logger.info(f"Successfully retrieved {len(bars)} bars for {symbol}")
            return bars[required_cols]  # Return only standardized columns

        except Exception as e:
            logger.error(f"Data fetch failed for {symbol}: {str(e)}")
            return pd.DataFrame()
    def submit_order(self, symbol, qty, side):
        """Execute trade with error handling"""
        try:
            self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type="market",
                time_in_force="gtc"
            )
            logger.info(f"Order executed: {side} {qty} {symbol}")
        except Exception as e:
            logger.error(f"Order failed: {str(e)}")