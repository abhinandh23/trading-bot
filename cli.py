"""Command-line interface for the trading bot."""

import argparse
import os
import sys
from pathlib import Path

from bot.client import BinanceFuturesClient
from bot.logging_config import api_logger, trade_logger, error_logger
from bot.validators import ValidationError, validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.orders import place_order, OrderPlacementError


def load_api_credentials():
    """
    Load API credentials from environment variables.
    
    Returns:
        Tuple of (api_key, api_secret)
        
    Raises:
        ValueError: If credentials are not set
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        raise ValueError(
            "API credentials not found. Please set BINANCE_API_KEY and "
            "BINANCE_API_SECRET environment variables."
        )
    
    return api_key, api_secret


def print_header():
    """Print application header."""
    print("\n" + "="*60)
    print("BINANCE FUTURES TESTNET TRADING BOT")
    print("="*60)
    print("Base URL: https://testnet.binancefuture.com")
    print("="*60 + "\n")


def print_order_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
):
    """Print order summary before placement."""
    print("\nORDER REQUEST SUMMARY")
    print("-" * 60)
    print(f"  Symbol:       {symbol}")
    print(f"  Side:         {side}")
    print(f"  Order Type:   {order_type}")
    print(f"  Quantity:     {quantity}")
    if price:
        print(f"  Price:        {price}")
    else:
        print(f"  Price:        Market Price")
    print("-" * 60)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a market order to buy 1 BTC
  python cli.py -s BTCUSDT -S BUY -t MARKET -q 1

  # Place a limit order to sell 10 ETH at 2000 USDT
  python cli.py -s ETHUSDT -S SELL -t LIMIT -q 10 -p 2000
        """
    )
    
    parser.add_argument(
        "-s", "--symbol",
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
    )
    parser.add_argument(
        "-S", "--side",
        required=True,
        help="Order side: BUY or SELL"
    )
    parser.add_argument(
        "-t", "--type",
        required=True,
        dest="order_type",
        help="Order type: MARKET or LIMIT"
    )
    parser.add_argument(
        "-q", "--quantity",
        required=True,
        type=str,
        help="Order quantity"
    )
    parser.add_argument(
        "-p", "--price",
        type=str,
        default=None,
        help="Order price (required for LIMIT orders)"
    )
    
    args = parser.parse_args()
    
    print_header()
    
    # Validate inputs
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = None
        
        if order_type == "LIMIT":
            if not args.price:
                print("ERROR: Price is required for LIMIT orders")
                sys.exit(1)
            price = validate_price(args.price)
        elif order_type == "MARKET" and args.price:
            print("WARNING: Price is ignored for MARKET orders\n")
        
    except ValidationError as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)
    
    # Load API credentials
    try:
        api_key, api_secret = load_api_credentials()
    except ValueError as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)
    
    # Initialize client
    client = BinanceFuturesClient(api_key, api_secret)
    
    # Print order summary
    print_order_summary(symbol, side, order_type, quantity, price)
    
    # Place order
    try:
        response = place_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        print(f"\n✓ Order placed successfully!")
        print(f"  Order ID: {response.get('orderId', 'N/A')}")
        print(f"  Status: {response.get('status', 'N/A')}\n")
        
    except OrderPlacementError as e:
        print(f"\n✗ Order placement failed: {str(e)}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}\n")
        error_logger.exception("Unexpected error in main CLI")
        sys.exit(1)


if __name__ == "__main__":
    main()
