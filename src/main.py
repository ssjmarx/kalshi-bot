import sys
from .auth import KalshiAuth
from .market_api import MarketAPI

# For Phase 1, we'll fetch markets dynamically
# The bot will list available markets and you can choose one
# Or uncomment and set a specific market ticker:
# DEMO_MARKET_TICKER = "YOUR_SPECIFIC_TICKER_HERE"
DEMO_MARKET_TICKER = None  # None means list markets first


def list_available_markets(market_api: MarketAPI, limit: int = 20) -> None:
    """List available markets from the Kalshi API.

    Args:
        market_api: MarketAPI instance
        limit: Number of markets to display
    """
    print("\nFetching available markets...")

    # Get all markets (no ticker filter to see everything)
    markets = market_api.get_markets_by_ticker("")

    if not markets:
        print("No markets found")
        return

    print(f"\nFound {len(markets)} markets. Showing first {limit}:\n")
    print(f"{'#':<4} {'Ticker':<36} {'Title':<50}")
    print("-" * 90)

    for i, market in enumerate(markets[:limit], 1):
        ticker = market.get("ticker_symbol", "N/A")
        title = market.get("title", "N/A")[:50]  # Truncate long titles

        print(f"{i:<4} {ticker:<36} {title:<50}")

    if len(markets) > limit:
        print(f"\n... and {len(markets) - limit} more markets")
    print("\nTo use a specific market, set DEMO_MARKET_TICKER in main.py")


def main() -> None:
    """Main function to demonstrate API connection."""

    print("=== Kalshi Bot - Phase 1: Connect & Observe ===\n")

    # Step 1: Initialize authentication
    print("Step 1: Initializing authentication...")
    try:
        auth = KalshiAuth()
        print("Authentication successful\n")
    except ValueError as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

    # Step 2: Create MarketAPI instance
    print("Step 2: Initializing Market API...")
    market_api = MarketAPI(auth.get_client())
    print("Market API initialized\n")

    # Step 3: If no market ticker specified, list available markets
    if not DEMO_MARKET_TICKER:
        print("No specific market ticker provided. Listing available markets...")
        list_available_markets(market_api)
        print("\nTo fetch data for a specific market:")
        print("1. Choose a ticker from the list above")
        print("2. Set DEMO_MARKET_TICKER = 'your_ticker' in main.py")
        print("3. Run the script again")
        print("\n=== Phase 1 Complete (Market Discovery Mode) ===")
        return

    # Step 4: Fetch market data for specified market
    print(f"Step 3: Fetching data for market {DEMO_MARKET_TICKER}...")
    market_data = market_api.get_market_data(DEMO_MARKET_TICKER)

    if not market_data:
        print("Failed to fetch market data")
        print("Note: Make sure the ticker is valid and the market exists")
        print("Run with DEMO_MARKET_TICKER = None to list available markets")
        sys.exit(1)

    print("Market data fetched successfully\n")

    # Step 5: Display market information
    print("=== Market Information ===")
    print(f"Market: {market_data.title}")
    print(f"Ticker: {market_data.market_ticker}")
    print(f"Status: {market_data.status}")
    print(f"Current Price (Yes Bid): {market_data.yes_bid} cents")
    print(f"Current Price (No Bid): {market_data.no_bid} cents")
    print(f"Close Time: {market_data.close_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(
        f"Closes in: {market_data.seconds_until_close // 3600} hours "
        f"{(market_data.seconds_until_close % 3600) // 60} minutes"
    )
    print("\n=== Phase 1 Complete ===")


if __name__ == "__main__":
    main()
