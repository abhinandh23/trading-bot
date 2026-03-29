# Binance Futures Testnet Trading Bot

A Python application for placing orders on Binance Futures Testnet (USDT-M) with clean structure, comprehensive logging, and robust error handling.

## Features

✓ **Market and Limit Orders** — Place both order types on Binance Futures Testnet  
✓ **BUY/SELL Support** — Trade both sides  
✓ **CLI Interface** — Easy-to-use command-line interface with validation  
✓ **Structured Code** — Separate API client, order logic, and validators  
✓ **Comprehensive Logging** — Detailed logs for API requests, trades, and errors  
✓ **Error Handling** — Validates input and handles network/API failures gracefully  

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance Futures API client wrapper
│   ├── orders.py                # Order placement logic
│   ├── validators.py            # Input validation functions
│   └── logging_config.py         # Logging configuration
├── cli.py                        # CLI entry point
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── logs/                         # Log files (created on first run)
    ├── api_requests.log          # API requests and responses
    ├── trades.log                # Trade execution logs
    └── errors.log                # Error logs
```

## Setup Instructions

### 1. Register for Binance Futures Testnet

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Create an account or sign in with your Binance account
3. Complete any required verification steps
4. Access the testnet dashboard

### 2. Generate API Credentials

1. Go to Account → API Management (or similar option)
2. Create a new API Key
3. Configure permissions:
   - Enable Futures trading
   - Enable order placement
   - (Optional) Restrict to your IP address
4. Note your **API Key** and **Secret Key**

### 3. Install Dependencies

```bash
# Navigate to the project directory
cd trading_bot

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Set Environment Variables

Set your API credentials as environment variables:

**On Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY = "your_api_key_here"
$env:BINANCE_API_SECRET = "your_api_secret_here"
```

**On Windows (Command Prompt):**
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here
```

**On macOS/Linux:**
```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

**Alternatively, create a `.env` file** in the project root:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

Then load it before running:
```bash
# On macOS/Linux:
set -a && source .env && set +a

# On Windows PowerShell:
if (Test-Path .env) { Get-Content .env | ForEach-Object { $key, $value = $_ -split '='; [Environment]::SetEnvironmentVariable($key, $value) } }
```

## Usage

### Basic Command Format

```bash
python cli.py --symbol SYMBOL --side SIDE --type ORDER_TYPE --quantity QTY [--price PRICE]
```

### Parameters

| Parameter | Required | Values | Example |
|-----------|----------|--------|---------|
| `--symbol` / `-s` | Yes | Trading pair | `BTCUSDT`, `ETHUSDT` |
| `--side` / `-S` | Yes | `BUY` or `SELL` | `BUY` |
| `--type` / `-t` | Yes | `MARKET` or `LIMIT` | `MARKET` |
| `--quantity` / `-q` | Yes | Positive number | `1`, `0.5` |
| `--price` / `-p` | No* | Positive number | `45000` |

*Required for LIMIT orders, optional for MARKET orders

### Examples

#### 1. Place a Market Order (BUY)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Expected output:
```
============================================================
BINANCE FUTURES TESTNET TRADING BOT
============================================================
Base URL: https://testnet.binancefuture.com
============================================================

ORDER REQUEST SUMMARY
------------------------------------------------------------
  Symbol:       BTCUSDT
  Side:         BUY
  Order Type:   MARKET
  Quantity:     0.001
  Price:        Market Price
------------------------------------------------------------

✓ Order placed successfully!
  Order ID: 123456789
  Status: FILLED

============================================================
ORDER PLACED SUCCESSFULLY
============================================================
  Order ID:        123456789
  ...
```

#### 2. Place a Limit Order (SELL)

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 1 --price 2000
```

Expected output shows order with status `NEW` or `PARTIALLY_FILLED`.

#### 3. Short Form with Abbreviations

```bash
python cli.py -s BNBUSDT -S BUY -t LIMIT -q 10 -p 300
```

### Input Validation

The bot validates all inputs:

- **Symbol**: Must be alphanumeric, at least 6 characters (e.g., `BTCUSDT`)
- **Side**: Must be `BUY` or `SELL` (case-insensitive)
- **Type**: Must be `MARKET` or `LIMIT` (case-insensitive)
- **Quantity**: Must be a positive number
- **Price**: Must be a positive number (required for LIMIT orders)

Invalid input example:
```bash
python cli.py -s BTC -S INVALID -t MARKET -q -1

# Output:
# ERROR: Symbol must be at least 6 characters (e.g., BTCUSDT)
```

## Logging

The bot creates three log files in the `logs/` directory:

### 1. `api_requests.log`
Detailed logs of all API interactions:
```
2026-03-28 14:23:45 - trading_bot.api - INFO - funcName:125 - BinanceFuturesClient initialized (Testnet)
2026-03-28 14:23:46 - trading_bot.api - DEBUG - funcName:156 - POST /fapi/v1/order | Params: {...}
2026-03-28 14:23:47 - trading_bot.api - DEBUG - funcName:165 - Response status: 200
2026-03-28 14:23:47 - trading_bot.api - DEBUG - funcName:169 - Response: {'orderId': 123456789, ...}
```

### 2. `trades.log`
Trade execution records:
```
2026-03-28 14:23:46 - trading_bot.trade - INFO - Order placed successfully! Order ID: 123456789
2026-03-28 14:23:46 - trading_bot.trade - INFO - Order details: {...}
```

### 3. `errors.log`
Error records for debugging:
```
2026-03-28 14:24:01 - trading_bot.error - ERROR - Failed to place order: API Error: Insufficient balance
```

## Error Handling

