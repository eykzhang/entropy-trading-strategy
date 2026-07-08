import numpy as np
import pandas as pd
from scipy.stats import entropy
from config import Config
from logger import logger

class DataHandler:
    def __init__(self):
        logger.info("DataHandler initialized")

    def compute_features(self, ohlc):
        """Calculate feature space exactly as defined in paper"""
        features = pd.DataFrame({
            'H-L': ohlc['high_price'] - ohlc['low_price'],
            'C-O': ohlc['close_price'] - ohlc['open_price'],
            'H-O': ohlc['high_price'] - ohlc['open_price'],
            'O-L': ohlc['open_price'] - ohlc['low_price']
        })
        return features

    def detect_swings(self, ohlc):
        """Safe pattern detection with data validation"""
        if ohlc.empty:
            return pd.DataFrame(), pd.DataFrame()

        try:
            # Verify we have required data
            required_col = 'close_price'
            if required_col not in ohlc.columns:
                raise KeyError(f"Missing required column: {required_col}")

            returns = ohlc[required_col].pct_change(Config.PATTERN_WINDOW)
            buy_patterns = ohlc[returns > Config.MIN_SWING].copy()
            sell_patterns = ohlc[returns < -Config.MIN_SWING].copy()
            
            buy_patterns['label'] = 'Buy'
            sell_patterns['label'] = 'Sell'
            
            return buy_patterns, sell_patterns

        except Exception as e:
            logger.error(f"Pattern detection failed: {str(e)}")
            return pd.DataFrame(), pd.DataFrame()

    def compute_local_entropy(self, pattern, all_patterns, labels, k=50):
        """Calculate entropy in pattern neighborhood"""
        distances = np.sum(np.abs(all_patterns - pattern), axis=1)  # L1 distance
        nearest = np.argpartition(distances, k)[:k]
        neighbor_labels = labels.iloc[nearest]
        prob = np.array([
            np.mean(neighbor_labels == 'Buy'),
            np.mean(neighbor_labels == 'Sell')
        ])
        return entropy(prob)