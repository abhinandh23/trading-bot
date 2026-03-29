# Binance Futures Testnet Setup Guide

A step-by-step guide to register for Binance Futures Testnet and generate API credentials.

## Step 1: Access Binance Futures Testnet

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com) in your browser
2. You'll see the Binance Futures Testnet login page
3. You can either:
   - **Sign in with your existing Binance account** (recommended)
   - **Create a new account** for testnet (email-based account)

## Step 2: Sign In or Register

### Option A: Using Your Binance Account

```
1. Click "Sign In" 
2. Enter your Binance email and password
3. Complete 2FA if enabled
4. You'll be redirected to the testnet dashboard
```

### Option B: Create a New Testnet Account

```
1. Click "Register"
2. Enter an email address
3. Create a password
4. Confirm email verification
5. Login with new credentials
```

**Note**: Testnet accounts are separate from live Binance accounts. Use testnet-only credentials.

## Step 3: Verify Testnet Account

After login, you should see:
- Testnet balance (usually 10,000 USDT by default)
- Portfolio overview
- Market data with testnet prices

## Step 4: Generate API Credentials

### Navigate to API Management

1. **Click your account icon** in the top-right corner
2. **Select "Account"** or look for user settings
3. **Find "API Management"** or **"API"** section
4. You might be asked to enable API access via email verification

### Create API Key

1. **Click "Create New Key"** or **"+ Generate API Key"**
2. **Choose authentication type**:
   - Usually uses HMAC SHA256 (most secure for our use case)
3. **Accept the API key terms**
4. **Click "Create"**

### Your API Key Will Look Like

```
API Key:    vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgMQWCIPvlanmIZJS7hucDA
Secret Key: NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7h5hhGQ
```

⚠️ **IMPORTANT**: Save these securely! You won't be able to view the secret key again.

## Step 5: Configure API Permissions

In the API Management section, set the following permissions:

### Required Permissions

- ✅ **Enable Futures Trading** — Allows placing orders on Futures
- ✅ **Enable Reading Account Data** — Allows checking balance and orders

### Optional (for security)

- 🔒 **IP Whitelist** — Restrict API calls to specific IPs
  - Leave empty if unsure (allows all IPs, testnet is not critical)
- ⏰ **Expiration** — Set expiration date (e.g., 90 days)

## Step 6: Set Environment Variables

Once you have your API Key and Secret Key, add them to your system:

### On Windows (PowerShell)

```powershell
$env:BINANCE_API_KEY = "vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgMQWCIPvlanmIZJS7hucDA"
$env:BINANCE_API_SECRET = "NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7h5hhGQ"
```

### On Windows (Command Prompt)

```cmd
set BINANCE_API_KEY=vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgMQWCIPvlanmIZJS7hucDA
set BINANCE_API_SECRET=NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7h5hhGQ
```

### On macOS/Linux

```bash
export BINANCE_API_KEY="vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgMQWCIPvlanmIZJS7hucDA"
export BINANCE_API_SECRET="NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7h5hhGQ"
```

### Or Create .env File

Create a `.env` file in the `trading_bot/` directory:

```
BINANCE_API_KEY=vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgMQWCIPvlanmIZJS7hucDA
BINANCE_API_SECRET=NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7h5hhGQ
```

Then load before running:

```bash
# macOS/Linux
set -a && source .env && set +a

# PowerShell
Get-Content .env | ForEach-Object { if ($_ -match '(.+?)=(.+)') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) } }
```

## Step 7: Verify API Connection

Run a quick test to verify everything works:

```bash
python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.001
```

Expected output:
```
✓ Order placed successfully!
  Order ID: 1234567890
  Status: FILLED
```

## Step 8: Check Testnet Balance

Log in to https://testnet.binancefuture.com and verify:

- ✅ Your account shows the new order
- ✅ Testnet balance has decreased by the order amount
- ✅ Order status is visible in "Order History"

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **API key not found** | Check environment variables are set: `echo $BINANCE_API_KEY` |
| **Invalid API credentials** | Generate new credentials and verify you're using testnet, not live |
| **Order fails with "Symbol not found"** | Check symbol is correct (e.g., BTCUSDT). Use https://testnet.binancefuture.com to see available symbols |
| **Insufficient balance** | Testnet accounts get 10,000 USDT. Check your balance on the testnet website |
| **API signature invalid** | Ensure API_SECRET is exactly correct (no extra spaces) |

## Common Trading Pairs on Testnet

These symbols should be available to trade:

- `BTCUSDT` — Bitcoin
- `ETHUSDT` — Ethereum
- `BNBUSDT` — Binance Coin
- `XRPUSDT` — Ripple
- `ADAUSDT` — Cardano
- `DOGEUSDT` — Dogecoin
- `LTCUSDT` — Litecoin
- `TRXUSDT` — TRON

Try starting with `BTCUSDT` as it's the most liquid.

## Important Notes

⚠️ **Testnet Only**

- Testnet balances, prices, and orders are completely separate from live trading
- Testnet has different prices and behavior than the real market
- Testnet data resets periodically
- **NEVER use live API keys for this bot**

## Next Steps

1. ✅ Testnet account created
2. ✅ API credentials generated
3. ✅ Environment variables set
4. **→ Install the trading bot** (see [README.md](README.md))
5. **→ Run your first order!**

For more help, visit [Binance Futures Testnet](https://testnet.binancefuture.com) or check [Binance API Docs](https://binance-docs.github.io/apidocs/).
