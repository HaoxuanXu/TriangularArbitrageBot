from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderStatus
from alpaca.trading.models import Order
import time

class TradeBroker:
    def __init__(self, is_paper: bool, entry_percent: float, config: dict[dict[str, str]]):
        if is_paper:
            self.trading_client = TradingClient(
                api_key=config["paper"]["api_key"],
                secret_key=config["paper"]["api_secret"]
            )
        else:
            self.trading_client = TradingClient(
                api_key=config["live"]["api_key"],
                secret_key=config["live"]["api_secret"]
            )
        self.account = self.trading_client.get_account()
        self.available_cash: float = float(self.account.cash)
        self.committed_cash: float = round(self.available_cash * entry_percent, 2) # round the committed cash to 2 digits
            
    # order is refresh as part of monitoring process until the 
    def __refresh_order(self, order_id: str) -> Order:
        order = self.trading_client.get_order_by_id(order_id)
        return order 
    
    def __monitor_order(self, order_id: str) -> list[Order, bool]:
        
        order = self.__refresh_order(order_id)
        
        while order.status not in [
            OrderStatus.FILLED, OrderStatus.CANCELED, OrderStatus.EXPIRED, OrderStatus.REJECTED,
            OrderStatus.STOPPED, OrderStatus.SUSPENDED, OrderStatus
        ]:
            order = self.refresh_order(order_id)
            time.sleep(0.1)
            
        return order
        
    def submit_market_order(self, symbol: str, is_notional: bool, qty: float, side: str) -> Order:
        
        if side == "buy":
            order_side = OrderSide.BUY
        elif side == "sell":
            order_side = OrderSide.SELL
        
        # initialize the order request param
        if is_notional:
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                notional=qty,
                side=order_side,
                time_in_force=TimeInForce.GTC
            )
        else:
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.GTC
            )
        
        market_order = self.trading_client.submit_order(
            order_data=market_order_data
        )
        
        if market_order.status != OrderStatus.FILLED:
            market_order = self.__monitor_order(market_order.id)
            
        return market_order
    
        