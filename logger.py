import logging 
import sys
from logging.handlers import RotatingFileHandler


class TradeLogger:
    def __init__(self):
        self.logger = self.set_logger()

    def set_logger(self) -> logging.Logger:
        
        logging.basicConfig()
        logger = logging.getLogger("trade_log")
        logger.setLevel(logging.INFO)
        
        # add log rotation 
        handler = RotatingFileHandler(f"log/trade_log.log", mode="a", maxBytes=20000, backupCount=3)
        logger.addHandler(handler)
        
        return logger
    

LoggerInstance = TradeLogger()
    