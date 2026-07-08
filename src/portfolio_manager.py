"""
Portfolio management and risk control
"""

from logger import logger
from alpaca_client import AlpacaClient
from config import Config

class PortfolioManager:
    def __init__(self):
        self.alpaca_client = AlpacaClient()
        logger.info("Portfolio manager initialized")
        
    def enter_position(self, ticker):
        """Enter a new position with proper risk management"""
        try:
            # Get account information
            account = self.alpaca_client.get_account_info()
            equity = float(account.equity)
            
            # Calculate position size based on risk parameters
            position_size = equity * Config.MAX_POSITION_SIZE
            
            # Get current price (simplified - in reality you'd want more robust price checking)
            last_price = self.alpaca_client.get_market_data(
                [ticker], 
                "1Min", 
                pd.Timestamp.now() - pd.Timedelta(minutes=5),
                pd.Timestamp.now()
            )['close'].iloc[-1]
            
            # Calculate quantity
            qty = int(position_size / last_price)
            
            if qty > 0:
                # Submit buy order
                self.alpaca_client.submit_order(ticker, qty, "buy")
                logger.info(f"Entered position in {ticker}: {qty} shares")
                
        except Exception as e:
            logger.error(f"Error entering position: {e}")
            raise
            
    def exit_position(self, ticker):
        """Exit an existing position"""
        try:
            # Get current position
            positions = self.alpaca_client.get_positions()
            position = next((p for p in positions if p.symbol == ticker), None)
            
            if position:
                # Submit sell order
                qty = int(float(position.qty))
                self.alpaca_client.submit_order(ticker, qty, "sell")
                logger.info(f"Exited position in {ticker}: {qty} shares")
                
        except Exception as e:
            logger.error(f"Error exiting position: {e}")
            raise
            
    def rebalance_portfolio(self):
        """Rebalance portfolio according to strategy rules"""
        # Implement if your strategy requires periodic rebalancing
        pass