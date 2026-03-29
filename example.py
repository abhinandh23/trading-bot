
import os
from bot.client import BinanceFuturesClient
from bot.orders import place_order
from bot.logging_config import api_logger, trade_logger

# Load API credentials from environment
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

if not api_key or not api_secret:
    print("ERROR: Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables")
    exit(1)

# Initialize client
client = BinanceFuturesClient(api_key, api_secret)

print("\n" + "="*60)
print("Example 1: Place a Market Order")
print("="*60)

try:
    response = place_order(
        client=client,
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity=0.001,
    )
    print(f"✓ Market order placed! Order ID: {response['orderId']}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("Example 2: Place a Limit Order")
print("="*60)

try:
    response = place_order(
        client=client,
        symbol="ETHUSDT",
        side="SELL",
        order_type="LIMIT",
        quantity=1.0,
        price=2000.0,
    )
    print(f"✓ Limit order placed! Order ID: {response['orderId']}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("Example 3: Get Account Balance")
print("="*60)

try:
    account = client.get_account_balance()
    print(f"✓ Account fetched!")
    print(f"  Total wallet balance: {account.get('totalWalletBalance', 'N/A')} USDT")
    print(f"  Total unrealized profit: {account.get('totalUnrealizedProfit', 'N/A')} USDT")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("Example 4: Get Open Orders")
print("="*60)

try:
    orders = client.get_open_orders(symbol="BTCUSDT")
    print(f"✓ Open orders fetched!")
    if orders:
        for order in orders:
            print(f"  - Order {order['orderId']}: {order['side']} {order['origQty']} @ {order['price']}")
    else:
        print("  No open orders for BTCUSDT")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("All examples completed. Check logs/ for details.")
print("="*60 + "\n")
