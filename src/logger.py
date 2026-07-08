import logging
from pathlib import Path
import os

def setup_logging():
    """Configure logging with automatic directory creation"""
    log_dir = Path("logs")
    log_file = log_dir / "trading_bot.log"
    
    # Create logs directory if it doesn't exist
    try:
        log_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(f"Failed to create logs directory: {e}")
        # Fallback to console-only logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger('trading_bot')
    
    # Full logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('trading_bot')

logger = setup_logging()