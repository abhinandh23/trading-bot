# Development Guide

Information for developers who want to understand or extend the trading bot.

## Project Structure Overview

```
trading_bot/
├── bot/                          # Main package
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance API client (low-level API calls)
│   ├── orders.py                # Order placement logic (high-level order functions)
│   ├── validators.py            # Input validation
│   └── logging_config.py         # Logging setup
├── cli.py                        # Command-line interface (main entry point)
├── example.py                    # Example usage (programmatic)
├── bonus_orders.py              # Bonus: Stop-Limit and OCO orders
├── requirements.txt              # Dependencies
├── pyproject.toml               # Alternative package config
├── README.md                     # User documentation
├── SETUP_GUIDE.md               # Setup instructions
├── DEVELOPMENT.md               # This file
└── logs/                         # Log files (created at runtime)
    ├── api_requests.log
    ├── trades.log
    └── errors.log
```

## Module Responsibilities

### `bot/client.py` — Binance API Wrapper

**Responsibility**: Low-level HTTP communication with Binance API

**Key Classes**:
- `BinanceFuturesClient` — Main API client
  - `place_order()` — Place orders
  - `cancel_order()` — Cancel orders
  - `get_open_orders()` — Fetch open orders
  - `get_account_balance()` — Fetch account info
  
**Key Methods**:
- `_request()` — Generic HTTP request handler
- `_generate_signature()` — HMAC-SHA256 signing
- `_build_headers()` — API key headers

**Exceptions**:
- `BinanceAPIError` — API returns error
- `BinanceNetworkError` — Network/connection issues

**Example**:
```python
from bot.client import BinanceFuturesClient

client = BinanceFuturesClient(api_key, api_secret)
response = client.place_order("BTCUSDT", "BUY", "MARKET", 0.001)
```

### `bot/orders.py` — Order Placement Logic

**Responsibility**: High-level order placement with logging and error handling

**Key Functions**:
- `place_order()` — Main entry point
- `place_market_order()` — Market order specifics
- `place_limit_order()` — Limit order specifics
- `format_order_response()` — Pretty-print order responses

**Exceptions**:
- `OrderPlacementError` — Order placement failed

**Example**:
```python
from bot.orders import place_order

response = place_order(client, "BTCUSDT", "BUY", "MARKET", 0.001)
```

### `bot/validators.py` — Input Validation

**Responsibility**: Validate user input before API calls

**Functions**:
- `validate_symbol()` — Check trading pair format
- `validate_side()` — Check BUY/SELL
- `validate_order_type()` — Check MARKET/LIMIT
- `validate_quantity()` — Check positive number
- `validate_price()` — Check positive number

**Exception**:
- `ValidationError` — Validation failed

**Example**:
```python
from bot.validators import validate_symbol, ValidationError

try:
    symbol = validate_symbol("BTCUSDT")
except ValidationError as e:
    print(f"Invalid: {e}")
```

### `bot/logging_config.py` — Logging Configuration

**Responsibility**: Set up loggers for API, trades, and errors

**Loggers**:
- `trading_bot.api` — API requests/responses
- `trading_bot.trade` — Trade execution
- `trading_bot.error` — Errors

**Log Files**:
- `logs/api_requests.log` — Detailed API logs
- `logs/trades.log` — Trade records  
- `logs/errors.log` — Error stack traces

**Features**:
- Rotating file handlers (max 5 MB per file)
- Console output for important messages
- Timestamps and function names in logs

**Example**:
```python
from bot.logging_config import api_logger, trade_logger, error_logger

api_logger.info("Making API call")
trade_logger.info("Order placed")
error_logger.error("Something went wrong")
```

### `cli.py` — Command-Line Interface

**Responsibility**: Parse CLI arguments and orchestrate order placement

**Key Functions**:
- `main()` — Entry point
- `load_api_credentials()` — Load from environment
- `print_header()` — Display banner
- `print_order_summary()` — Show order details

**Example**:
```bash
python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.001
```

## Code Flow Diagrams

### CLI Order Placement Flow

```
cli.py main()
  ↓
[Parse arguments]
  ↓
[Validate inputs] → validators.py
  ↓
[Load API credentials] → os.getenv()
  ↓
[Create client] → BinanceFuturesClient()
  ↓
[Place order] → orders.place_order()
  ↓
  ├→ orders.place_market_order()
  │   ↓
  │   client.place_order(type_="MARKET")
  │
  └→ orders.place_limit_order()
      ↓
      client.place_order(type_="LIMIT")
  ↓
[Log response] → logging_config.trade_logger
  ↓
[Print success/error] → stdout
```

### API Request Flow

```
client.place_order()
  ↓
[Build parameters]
  ↓
client._request(method="POST", endpoint="/fapi/v1/order")
  ↓
[Build headers] → _build_headers()
  ↓
[Add timestamp]
  ↓
[Generate signature] → _generate_signature()
  ↓
[Make HTTP request] → requests.Session()
  ↓
[Log request] → logging_config.api_logger
  ↓
[Parse JSON response]
  ↓
[Log response] → logging_config.api_logger
  ↓
[Check status code]
  ├→ 200: Return JSON
  └→ !200: Raise BinanceAPIError
```