The bot handles the following error scenarios:

| Error | Cause | Response |
|-------|-------|----------|
| **ValidationError** | Invalid input (symbol, side, etc.) | Exit with error message |
| **BinanceAPIError** | API returns error (invalid parameters, insufficient funds, etc.) | Log error and exit |
| **BinanceNetworkError** | Network timeout or connection failure | Log error and exit |
| **OrderPlacementError** | Order placement failed | Log detailed error |
| **Missing API Credentials** | `BINANCE_API_KEY` or `BINANCE_API_SECRET` not set | Exit with helpful message |

## Testing

### Test on Binance Futures Testnet

Since this is a testnet, all orders use fake/test funds. Here's how to verify it works:

1. **Log in to Binance Futures Testnet** at https://testnet.binancefuture.com
2. **Check your testnet balance** — You should have test USDT
3. **Run a market order**:
   ```bash
   python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.001
   ```
4. **Check the order** in your testnet account under "Orders" or "Order History"
5. **Review logs** in `logs/trades.log` and `logs/api_requests.log`

### Example Log Output

After running a few orders, your `logs/trades.log` should show:

```
2026-03-28 14:23:46 - trading_bot.trade - INFO - Placing MARKET BUY order: 0.001 BTCUSDT
2026-03-28 14:23:47 - trading_bot.trade - INFO - 
============================================================
ORDER PLACED SUCCESSFULLY
============================================================
  Order ID:        1234567890
  Symbol:          BTCUSDT
  Side:            BUY
  Order Type:      MARKET
  Status:          FILLED
  Quantity:        0.001
  Price:           Market Price
  Executed Qty:    0.001
  Avg Price:       45000.50
...
2026-03-28 14:28:32 - trading_bot.trade - INFO - Placing LIMIT SELL order: 1.0 ETHUSDT @ 2000.0
2026-03-28 14:28:33 - trading_bot.trade - INFO - 
============================================================
ORDER PLACED SUCCESSFULLY
============================================================
  Order ID:        1234567891
  Symbol:          ETHUSDT
  Side:            SELL
  Order Type:      LIMIT
  Status:          NEW
...
```

## Assumptions

1. **Python 3.6+** — Uses standard requests library and string formatting
2. **Binance Testnet Only** — Explicitly uses testnet URL: `https://testnet.binancefuture.com`
3. **USDT-M Futures** — Configured for USDT Margin futures (not regular spot or coin-M)
4. **Valid API Credentials** — Assumes credentials are correct and have appropriate permissions
5. **Testnet-Only Disclaimer** — NOT intended for live trading; testnet is for testing only
6. **Network Connectivity** — Assumes internet connectivity to reach Binance API
7. **Order Validation** — Basic validation; Binance will validate precision, tick size, etc.

## Common Issues & Troubleshooting

### Issue: `ERROR: API credentials not found`

**Solution**: Make sure environment variables are set:
```bash
# Check if variables are set:
echo $BINANCE_API_KEY  # macOS/Linux
echo %BINANCE_API_KEY%  # Windows (Command Prompt)
$env:BINANCE_API_KEY  # Windows (PowerShell)
```

### Issue: `BinanceAPIError: API Error: 400: Invalid symbol`

**Solution**: Symbol must be valid and correctly formatted:
- Valid: `BTCUSDT`, `ETHUSDT`, `BNBUSDT`
- Invalid: `BTC`, `USDT-BTC`, `btcusdt` (case doesn't matter, but format does)

### Issue: `OrderPlacementError: Failed to place order: Insufficient balance`

**Solution**: Make sure your testnet account has sufficient balance. Log in to https://testnet.binancefuture.com and check your account balance.

### Issue: Connection timeout

**Solution**: Check your internet connection and firewall. If the issue persists, try:
1. Increase timeout: Modify `BinanceFuturesClient(timeout=20)` in `cli.py`
2. Check Binance API status at https://status.binance.com

## API Reference

### BinanceFuturesClient

```python
from bot.client import BinanceFuturesClient

client = BinanceFuturesClient(api_key, api_secret)

# Place order
response = client.place_order(
    symbol="BTCUSDT",
    side="BUY",
    type_="MARKET",
    quantity=0.001
)

# Get account info
account = client.get_account_balance()

# Get open orders
orders = client.get_open_orders(symbol="BTCUSDT")

# Cancel order
client.cancel_order(symbol="BTCUSDT", order_id=123456789)
```

### Order Functions

```python
from bot.orders import place_order, place_market_order, place_limit_order

# Main order placement
response = place_order(
    client=client,
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity=0.001
)

# Or use specific functions
response = place_market_order(client, "BTCUSDT", "BUY", 0.001)
response = place_limit_order(client, "BTCUSDT", "SELL", 1, 45000)
```

## License

MIT License — Feel free to modify and use for personal/educational purposes.

## Support

For issues:
1. Check logs in `logs/` directory
2. Review the "Troubleshooting" section above
3. Verify API credentials and network connectivity
4. Check Binance API documentation: https://binance-docs.github.io/apidocs/

## Next Steps (Bonus Features)

To extend this bot, consider:
1. **Stop-Limit Orders** — Add `type_="STOP_LOSS_LIMIT"` support
2. **OCO Orders** — One-Cancels-Other orders
3. **TWAP Orders** — Time-Weighted Average Price execution
4. **Grid Trading** — Automated grid-based orders
5. **Web UI** — Flask/Streamlit dashboard
6. **Real-time Updates** — WebSocket for live price/order updates
7. **Backtesting** — Historical data analysis
8. **Alerts** — Email/Slack notifications for order fills
