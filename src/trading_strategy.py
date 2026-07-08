import numpy as np
from config import Config
from logger import logger

class TradingStrategy:
    def __init__(self, data_handler, alpaca_client):
        self.dh = data_handler
        self.alpaca = alpaca_client
        logger.info("TradingStrategy initialized")

    def score_patterns(self, patterns, feature_matrix, labels, historical_pnl):
        """Implement Algorithm 1 scoring"""
        global_entropy = entropy(np.bincount(labels == 'Buy') / len(labels))
        scores = []
        
        for i, pattern in patterns.iterrows():
            H_local = self.dh.compute_local_entropy(
                feature_matrix[i], feature_matrix, labels
            )
            IG = global_entropy - H_local
            pnl_norm = (historical_pnl[i] - historical_pnl.min()) / (historical_pnl.max() - historical_pnl.min())
            scores.append(Config.ALPHA * IG + (1 - Config.ALPHA) * pnl_norm)
            
        return scores

    def filter_conflicts(self, buy_patterns, sell_patterns, buy_scores, sell_scores):
        """Resolve pattern overlaps per θ threshold"""
        buy_features = buy_patterns[Config.FEATURES].values
        sell_features = sell_patterns[Config.FEATURES].values
        
        for i, buy_feat in enumerate(buy_features):
            for j, sell_feat in enumerate(sell_features):
                if np.sum(np.abs(buy_feat - sell_feat)) < Config.THETA:
                    if buy_scores[i] >= sell_scores[j]:
                        sell_patterns.iloc[j] = None
                    else:
                        buy_patterns.iloc[i] = None
        
        return buy_patterns.dropna(), sell_patterns.dropna()

    def run(self, symbol):
        try:
            logger.info(f"Running strategy for {symbol}")
            
            # 1. Get and validate data
            ohlc = self.alpaca.get_ohlc(symbol, Config.TIME_FRAME)
            if ohlc.empty:
                logger.warning(f"Skipping {symbol} - no data available")
                return
                
            if len(ohlc) < Config.PATTERN_WINDOW * 2:
                logger.warning(f"Skipping {symbol} - insufficient data ({len(ohlc)} bars)")
                return

            # 2. Detect patterns
            buy_raw, sell_raw = self.dh.detect_swings(ohlc)
            if buy_raw.empty and sell_raw.empty:
                logger.info("No patterns detected")
                return

            # Rest of your strategy logic...
            features = self.dh.compute_features(ohlc)
            
            # 3. Score patterns (using mock PnL for now)
            historical_pnl = np.random.uniform(50, 100, len(buy_raw))
            buy_scores = self.score_patterns(buy_raw, features, buy_raw['label'], historical_pnl)
            
            historical_pnl = np.random.uniform(50, 100, len(sell_raw))
            sell_scores = self.score_patterns(sell_raw, features, sell_raw['label'], historical_pnl)
            
            # 4. Filter conflicts
            buy_filtered, sell_filtered = self.filter_conflicts(buy_raw, sell_raw, buy_scores, sell_scores)
            
            # 5. Execute trades
            if not buy_filtered.empty:
                logger.info(f"Executing {len(buy_filtered)} buy orders")
                self.alpaca.submit_order(symbol, 100, 'buy')
                
            if not sell_filtered.empty:
                logger.info(f"Executing {len(sell_filtered)} sell orders")
                self.alpaca.submit_order(symbol, 100, 'sell')

        except Exception as e:
            logger.error(f"Strategy execution failed: {str(e)}", exc_info=True)