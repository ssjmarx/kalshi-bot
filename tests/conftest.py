import pytest
import os


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test."""
    # Clear environment variables
    os.environ.pop("KALSHI_KEY_ID", None)

    yield

    # Cleanup after test
    os.environ.pop("KALSHI_KEY_ID", None)
