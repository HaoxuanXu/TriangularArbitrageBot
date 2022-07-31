from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoLatestOrderbookRequest
from util import load_json


class MarketData:
    def __init__(self, accountType: str):
        config = load_json("./config/config.json")
        self.client = CryptoHistoricalDataClient(
            api_key=config[accountType]["api_key"],
            secret_key=config[accountType]["api_secret"]
        )
        
    """get_latest_crypto_orderbooks return the latest level II orderbooks for all coin pairs"""   
    def get_latest_crypto_orderbooks(self, coin_pairs:list):
        
        latest_orderbooks = self.client.get_crypto_latest_orderbook(
            CryptoLatestOrderbookRequest(
                symbol_or_symbols=coin_pairs
            )
        )
        
        return latest_orderbooks
        
        