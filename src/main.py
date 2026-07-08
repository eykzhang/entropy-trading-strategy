from config import Config
from logger import logger
from alpaca_client import AlpacaClient
from data_handler import DataHandler
from trading_strategy import TradingStrategy

def main():
    try:
        logger.info("Starting entropy trading bot")
        
        alpaca = AlpacaClient()
        dh = DataHandler()
        strategy = TradingStrategy(dh, alpaca)
        
        for symbol in Config.TICKERS:
            strategy.run(symbol)
            
    except Exception as e:
        logger.critical(f"Strategy failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()