import os
from dotenv import load_dotenv

class APIVault:
    """
    Security Vault: Securely loads and manages API credentials.
    """
    def __init__(self):
        load_dotenv()
        self.broker = os.getenv("BROKER_NAME", "PAPER")

    def get_shoonya_credentials(self) -> dict:
        return {
            "user_id": os.getenv("SHOONYA_USER_ID"),
            "password": os.getenv("SHOONYA_PASSWORD"),
            "twofa": os.getenv("SHOONYA_TWOFA_KEY"),
            "vendor_code": os.getenv("SHOONYA_API_KEY"),
            "imei": os.getenv("SHOONYA_IMEI")
        }

    def get_angel_credentials(self) -> dict:
        return {
            "api_key": os.getenv("ANGEL_API_KEY"),
            "client_id": os.getenv("ANGEL_CLIENT_ID"),
            "password": os.getenv("ANGEL_PASSWORD"),
            "totp_key": os.getenv("ANGEL_TOTP_KEY")
        }
