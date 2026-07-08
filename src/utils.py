"""
Utility functions for the trading bot
"""

import pandas as pd
from logger import logger

def format_timestamp(timestamp):
    """Format timestamp for display"""
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def calculate_portfolio_metrics(positions, equity):
    """Calculate various portfolio metrics"""
    metrics = {
        'total_equity': equity,
        'num_positions': len(positions),
        'position_values': {p.symbol: float(p.market_value) for p in positions}
    }
    return metrics

def save_backtest_results(results, filename='backtest_results.csv'):
    """Save backtest results to CSV"""
    try:
        results.to_csv(filename)
        logger.info(f"Saved backtest results to {filename}")
    except Exception as e:
        logger.error(f"Error saving backtest results: {e}")
        raise