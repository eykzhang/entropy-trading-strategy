import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ALPACA_API_KEY = os.getenv('APCA_API_KEY_ID')
    ALPACA_SECRET_KEY = os.getenv('APCA_API_SECRET_KEY')
    ALPACA_PAPER = True
    
    # Entropy Strategy Parameters
    TICKERS = ["SPY"]  # Primary trading instrument
    TIME_FRAME = "15Min"
    PATTERN_WINDOW = 20  # Bars for pattern detection
    THETA = 1.0  # L1 distance threshold
    ALPHA = 0.7  # Entropy/PnL weighting
    MIN_SWING = 0.015  # 1.5% price movement threshold
    
    # Feature Space
    FEATURES = ['H-L', 'C-O', 'H-O', 'O-L']  # Exactly as in paper