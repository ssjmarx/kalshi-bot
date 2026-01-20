# src/market_api.py
# Removed: from kalshi_python.models import GetMarketRequest
from auth import get_demo_client

def get_market_status(market_ticker):
    """
    Fetches the current status of a single market.
    Returns the market data object.
    """
    client = get_demo_client()
    
    if not client:
        print("Failed to connect client.")
        return None

    try:
        # 1. Pass the ticker directly as a named argument
        response = client.get_market(ticker=market_ticker)
        
        # 2. Handle the response structure
        # Some libraries wrap the data in a "market" property, others return it directly.
        # We check to be safe.
        if hasattr(response, 'market'):
            return response.market
        else:
            # If it doesn't have 'market', the response object IS the market data
            return response

    except Exception as e:
        print(f"Error fetching market {market_ticker}: {e}")
        return None

def print_market_summary(market_ticker):   
    market = market_ticker

    if market:
        print(f"--- Market Summary ---")
        print(f"Ticker: {market.ticker}")
        print(f"Title: {market.title}")
        print(f"Status: {market.status}")
        print(f"Close Time: {market.close_time}")
        
        # Prices are in cents. 50 cents = 0.50 probability
        print(f"Yes Ask: ${market.yes_ask / 100:.2f}")
        print(f"Yes Bid: ${market.yes_bid / 100:.2f}")
        print(f"No Ask:  ${market.no_ask / 100:.2f}")
        print(f"No Bid: ${market.no_bid / 100:.2f}")
        print(f"--------------------")
    else:
        print("Could not retrieve market.")

def list_open_markets(limit=10):
    client = get_demo_client()

    if not client:
        print(f"Failed to connect client.")
        return
    
    try:
        response = client.get_markets(limit=limit, status="open")

        if hasattr(response, 'markets'):
            print(f"--- Found {len(response.markets)} Open Markets ---")
            for market in response.markets:
                print_market_summary(market)

        else:
            print(f"Unexpected response format.")

    except Exception as e:
        print(f"Error reading market list: {e}")
                
def list_active_markets(limit=20):
    """
    Fetches markets that have actual trading volume (liquidity).
    """
    client = get_demo_client()
    
    if not client:
        print("Failed to connect client.")
        return

    try:
        # Request markets
        response = client.get_markets(limit=limit, status="open")
        
        if hasattr(response, 'markets'):
            print(f"--- Scanning {len(response.markets)} markets for activity... ---")
            
            for market in response.markets:
                # FILTER: Only look at markets with at least one trade
                if market.volume > 0:
                    print_market_summary(market)
        
        else:
            print("No markets found.")
            return

    except Exception as e:
        print(f"Error: {e}")
        return

def list_series_markets(keyword="Fed"):
    """
    Searches for markets containing a specific keyword in the title.
    Useful for finding specific high-profile markets (Fed, CPI) in a quiet Demo environment.
    """
    client = get_demo_client()
    
    if not client:
        print("Failed to connect client.")
        return []

    try:
        # Get a large batch of markets
        response = client.get_markets(limit=1000, status="open")
        
        found_markets = []
        
        if hasattr(response, 'markets'):
            print(f"--- Searching for '{keyword}' in {len(response.markets)} markets... ---")
            
            for market in response.markets:
                # Filter: Check if the keyword is in the title
                if keyword.lower() in market.title.lower():
                    found_markets.append(market)
                    print(f"Ticker: {market.ticker}")
                    print(f"Title: {market.title}")
                    
                    # Even if volume is 0, let's check if the exchange set a Last Price
                    if market.last_price > 0:
                        print(f"Last Price: ${market.last_price / 100:.2f}")
                    else:
                        print("Price: No trades yet (Uninitialized)")
                        
                    print("-" * 30)
        
        if not found_markets:
            print(f"No '{keyword}' markets found in the first 1000.")
            return []
            
        return found_markets

    except Exception as e:
        print(f"Error: {e}")
        return []

