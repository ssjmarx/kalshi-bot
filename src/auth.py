import os
from dotenv import load_dotenv
from kalshi_python import KalshiClient
from kalshi_python.configuration import Configuration

# Load environment variables at module level
load_dotenv()


class KalshiAuth:
    """Handles Kalshi API authentication and client initialization."""

    def __init__(self, key_id: str | None = None, private_key_path: str | None = None) -> None:
        """Initialize authentication using key ID and private key PEM file.

        Args:
            key_id: Kalshi API key ID (from .env: KALSHI_KEY_ID)
            private_key_path: Path to private key PEM file (default: secrets/kalshi_private.pem)
        """
        # Get credentials from parameters or environment
        self.key_id = key_id or os.getenv("KALSHI_KEY_ID")
        self.private_key_path = private_key_path or "secrets/kalshi_private.pem"

        # Validate credentials exist
        if not self.key_id:
            raise ValueError(
                "KALSHI_KEY_ID must be set in .env file or provided as parameter"
            )

        if not os.path.exists(self.private_key_path):
            raise FileNotFoundError(
                f"Private key file not found at: {self.private_key_path}"
            )

        # Read private key from PEM file
        with open(self.private_key_path, "r") as f:
            self.private_key = f.read()

        # Create Configuration object with credentials
        self.configuration = Configuration(
            host="https://demo-api.kalshi.co/trade-api/v2"  # Demo API URL v2
        )
        self.configuration.api_key_id = self.key_id
        self.configuration.private_key_pem = self.private_key

        # Initialize Kalshi client with configuration
        self.client = KalshiClient(self.configuration)

    def get_client(self) -> KalshiClient:
        """Return the authenticated Kalshi client.

        Returns:
            KalshiClient: Authenticated client for API calls
        """
        return self.client
