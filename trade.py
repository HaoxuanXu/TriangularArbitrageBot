from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderStatus
import time
from logger import LoggerInstance

class TradeBroker:
    def __init__(self, account_type: str, entry_percent: float, config: dict[dict[str, str]]):
        self.trading_client = TradingClient(
                api_key=config[account_type]["api_key"],
                secret_key=config[account_type]["api_secret"],
                paper=True
            )
        self.account = self.trading_client.get_account()
        self.available_cash: float = float(self.account.cash)
        self.committed_cash: float = round(self.available_cash * entry_percent, 2) # round the committed cash to 2 digits
            
    # order is refresh as part of monitoring process until the 
    def __refresh_order(self, order_id: str):
        order = self.trading_client.get_order_by_id(order_id)
        return order 
    
    def __monitor_order(self, order_id: str):
        
        order = self.__refresh_order(order_id)
        
        while order.status not in [
            OrderStatus.FILLED, OrderStatus.CANCELED, OrderStatus.EXPIRED, OrderStatus.REJECTED,
            OrderStatus.STOPPED, OrderStatus.SUSPENDED, OrderStatus
        ]:
            order = self.refresh_order(order_id)
            time.sleep(0.1)
            
        return order
        
    def submit_market_order(self, symbol: str, is_notional: bool, qty: float, side: str):
        
        if side == "buy":
            order_side = OrderSide.BUY
        elif side == "sell":
            order_side = OrderSide.SELL
            
        
        # initialize the order request param
        try:
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
                
        except Exception as e:
            LoggerInstance.logger.error(e)
            
        return market_order
    
        