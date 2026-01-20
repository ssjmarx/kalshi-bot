from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from kalshi_python import KalshiClient


@dataclass
class MarketData:
    """Represents market data from the Kalshi API."""

    market_id: str
    market_ticker: str
    title: str
    status: str
    yes_bid: int  # in cents
    no_bid: int  # in cents
    close_time: datetime
    seconds_until_close: int


class MarketAPI:
    """Handles communication with Kalshi API to fetch market data."""

    def __init__(self, client: KalshiClient) -> None:
        """Initialize MarketAPI with authenticated client.

        Args:
            client: Authenticated KalshiClient instance
        """
        self.client = client

    def get_market_data(self, ticker: str) -> Optional[MarketData]:
        """Fetch market data for a specific market by ticker.

        Args:
            ticker: The ticker symbol of the market (e.g., "HIGH-NYC-01")

        Returns:
            MarketData object if successful, None if market not found or error
        """
        try:
            # Call Kalshi API to get market details
            response = self.client.get_market(ticker=ticker)

            # Check if request was successful
            if not response or not response.market:
                return None

            market = response.market

            # Parse close_time to datetime
            # The API returns ISO format string without timezone
            close_time = datetime.fromisoformat(market.close_time.replace("Z", ""))

            # Calculate seconds until close (both are now timezone-naive)
            time_until_close = int((close_time - datetime.now()).total_seconds())

            # Create and return MarketData object
            return MarketData(
                market_id=ticker,  # Use ticker as market_id for now
                market_ticker=market.ticker,
                title=market.title,
                status=market.status.value if hasattr(market.status, "value") else str(market.status),
                yes_bid=market.yes_bid if market.yes_bid else 0,
                no_bid=market.no_bid if market.no_bid else 0,
                close_time=close_time,
                seconds_until_close=time_until_close,
            )

        except Exception as e:
            # Log error and return None
            print(f"Error fetching market {ticker}: {e}")
            return None

    def get_markets_by_ticker(self, ticker: str) -> list:
        """Get all markets matching a ticker pattern.

        Args:
            ticker: Ticker symbol or pattern to search for (empty string for all markets)

        Returns:
            List of Market objects matching the ticker
        """
        try:
            response = self.client.get_markets(limit=100, tickers=ticker if ticker else None)

            if not response or not response.markets:
                return []

            # Convert Market objects to dictionaries
            markets_list = []
            for market in response.markets:
                markets_list.append(
                    {
                        "market_id": market.ticker,  # Use ticker as ID
                        "ticker_symbol": market.ticker,
                        "title": market.title,
                    }
                )

            return markets_list

        except Exception as e:
            print(f"Error fetching markets for ticker {ticker}: {e}")
            return []