## Adding New Features

### Add a New Order Type

1. **Add validation** in `validators.py`:
```python
def validate_new_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in ["MARKET", "LIMIT", "NEW_TYPE"]:
        raise ValidationError(...)
    return order_type
```

2. **Add placement function** in `orders.py`:
```python
def place_new_order_type(client, symbol, side, quantity, **kwargs):
    logger.info(f"Placing NEW_TYPE order...")
    response = client.place_order(
        symbol=symbol,
        side=side,
        type_="NEW_TYPE",
        quantity=quantity,
        # ... extra parameters
    )
    return response
```

3. **Update CLI** in `cli.py`:
```python
parser.add_argument("-t", "--type", choices=["MARKET", "LIMIT", "NEW_TYPE"])
# ... then in main():
if args.order_type == "NEW_TYPE":
    response = place_new_order_type(client, symbol, side, quantity)
```

### Add API Endpoints

1. **Add method** to `BinanceFuturesClient` in `client.py`:
```python
def new_endpoint_function(self, param: str):
    logger.info(f"Calling new endpoint with {param}")
    return self._request("GET", "/fapi/v1/new_endpoint", 
                        params={"param": param}, signed=True)
```

2. **Use in CLI or orders.py**:
```python
result = client.new_endpoint_function(some_value)
```

### Add Error Handling

Add custom exception in relevant module:
```python
class NewSpecificError(Exception):
    """Raised when specific error occurs."""
    pass
```

Then catch it:
```python
try:
    # some code
except NewSpecificError as e:
    error_logger.error(f"Details: {e}")
    raise
```

## Testing (Manual)

### Unit Test Example

```python
# test_validators.py
from bot.validators import validate_symbol, ValidationError

def test_validate_symbol():
    assert validate_symbol("BTCUSDT") == "BTCUSDT"
    assert validate_symbol("btcusdt") == "BTCUSDT"
    
    try:
        validate_symbol("BTC")
        assert False, "Should raise ValidationError"
    except ValidationError:
        pass
```

Run with pytest:
```bash
pip install pytest
pytest test_validators.py
```

### Integration Test

```python
# test_client.py
import os
from bot.client import BinanceFuturesClient

def test_client_initialization():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    client = BinanceFuturesClient(api_key, api_secret)
    account = client.get_account_balance()
    
    assert account is not None
    assert "totalWalletBalance" in account
```

## Performance Considerations

### Logging Impact

- **RotatingFileHandler** prevents log files from growing indefinitely
- **Separate loggers** allow filtering messages by component
- **Console output** reduced to INFO level to avoid noise

To improve performance:
- Increase timeout in `BinanceFuturesClient(timeout=20)`
- Add caching for slow API calls

### Network Optimization

- **Connection reuse** via `requests.Session()`
- **Signature generation** is very fast (HMAC-SHA256)
- **API rate limits** — Binance has rate limits; respect them!

Typical order placement: **50-500ms**

## Security Considerations

⚠️ **CRITICAL**

1. **Never hardcode API keys** — Use environment variables
2. **Never commit `.env` files** — .gitignore them
3. **Testnet only** — Never use live credentials for testing
4. **Validate all input** — Always use validators
5. **Log responsibly** — Never log full API responses with sensitive data
6. **Keep dependencies updated** — `pip install --upgrade requests`

### API Key Permissions

Minimum required:
- ✅ Futures Trading
- ✅ Read Account Data

Not needed:
- ✗ Withdraw (testnet doesn't allow)
- ✗ Deposit
- ✗ Spot Trading (unless trading spot)

## Debugging

### Enable Debug Logging

```python
import logging
logging.getLogger("trading_bot").setLevel(logging.DEBUG)
```

### Check Logs

```bash
# Watch trades in real-time
tail -f logs/trades.log

# Watch API calls
tail -f logs/api_requests.log

# Watch errors
tail -f logs/errors.log
```

### Print Variables

```python
from bot.logging_config import api_logger

api_logger.debug(f"Order params: {params}")
```

## Common Pitfalls

| Mistake | Impact | Solution |
|---------|--------|----------|
| Hardcoded API keys | Security breach | Use environment variables |
| No input validation | Invalid API calls | Use validators |
| Ignoring exceptions | Silent failures | Add try-except blocks |
| Too much logging | Performance hit | Use appropriate log levels |
| Typos in symbol | API errors | Validate before placing |
| Forgetting signature | 401 Unauthorized | Check `_generate_signature()` |

## Dependencies

- **requests** — HTTP library for API calls
- **Standard library** — logging, argparse, hashlib, hmac, time

No external trading libraries required! This makes it lightweight and flexible.

## Future Enhancements

See [README.md](README.md) "Next Steps (Bonus Features)" section for ideas:

1. Stop-Limit/OCO orders (partially implemented in `bonus_orders.py`)
2. TWAP (Time-Weighted Average Price) execution
3. Grid trading strategies
4. WebSocket for real-time updates
5. Backtesting framework
6. Web UI (Streamlit/Flask)
7. Trading alerts/notifications
8. Database logging

## Questions?

- Check [README.md](README.md) for usage
- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for setup
- Review docstrings in source code
- Check log files for detailed error messages
