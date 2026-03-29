"""Input validators for the trading bot."""

import logging

logger = logging.getLogger("trading_bot.validators")


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Validate trading pair symbol.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        
    Returns:
        Validated symbol in uppercase
        
    Raises:
        ValidationError: If symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string")
    
    symbol = symbol.strip().upper()
    
    # Basic pattern check: must be alphanumeric
    if not symbol.isalnum():
        raise ValidationError("Symbol must contain only alphanumeric characters")
    
    if len(symbol) < 6:
        raise ValidationError("Symbol must be at least 6 characters (e.g., BTCUSDT)")
    
    logger.debug(f"Symbol '{symbol}' validated successfully")
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side (BUY or SELL).
    
    Args:
        side: Order side
        
    Returns:
        Validated side in uppercase
        
    Raises:
        ValidationError: If side is invalid
    """
    if not side or not isinstance(side, str):
        raise ValidationError("Side must be a non-empty string")
    
    side = side.strip().upper()
    
    if side not in ["BUY", "SELL"]:
        raise ValidationError("Side must be 'BUY' or 'SELL'")
    
    logger.debug(f"Side '{side}' validated successfully")
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type.
    
    Args:
        order_type: Order type (MARKET or LIMIT)
        
    Returns:
        Validated order type in uppercase
        
    Raises:
        ValidationError: If order type is invalid
    """
    if not order_type or not isinstance(order_type, str):
        raise ValidationError("Order type must be a non-empty string")
    
    order_type = order_type.strip().upper()
    
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValidationError("Order type must be 'MARKET' or 'LIMIT'")
    
    logger.debug(f"Order type '{order_type}' validated successfully")
    return order_type


def validate_quantity(quantity: str) -> float:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity as string or number
        
    Returns:
        Validated quantity as float
        
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError("Quantity must be a valid number")
    
    if qty <= 0:
        raise ValidationError("Quantity must be greater than 0")
    
    logger.debug(f"Quantity '{qty}' validated successfully")
    return qty


def validate_price(price: str) -> float:
    """
    Validate order price.
    
    Args:
        price: Order price as string or number
        
    Returns:
        Validated price as float
        
    Raises:
        ValidationError: If price is invalid
    """
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValidationError("Price must be a valid number")
    
    if p <= 0:
        raise ValidationError("Price must be greater than 0")
    
    logger.debug(f"Price '{p}' validated successfully")
    return p
