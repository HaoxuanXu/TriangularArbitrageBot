from data import MarketData
from util import load_json
from trade import TradeBroker
from assets import TradingAssets
from signal import get_optimal_pair
import argparse
from alpaca.trading.models import Order


def commit_triangular_arbitrage(
    base_coin_symbol: str, 
    paired_coin_symbol: str,
    trading_client: TradeBroker,
    assets: TradingAssets
) -> float:
    
    # 1. start by buying the base coin
    buy_base_coin_with_usd_symbol: str = base_coin_symbol + "/USD"
    buy_base_coin_order: Order = trading_client.submit_market_order(
        symbol=buy_base_coin_with_usd_symbol,
        is_notional=True,
        qty=trading_client.committed_cash,
        side="buy"
    )
    
    base_coin_amount: float = float(buy_base_coin_order.filled_qty)
    
    # 2. buy the paired coin with the base coin
    buy_paired_coin_with_base_coin_symbol: str = paired_coin_symbol + "/" + base_coin_symbol
    buy_paired_coin_order: Order = trading_client.submit_market_order(
        symbol=buy_paired_coin_with_base_coin_symbol,
        is_notional=True,
        qty=base_coin_amount,
        side="buy"
    )
    
    paired_coin_amount: float = float(buy_paired_coin_order.filled_qty)
    
    # 3. sell the paired coin back to usd
    sell_paired_coin_for_usd_symbol: str = paired_coin_symbol + "/USD"
    sell_paired_coin_for_usd_order: Order = trading_client.submit_market_order(
        symbol=sell_paired_coin_for_usd_symbol,
        is_notional=False,
        qty=paired_coin_amount,
        side="sell"
    )
    
    exit_cash_amount: float = float(sell_paired_coin_for_usd_order.filled_avg_price) * float(sell_paired_coin_for_usd_order.filled_qty)
    
    return exit_cash_amount - trading_client.committed_cash
    
    
    
if __name__ == "__main__":
    # add is_paper parameter 
    parser = argparse.ArgumentParser(description="run the bot in live or paper account")
    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument("--live", dest="account", action="store_true")
    feature_parser.add_argument("--no-live", dest="account", action="store_false")
    parser.add_argument("--entrypercent", dest="entry_percent", type=float())
    parser.set_defaults(account=False)
    parser.set_defaults(entry_percent=0.2)
    args = parser.parse_args()
    
    is_paper = args.account
    entry_percent = args.entry_percent
    config = load_json(path)
    
    market_data_source = MarketData(accountType, config)
    trade_broker = TradeBroker(is_paper, config)
    tradable_assets = TradingAssets()
    
    # start an infinite loop
    while True:
        # get the most recent dictionary of order books
        latest_orderbooks = market_data_source.get_latest_crypto_orderbooks(tradable_assets.coin_pairs)
        
        current_optimal_profit_percent, winning_pair = get_optimal_pair(
            orderbooks=latest_orderbooks,
            coin_dependency=tradable_assets.coin_dependency,
            committed_cash=trade_broker.committed_cash
        )
        
        # We will make the transaction if the profit is percent is equal or larger than 1 percent
        if current_optimal_profit_percent >= 0.01:
            
            profit = commit_triangular_arbitrage(
                base_coin_symbol=winning_pair[1],
                paired_coin_symbol=winning_pair[0],
                trading_client=trade_broker,
                assets=tradable_assets
            )
        