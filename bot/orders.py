"""Order placement logic for the trading bot."""

import logging
from typing import Any, Dict

from .client import BinanceFuturesClient, BinanceAPIError, BinanceNetworkError
from .validators import ValidationError

logger = logging.getLogger("trading_bot.trade")
error_logger = logging.getLogger("trading_bot.error")


class OrderPlacementError(Exception):
    """Raised when order placement fails."""
    pass


def format_order_response(response: Dict[str, Any]) -> str:
    """
    Format order response for display.
    
    Args:
        response: Order response from API
        
    Returns:
        Formatted string with order details
    """
    lines = [
        "\n" + "="*60,
        "ORDER PLACED SUCCESSFULLY",
        "="*60,
        f"  Order ID:        {response.get('orderId', 'N/A')}",
        f"  Symbol:          {response.get('symbol', 'N/A')}",
        f"  Side:            {response.get('side', 'N/A')}",
        f"  Order Type:      {response.get('type', 'N/A')}",
        f"  Status:          {response.get('status', 'N/A')}",
        f"  Quantity:        {response.get('origQty', 'N/A')}",
        f"  Price:           {response.get('price', 'Market Price')}",
        f"  Executed Qty:    {response.get('executedQty', '0')}",
        f"  Avg Price:       {response.get('avgPrice', 'Pending')}",
        f"  Commission:      {response.get('commission', 'N/A')}",
        f"  Commission Asset: {response.get('commissionAsset', 'N/A')}",
        f"  Time in Force:   {response.get('timeInForce', 'N/A')}",
        f"  Timestamp:       {response.get('updateTime', 'N/A')}",
        "="*60 + "\n",
    ]
    return "\n".join(lines)


def place_market_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float
) -> Dict[str, Any]:
    """
    Place a market order.
    
    Args:
        client: BinanceFuturesClient instance
        symbol: Trading pair
        side: BUY or SELL
        quantity: Order quantity
        
    Returns:
        Order response
        
    Raises:
        OrderPlacementError: If order placement fails
    """
    try:
        logger.info(f"Placing MARKET {side} order: {quantity} {symbol}")
        response = client.place_order(
            symbol=symbol,
            side=side,
            type_="MARKET",
            quantity=quantity
        )
        logger.info(format_order_response(response))
        return response
    except (BinanceAPIError, BinanceNetworkError) as e:
        error_msg = f"Failed to place MARKET order: {str(e)}"
        error_logger.error(error_msg)
        logger.error(error_msg)
        raise OrderPlacementError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected error placing MARKET order: {str(e)}"
        error_logger.error(error_msg)
        logger.error(error_msg)
        raise OrderPlacementError(error_msg) from e


def place_limit_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    time_in_force: str = "GTC"
) -> Dict[str, Any]:
    """
    Place a limit order.
    
    Args:
        client: BinanceFuturesClient instance
        symbol: Trading pair
        side: BUY or SELL
        quantity: Order quantity
        price: Limit price
        time_in_force: GTC (Good-Til-Canceled), IOC, or FOK
        
    Returns:
        Order response
        
    Raises:
        OrderPlacementError: If order placement fails
    """
    try:
        logger.info(f"Placing LIMIT {side} order: {quantity} {symbol} @ {price}")
        response = client.place_order(
            symbol=symbol,
            side=side,
            type_="LIMIT",
            quantity=quantity,
            price=price,
            time_in_force=time_in_force
        )
        logger.info(format_order_response(response))
        return response
    except (BinanceAPIError, BinanceNetworkError) as e:
        error_msg = f"Failed to place LIMIT order: {str(e)}"
        error_logger.error(error_msg)
        logger.error(error_msg)
        raise OrderPlacementError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected error placing LIMIT order: {str(e)}"
        error_logger.error(error_msg)
        logger.error(error_msg)
        raise OrderPlacementError(error_msg) from e


def place_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
) -> Dict[str, Any]:
    """
    Place an order (main entry point).
    
    Args:
        client: BinanceFuturesClient instance
        symbol: Trading pair
        side: BUY or SELL
        order_type: MARKET or LIMIT
        quantity: Order quantity
        price: Price (required for LIMIT)
        
    Returns:
        Order response
        
    Raises:
        OrderPlacementError: If order placement fails
    """
    if order_type == "MARKET":
        return place_market_order(client, symbol, side, quantity)
    elif order_type == "LIMIT":
        if price is None:
            raise OrderPlacementError("Price required for LIMIT orders")
        return place_limit_order(client, symbol, side, quantity, price)
    else:
        raise OrderPlacementError(f"Unknown order type: {order_type}")