def list_high_impact_markets(limit=10):
    """
    Fetches markets from the 'HIGH' series.
    These are the Federal Reserve, CPI, and major event markets
    that actually have traders and real prices.
    """
    client = get_demo_client() # or get_demo_client depending on which you are testing
    
    if not client:
        print("Failed to connect client.")
        return []

    try:
        # SPECIFIC FILTER: We only want series_ticker "HIGH"
        response = client.get_markets(
            limit=limit, 
            status="open",
            series_ticker="HIGH" # <--- THE MAGIC PARAMETER
        )
        
        found_markets = []
        
        if hasattr(response, 'markets'):
            print(f"--- Found {len(response.markets)} 'High Impact' Markets ---")
            
            for market in response.markets:
                found_markets.append(market)
                print(f"Ticker: {market.ticker}")
                print(f"Title: {market.title}")
                print(f"Subtitles: {market.subtitle}")
                
                # Now you should see real prices
                print(f"Yes Bid: ${market.yes_bid / 100:.2f}")
                print(f"Yes Ask: ${market.yes_ask / 100:.2f}")
                print(f"Volume: {market.volume}")
                print("-" * 30)
        
        if not found_markets:
            print("No 'High Impact' markets found.")
            return []
            
        return found_markets

    except Exception as e:
        print(f"Error fetching high impact markets: {e}")
        return []
    
def list_all_series():
    """
    Fetches all available Series (categories) from Kalshi.
    This helps us find the correct Ticker for the 'Federal Reserve' or other categories.
    """
    client = get_demo_client() # or get_demo_client
    
    if not client:
        print("Failed to connect client.")
        return

    try:
        # This fetches the list of categories, not individual markets
        response = client.get_series()
        
        print(f"--- Found {len(response.series)} Series Categories ---")
        
        # We are looking for Series that start with "HIGH" or contain "Fed"
        found_fed = False
        for series in response.series:
            # Print every series name so you can see what's available
            print(f"Name: {series.name}")
            print(f"Ticker: {series.ticker}")
            print("-" * 30)
            
            # If we find the Fed series, we can save it for the next step
            if "FED" in series.ticker.upper():
                print(f"!!! FOUND FED SERIES: {series.ticker} !!!")
                found_fed = True
                
        if not found_fed:
            print("Did not find a series with 'FED' in the ticker.")

    except Exception as e:
        print(f"Error fetching series: {e}")

def debug_series_list():
    """
    Prints the raw data of the first series to find correct field names,
    then scans all 8000+ series for 'Fed'.
    """
    client = get_demo_client()
    
    if not client:
        print("Failed to connect client.")
        return

    try:
        response = client.get_series()
        series_list = response.series
        
        print(f"Total Series Found: {len(series_list)}")
        
        # --- STEP 1: Inspect the first item to see the structure ---
        first_series = series_list[0]
        print("\n--- RAW DATA OF FIRST SERIES (Field Names) ---")
        # This prints the actual JSON structure so we can see what to use
        print(first_series.model_dump_json(indent=2))
        print("-" * 50 + "\n")
        
        # --- STEP 2: Search for 'Fed' safely ---
        print("--- Searching for 'Fed' Series... ---")
        count = 0
        for series in series_list:
            # We use getattr to be safe. 
            # We check if it has a 'series_ticker' attribute.
            ticker = getattr(series, 'series_ticker', None)
            
            # We also try to get a human-readable name, trying common options
            name = getattr(series, 'display_name', 
                          getattr(series, 'name', 
                          getattr(series, 'title', "Unknown")))
            
            if ticker and "FED" in ticker.upper():
                count += 1
                print(f"Ticker: {ticker}")
                print(f"Name: {name}")
                print("-" * 30)
                
                if count >= 5: # Stop after 5 finds
                    break
                    
        if count == 0:
            print("No 'Fed' series found in list.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_series_list()
    print("\n" + "=" * 30 + "\n")