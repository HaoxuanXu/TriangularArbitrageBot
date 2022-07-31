from alpaca.data.models import Orderbook


def __bought_sold_quantity(orderbook: Orderbook, committed_cash: float, is_buy: bool) -> float:
    
    cash_available = committed_cash
    transacted_qty = 0
    
    if is_buy:
        quote_levels = orderbook.asks
    else:
        quote_levels = orderbook.bids
    

    if is_buy:
        for order_quote in orderbook.asks:
            if order_quote.price * order_quote.size >= cash_available:
                transacted_qty += cash_available / order_quote.price
                break
            else:
                cash_available -= order_quote.price * order_quote.size
                transacted_qty += order_quote.size
    else:
        for order_quote in orderbook.bids:
            if order_quote.size >= cash_available:
                transacted_qty += order_quote.price * cash_available
                break 
            else:
                cash_available -= order_quote.size
                transacted_qty += order_quote.size * order_quote.price
        
        
    return transacted_qty

def predict_trading_return(
    base_coin_symbol, 
    paired_coin_symbol: str, 
    orderbooks: dict[str, list[Orderbook, ...]], 
    committed_cash: float) -> float:
    
    base_coin_usd_symbol: str = base_coin_symbol + "/USD" 
    paired_coin_usd_symbol: str = paired_coin_symbol + "/USD"
    paired_coin_base_coin_symbol: str = paired_coin_symbol + "/" + base_coin_symbol
    
    # quantity of base coin bought in the first step
    base_coin_qty: float = __bought_sold_quantity(
        orderbook=orderbooks[base_coin_usd_symbol],
        committed_cash=committed_cash,
        is_buy=True
    )
    
    # quantity of the paired coin bought with the base coin 
    paired_coin_qty: float = __bought_sold_quantity(
        orderbook=orderbooks[paired_coin_base_coin_symbol],
        committed_cash=base_coin_qty,
        is_buy=True
    )
    
    # quantity of usd received after selling the paired coin
    final_usd_qty: float = __bought_sold_quantity(
        orderbook=orderbooks[paired_coin_usd_symbol], 
        committed_cash=paired_coin_qty,
        is_buy=False
    )
    
    return (final_usd_qty - committed_cash) / committed_cash

def get_optimal_pair(
    orderbooks: dict[str, list[Orderbook, ...]], 
    coin_dependency: dict[str, dict[str, list[str, ...]]],
    committed_cash: float) -> (float, list):
    
    # initialize profit percent and winning pair as null
    max_profit_percent = 0
    winning_pair = [] # [paired_coin, base_coin]
    
    for base_coin_symbol, paired_coin_list in coin_dependency["coin"].items():
        
        for paired_coin_symbol in paired_coin_list:
            
            profit_percent = predict_trading_return(base_coin_symbol, paired_coin_symbol, orderbooks, committed_cash)
            
            if profit_percent > max_profit_percent:
                max_profit_percent = profit_percent
                winning_pair = [paired_coin_symbol, base_coin_symbol]
                
    return max_profit_percent, winning_pair


    
    
    
