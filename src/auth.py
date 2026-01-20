import os
from dotenv import load_dotenv
from kalshi_python import Configuration, KalshiClient

load_dotenv()

def get_kalshi_credentials():
    key_id = os.getenv("KALSHI_KEY_ID")
    private_key_path = "secrets/kalshi_private.pem"
    
    # Clean the Key ID (remove accidental quotes or spaces)
    if key_id:
        key_id = key_id.strip().strip('"').strip("'")
        
    if not key_id:
        raise ValueError("KALSHI_KEY_ID not found in env")
    
    if not os.path.exists(private_key_path):
        raise FileNotFoundError(f"Private key file not found at {private_key_path}")
        
    with open(private_key_path, "r") as f:
        private_key = f.read()
        
    # STRICT CLEANING for the Private Key
    private_key = private_key.strip()
        
    return key_id, private_key

def get_demo_client():
    # 1. Get credentials
    key_id, private_key = get_kalshi_credentials()
    
    # 2. Create the Configuration object INSIDE this function
    # This ensures 'config' always exists when this function runs.
    config = Configuration(
        host="https://api.elections.kalshi.com/trade-api/v2"
    )
    
    # 3. Manually assign the keys
    config.api_key_id = key_id
    config.private_key_pem = private_key
    
    # 4. Create and return the client
    try:
        client = KalshiClient(config)
        return client
    except Exception as e:
        print(f"Failed to create client: {e}")
        return None

def get_current_balance():
    # We need to create a client instance to call this
    client = get_demo_client()
    if client:
        try:
            balance_response = client.get_balance()
            print(f"Balance: ${balance_response.balance / 100:.2f}")
        except Exception as e:
            print(f"Error getting balance: {e}")
    
if __name__ == "__main__":
    # This block only runs when you run 'python src/auth.py'
    # It's just for testing the file itself.
    client = get_demo_client()
    if client:
        print("Connected to Client (Test Run)")
        get_current_balance()