"""Binance API client wrapper for Futures trading."""

import hashlib
import hmac
import logging
import time
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger("trading_bot.api")


class BinanceAPIError(Exception):
    """Raised when Binance API returns an error."""
    pass


class BinanceNetworkError(Exception):
    """Raised when network communication fails."""
    pass


class BinanceFuturesClient:
    """
    Client for Binance Futures (USDT-M) Testnet trading.
    
    Uses the Testnet base URL: https://testnet.binancefuture.com
    """
    
    BASE_URL = "https://testnet.binancefuture.com"
    
    def __init__(self, api_key: str, api_secret: str, timeout: int = 10):
        """
        Initialize the Binance Futures client.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout
        self.session = requests.Session()
        
        logger.info("BinanceFuturesClient initialized (Testnet)")
    
    def _generate_signature(self, query_string: str) -> str:
        """
        Generate HMAC SHA256 signature for API request.
        
        Args:
            query_string: Query string to sign
            
        Returns:
            Signature string
        """
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _build_headers(self) -> Dict[str, str]:
        """Build request headers with API key."""
        return {
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        signed: bool = False
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to Binance API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Request parameters
            signed: Whether request should be signed
            
        Returns:
            JSON response from API
            
        Raises:
            BinanceNetworkError: If network communication fails
            BinanceAPIError: If API returns an error
        """
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        headers = self._build_headers()
        
        if signed:
            params["timestamp"] = int(time.time() * 1000)
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            params["signature"] = self._generate_signature(query_string)
        
        try:
            logger.debug(f"{method} {endpoint} | Params: {params}")
            
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            logger.debug(f"Response status: {response.status_code}")
            
            # Check for HTTP errors
            if response.status_code != 200:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    if "msg" in error_data:
                        error_msg += f": {error_data['msg']}"
                    logger.error(f"API Error: {error_msg} | Response: {error_data}")
                except:
                    logger.error(f"API Error: {error_msg} | Response: {response.text}")
                raise BinanceAPIError(error_msg)
            
            result = response.json()
            logger.debug(f"Response: {result}")
            return result
            
        except requests.exceptions.Timeout:
            msg = f"Request timeout ({self.timeout}s) for {endpoint}"
            logger.error(msg)
            raise BinanceNetworkError(msg)
        except requests.exceptions.ConnectionError as e:
            msg = f"Connection error: {str(e)}"
            logger.error(msg)
            raise BinanceNetworkError(msg)
        except requests.exceptions.RequestException as e:
            msg = f"Request error: {str(e)}"
            logger.error(msg)
            raise BinanceNetworkError(msg)
    
    def get_account_balance(self) -> Dict[str, Any]:
        """
        Get account balance and position information.
        
        Returns:
            Account data from API
        """
        logger.info("Fetching account balance...")
        return self._request("GET", "/fapi/v2/account", signed=True)
    
    def place_order(
        self,
        symbol: str,
        side: str,
        type_: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC"
    ) -> Dict[str, Any]:
        """
        Place an order on Binance Futures.
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            type_: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
            time_in_force: Time in force (GTC, IOC, FOK). Default GTC.
            
        Returns:
            Order response data
            
        Raises:
            BinanceAPIError: If order placement fails
        """
        params = {
            "symbol": symbol,
            "side": side,
            "type": type_,
            "quantity": quantity,
        }
        
        if type_ == "LIMIT":
            if price is None:
                raise ValueError("Price required for LIMIT orders")
            params["price"] = price
            params["timeInForce"] = time_in_force
        
        logger.info(
            f"Placing {type_} {side} order: {quantity} {symbol} @ {price or 'market price'}"
        )
        
        return self._request("POST", "/fapi/v1/order", params=params, signed=True)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an existing order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID to cancel
            
        Returns:
            Cancelled order data
        """
        params = {
            "symbol": symbol,
            "orderId": order_id,
        }
        logger.info(f"Cancelling order {order_id} for {symbol}")
        return self._request("DELETE", "/fapi/v1/order", params=params, signed=True)
    
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """
        Get list of open orders.
        
        Args:
            symbol: Optional trading pair to filter
            
        Returns:
            List of open orders
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        
        logger.info(f"Fetching open orders{' for ' + symbol if symbol else ''}...")
        return self._request("GET", "/fapi/v1/openOrders", params=params, signed=True)
    
    def get_exchange_info(self) -> Dict[str, Any]:
        """
        Get exchange trading rules and symbol information.
        
        Returns:
            Exchange info data
        """
        logger.info("Fetching exchange info...")
        return self._request("GET", "/fapi/v1/exchangeInfo")
