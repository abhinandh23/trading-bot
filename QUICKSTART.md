# Quick Start Guide

Get the trading bot running in **5 minutes**.

## Prerequisites

- Python 3.6 or later
- Binance Futures Testnet account (free)
- Binance Futures Testnet API credentials

## 1️⃣ Register on Testnet (1 min)

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Sign in with your Binance account (or create new testnet account)
3. You'll have 10,000 USDT testnet balance

👉 **Detailed steps?** See [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 2️⃣ Generate API Credentials (1 min)

1. Click account icon → **Account**
2. Find **API Management**
3. Click **Create API Key** → Select **HMAC SHA256**
4. Accept terms
5. You'll get:
   ```
   API Key:    vmPUZE6mv9SD5VN...
   Secret Key: NhqPtmdSJYdKjVHj...
   ```

⚠️ **Save these! You won't see the secret again.**

## 3️⃣ Set Environment Variables (1 min)

### Windows (PowerShell)

```powershell
$env:BINANCE_API_KEY = "your_api_key_here"
$env:BINANCE_API_SECRET = "your_secret_here"
```

### Windows (Command Prompt)

```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_secret_here
```

### macOS/Linux

```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_secret_here"
```

## 4️⃣ Install & Run (2 min)

```bash
# Navigate to project
cd trading_bot

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run your first order!
python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.001
```

## Expected Output

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
  Order ID: 1234567890
  Status: FILLED
```

## More Examples

```bash
# Buy 1 ETH at market price
python cli.py -s ETHUSDT -S BUY -t MARKET -q 1

# Sell 10 BNB at limit price of 300 USDT
python cli.py -s BNBUSDT -S SELL -t LIMIT -q 10 -p 300

# Buy 0.5 XRP at limit price of 0.50 USDT
python cli.py -s XRPUSDT -S BUY -t LIMIT -q 0.5 -p 0.50
```

## Check Your Orders

1. Log in to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Go to **Orders** or **Order History**
3. You should see your orders!

## Check Logs

After running orders, check logs in the `logs/` folder:

```
logs/
  ├── api_requests.log  — API calls and responses
  ├── trades.log        — Order execution details
  └── errors.log        — Any errors that occurred
```

View with:
```bash
# Windows
type logs\trades.log

# macOS/Linux
cat logs/trades.log

# Or tail (follow in real-time)
tail -f logs/trades.log
```

## 🎯 Next Steps

| What | File | Command |
|------|------|---------|
| **Learn more** | [README.md](README.md) | Read full documentation |
| **Setup details** | [SETUP_GUIDE.md](SETUP_GUIDE.md) | Detailed Binance setup |
| **Code details** | [DEVELOPMENT.md](DEVELOPMENT.md) | Understand the code |
| **Programmatic use** | [example.py](example.py) | Use as library, not CLI |

## ⚠️ Important Notes

- ✅ **Testnet only** — Uses fake USDT, no real money
- ✅ **Safe to test** — Reset any time at testnet.binancefuture.com
- ❌ **NOT for live trading** — Never use live API credentials here
- 🔒 **Keep credentials safe** — Never commit .env file

## Still Having Issues?

1. **Check environment variables**:
   ```bash
   echo $BINANCE_API_KEY  # macOS/Linux
   echo %BINANCE_API_KEY%  # Windows Command Prompt
   $env:BINANCE_API_KEY  # Windows PowerShell
   ```

2. **Check logs** in `logs/` folder

3. **Verify Binance status** at [https://status.binance.com](https://status.binance.com)

4. **Read troubleshooting** in [README.md](README.md#troubleshooting)

---

✅ **You're ready!** Go place your first order with:

```bash
python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.001
```
