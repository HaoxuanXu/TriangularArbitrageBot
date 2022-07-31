import logging 
from logging.handlers import RotatingFileHandler


class TradeLogger:
    def __init__(self):
        self.logger = self.set_logger(name, path)

    def set_logger(self) -> logging.Logger:
        
        logging.basicConfig()
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        # add log rotation 
        handler = RotatingFileHandler(f".log/trade_log.log", maxBytes=2000, backupCount=3)
        logger.addHandler(handler)
        
        return logger
    

LoggerInstance = TradeLogger()
    