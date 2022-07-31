from util import load_json

class TradingAssets:
    def __init__(self):
        self.coin_dependency: dict[str, dict[str, list[str, ...]]] = load_json("./assets.json")["coins"]
        self.coin_pairs = []
        self.build_coin_pairs()
        
    def build_coin_pairs(self):
        for base_coin, paired_coin_list in self.coin_dependency.items():
            self.coin_pairs.append(base_coin + "/" + "USD")
            
            for paired_coin in paired_coin_list:
                self.coin_pairs.append(paired_coin + "/" + "USD")
                self.coin_pairs.append(paired_coin + "/" + base_coin)