"""
BONUS: Stop-Limit Order Support

This module demonstrates extended order types beyond basic MARKET and LIMIT.
Uncomment and integrate into the main CLI to use.
"""

import logging
from typing import Any, Dict

from bot.client import BinanceFuturesClient, BinanceAPIError, BinanceNetworkError

logger = logging.getLogger("trading_bot.trade")
error_logger = logging.getLogger("trading_bot.error")


def place_stop_limit_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    stop_price: float,
    time_in_force: str = "GTC"
) -> Dict[str, Any]:
    """
    Place a stop-limit order.
    
    A stop-limit order will only be placed on the order book once the price
    touches the stopPrice. Then it acts as a limit order at the specified price.
    
    Args:
        client: BinanceFuturesClient instance
        symbol: Trading pair (e.g., BTCUSDT)
        side: BUY or SELL
        quantity: Order quantity
        price: Limit price (at which the order will execute)
        stop_price: Stop price (trigger price)
        time_in_force: GTC, IOC, or FOK (default GTC)
        
    Returns:
        Order response data
        
    Example:
        # Set a buy order that triggers when BTC drops to 42000, then buys at 41500
        response = place_stop_limit_order(
            client=client,
            symbol="BTCUSDT",
            side="BUY",
            quantity=0.001,
            price=41500,        # Limit price
            stop_price=42000,   # Trigger price
        )
        
        # Set a sell order that triggers when ETH rises to 2100, then sells at 2150
        response = place_stop_limit_order(
            client=client,
            symbol="ETHUSDT",
            side="SELL",
            quantity=1.0,
            price=2150,         # Limit price (higher than current to ensure fill)
            stop_price=2100,    # Trigger price
        )
    """
    try:
        logger.info(
            f"Placing STOP-LIMIT {side} order: {quantity} {symbol} | "
            f"Stop: {stop_price}, Limit: {price}"
        )
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": "STOP",  # Binance uses "STOP" for stop-loss/stop-limit
            "quantity": quantity,
            "price": price,         # Limit price
            "stopPrice": stop_price,  # Stop price
            "timeInForce": time_in_force,
        }
        
        response = client._request("POST", "/fapi/v1/order", params=params, signed=True)
        
        logger.info(
            f"Stop-Limit order placed! ID: {response.get('orderId', 'N/A')}, "
            f"Status: {response.get('status', 'N/A')}"
        )
        return response
        
    except (BinanceAPIError, BinanceNetworkError) as e:
        error_msg = f"Failed to place STOP-LIMIT order: {str(e)}"
        error_logger.error(error_msg)
        raise Exception(error_msg) from e


def place_occo_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    stop_price: float,
    stop_limit_price: float,
) -> Dict[str, Any]:
    """
    Place an OCO (One-Cancels-Other) order.
    
    An OCO order consists of two orders:
    1. A LIMIT order at the specified price
    2. A STOP-LIMIT order at stopPrice/stopLimitPrice
    
    When one order fills, the other is automatically canceled.
    
    Args:
        client: BinanceFuturesClient instance
        symbol: Trading pair
        side: BUY or SELL
        quantity: Order quantity
        price: Limit price for the limit order
        stop_price: Stop price for the stop-limit order
        stop_limit_price: Limit price for the stop-limit order
        
    Returns:
        OCO order response
        
    Example:
        # Sell 1 ETH either at 2200 (limit) or when it drops to 1800 and sell at 1750
        response = place_occo_order(
            client=client,
            symbol="ETHUSDT",
            side="SELL",
            quantity=1.0,
            price=2200,              # Regular limit order
            stop_price=1800,         # Stop-loss trigger
            stop_limit_price=1750,   # Stop-loss limit price
        )
    """
    try:
        logger.info(
            f"Placing OCO order: {quantity} {symbol} | "
            f"Limit: {price}, Stop: {stop_price}/{stop_limit_price}"
        )
        
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "stopPrice": stop_price,
            "stopLimitPrice": stop_limit_price,
        }
        
        response = client._request("POST", "/fapi/v1/orderList", params=params, signed=True)
        
        logger.info(
            f"OCO order placed! ID: {response.get('orderListId', 'N/A')}, "
            f"Status: {response.get('listStatus', 'N/A')}"
        )
        return response
        
    except (BinanceAPIError, BinanceNetworkError) as e:
        error_msg = f"Failed to place OCO order: {str(e)}"
        error_logger.error(error_msg)
        raise Exception(error_msg) from e


# Example CLI integration (add to cli.py):
"""
parser.add_argument(
    "--stop-price",
    type=float,
    default=None,
    help="Stop price for STOP-LIMIT orders"
)

if args.order_type == "STOP-LIMIT":
    if not args.price or not args.stop_price:
        print("ERROR: Both --price and --stop-price required for STOP-LIMIT")
        sys.exit(1)
    response = place_stop_limit_order(
        client, symbol, side, quantity, args.price, args.stop_price
    )
"""
