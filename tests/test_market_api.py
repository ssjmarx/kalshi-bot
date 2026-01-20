from unittest.mock import MagicMock
from src.market_api import MarketAPI, MarketData


def test_market_api_initialization():
    """Test that MarketAPI initializes with a KalshiClient."""
    # Create mock client
    mock_client = MagicMock()

    # Initialize MarketAPI
    api = MarketAPI(mock_client)

    # Verify client is stored
    assert api.client is mock_client


def test_get_market_data_success():
    """Test fetching market data for a valid market ticker."""
    # Create mock client
    mock_client = MagicMock()

    # Mock API response
    mock_response = MagicMock()
    mock_response.market = MagicMock()
    mock_response.market.ticker = "TEST-TICKER"
    mock_response.market.title = "Test Market Title"
    mock_response.market.status = "open"
    mock_response.market.yes_bid = 45
    mock_response.market.no_bid = 55
    # Use a future date (year 2027) to ensure seconds_until_close > 0
    mock_response.market.close_time = "2027-12-31T23:59:59Z"
    
    mock_client.get_market.return_value = mock_response

    # Initialize MarketAPI
    api = MarketAPI(mock_client)

    # Fetch market data
    market_data = api.get_market_data("TEST-TICKER")

    # Verify returned data
    assert market_data is not None
    assert isinstance(market_data, MarketData)
    assert market_data.market_id == "TEST-TICKER"
    assert market_data.market_ticker == "TEST-TICKER"
    assert market_data.title == "Test Market Title"
    assert market_data.status == "open"
    assert market_data.yes_bid == 45
    assert market_data.no_bid == 55
    assert market_data.seconds_until_close > 0


def test_get_market_data_invalid_ticker():
    """Test that invalid market ticker returns None."""
    # Create mock client that returns None or empty
    mock_client = MagicMock()
    mock_client.get_market.return_value = None

    # Initialize MarketAPI
    api = MarketAPI(mock_client)

    # Fetch market data for invalid ticker
    market_data = api.get_market_data("invalid_ticker")

    # Should return None
    assert market_data is None


def test_get_market_data_no_market():
    """Test that response without market returns None."""
    # Create mock client with response without market
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.market = None
    mock_client.get_market.return_value = mock_response

    # Initialize MarketAPI
    api = MarketAPI(mock_client)

    # Fetch market data
    market_data = api.get_market_data("any_ticker")

    # Should return None
    assert market_data is None


def test_get_market_data_api_error():
    """Test that API errors are handled gracefully."""
    # Create mock client that raises exception
    mock_client = MagicMock()
    mock_client.get_market.side_effect = Exception("API Error")

    # Initialize MarketAPI
    api = MarketAPI(mock_client)

    # Fetch market data
    market_data = api.get_market_data("any_ticker")

    # Should return None (error is printed but not raised)
    assert market_data is None


def test_get_markets_by_ticker_success():
    """Test fetching markets by ticker pattern."""
    # Create mock client
    mock_client = MagicMock()

    # Mock API response
    mock_response = MagicMock()
    mock_market1 = MagicMock()
    mock_market1.ticker = "TEST-1"
    mock_market1.title = "Test Market 1"
    
    mock_market2 = MagicMock()
    mock_market2.ticker = "TEST-2"
    mock_market2.title = "Test Market 2"
    
    mock_response.markets = [mock_market1, mock_market2]
    mock_client.get_markets.return_value = mock_response

    # Initialize MarketAPI
    api = MarketAPI(mock_client)

    # Fetch markets by ticker
    markets = api.get_markets_by_ticker("TEST")

    # Verify results
    assert len(markets) == 2
    assert markets[0]["ticker_symbol"] == "TEST-1"
    assert markets[1]["ticker_symbol"] == "TEST-2"


def test_get_markets_by_ticker_no_results():
    """Test that non-matching ticker returns empty list."""
    # Create mock client
    mock_client = MagicMock()

    # Mock API response with empty markets
    mock_response = MagicMock()
    mock_response.markets = []
    mock_client.get_markets.return_value = mock_response

    # Initialize MarketAPI
    api = MarketAPI(mock_client)

    # Fetch markets by ticker
    markets = api.get_markets_by_ticker("NONEXISTENT")

    # Should return empty list
    assert markets == []
