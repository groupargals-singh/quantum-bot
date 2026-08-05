import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

class BinanceLiveExchangeAPI:
    """Enterprise Binance REST API Client with HMAC-SHA256 Signature Security"""
    def __init__(self, testnet=True):
        self.api_key = os.environ.get("BINANCE_API_KEY", "")
        self.api_secret = os.environ.get("BINANCE_API_SECRET", "")
        # Testnet vs Mainnet Base URL
        self.base_url = "https://testnet.binance.vision" if testnet else "https://api.binance.com"
        self.testnet = testnet

    def _generate_signature(self, params):
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _send_signed_request(self, method, endpoint, params=None):
        if not self.api_key or not self.api_secret:
            print("⚠️ [LIVE API SECURITY WARNING] Missing BINANCE_API_KEY or BINANCE_API_SECRET!")
            return None

        if params is None:
            params = {}

        params['timestamp'] = int(time.time() * 1000)
        params['recvWindow'] = 5000  # 5-second replay attack protection window
        params['signature'] = self._generate_signature(params)

        headers = {
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, data=params, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, data=params, timeout=10)
            else:
                return None

            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ [BINANCE API ERROR {response.status_code}]: {response.text}")
                return None
        except Exception as e:
            print(f"❌ [NETWORK EXCEPTION]: {e}")
            return None

    def get_account_balance(self, asset="USDT"):
        """Fetch Real Spot Account Balance"""
        res = self._send_signed_request("GET", "/api/v3/account")
        if res and "balances" in res:
            for item in res["balances"]:
                if item["asset"] == asset:
                    return {
                        "free": float(item["free"]),
                        "locked": float(item["locked"]),
                        "total": float(item["free"]) + float(item["locked"])
                    }
        return {"free": 0.0, "locked": 0.0, "total": 0.0}

    def place_market_order(self, symbol, side, quantity):
        """Execute Real Signed Market Order (BUY / SELL)"""
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": "MARKET",
            "quantity": round(quantity, 5)
        }
        print(f"⚡ [REAL ORDER SENT] {side} {quantity} {symbol} via HMAC Signed API...")
        return self._send_signed_request("POST", "/api/v3/order", params)

    def cancel_order(self, symbol, order_id):
        """Cancel Active Order"""
        params = {
            "symbol": symbol.upper(),
            "orderId": order_id
        }
        return self._send_signed_request("DELETE", "/api/v3/order", params)

binance_live_api = BinanceLiveExchangeAPI(testnet=True)
