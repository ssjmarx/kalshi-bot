import os
import tempfile
import pytest
from src.auth import KalshiAuth


def test_auth_initialization_success():
    """Test that KalshiAuth initializes with valid key ID and PEM file."""
    # Create a temporary PEM file
    pem_content = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEArhgdrbUPhBQWTI/JfjPpuV5qWnzin918uj/F/eQ364SVbtL+
m+IsBXwf0o2efbc0dXgsZs17nuQ7yMRDncscoozTUubwMyL3+QDQkTgRFd26nlSW
WTn1jVo8lomHiL9bdnW+CfXnmAdaHvilXMVgQLLa4YSGrW/GWbpOeWTRNg80Ct6h
wvwUvhENrb4G2GMaMwL0ULIHIUi2RDN5xzgFO4XOrzdDLKu4+NQwcDYUfOCvTbtO
N+urLKG3WiwWGcssRMD/FYBobNRLuUPi9brt5WM6zcd21hjc+SWX8QtrbdxyzSqH
7ehNT9v8FiIYGH4aQ/K4GeBxe3Zzkz1cdvECAwIDAQABAoIBAAVfhviRa4XfwHAJ
fT/XZogxmUyEqTi85pIX0Mqmv6RI7PtejyKMuix+XO8SYhXIN0Be5QpUa9NtTa92
TnRXmS3zjojy/SJFTh9emCrubsL2TnTl8HDKWkFMGGDSPgW8iwKeqXuRat3yCb6F
9xIxB09hfC7uRUfW3zZt8RxL18crmoFvTHeU5ZFj7WSZslgFQ0sciT09Uzu1XR/b
UU3AApUpSepWt8IRglExUDYIQ2NK7rUnb/hHVgf/50uq2n6cs8YW1Z0ytZV1pYIl
ZZSI5a/l4d0S4fNly3RcL+4VnEfEIXsSl2X9sLjRnlLXR7qlos1UvlOcGykQcjXj
Fc9ejXkCgYEAyMfvPQodHD00W1N1e+sF+5zCf1x0fjsussqkYUiwozpnSfBTeD05
JVZWsEZ3dbcfAQJ1jSFS37zOQ20ggkot8mx4mJ4gt7gy0G9LW/ypWY/REm4BAFfm
CSE9yxkJpMqSmXxfkPFM4dKUWDGG87uy1q5Orl7fvFxg7AyB6KqgFikCgYEA3flJ
i11OjjRN72dFJSr/0+exEQ+BtI8aLIeJ9lOCFp02rrXsx3TjO5JWPXvPx5hEXsne
Rd0v2NKd97udr+ZYakgjezS49TFrJuW4HaFP+PPuWfeey3Uhfo7Vx13+ncYA4QxW
kWi7Uyzk7Y7fFcqklHm3ENym4GJz+Wql+ZGe5EsCgYAxQ10fzOt3kkzWW5Pn47KE
GeJe/YBXuI2ssKvEcuFkK2BMc/sG9X6f+p8qgR+uck/ZH5FYH2UGIH07bfsb/Ldp
U9QDHklIypktKyGCYGvs3ayeqP715ps6gj13J52GIW322t1X4tzKS7C6Muy5wMQQ
iJQllIGw5bmiMS9utu6wgQKBgQDc1DeNVUtkf7aVGIkam/edKh/m2CVyqvcgG8tt
6tA9jTQshcLE/41c4422Zylj6SEDqBLgMFd8frQ3FEihCSkmuxPJa78h94MhVGJh
3+y+wHZ8vLMWuDWVQaZ+TA2VirmvKmYpDSdnbP9nMr7PYCVxrNEqDkpaarf0B1yN
t4h6lwKBgQCHXh8YCDupyB4z1NF8HJT/2EeYrv3Xiz5UsF0ual2IkaT6oIaOJIXq
rIVcXqB//EOc2gCp4O/Y2JGxViLITxbv9vwqwfHFszMldm3nIMNMJ6kC/bzKKP0v
d5r8f3JhQhXO5uacBiOBjhxV65XT95nvJbZiLKBrApBSkYjoZ12uWg==
-----END RSA PRIVATE KEY-----"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".pem", delete=False) as f:
        f.write(pem_content)
        pem_path = f.name

    try:
        # Set up valid environment variable
        os.environ["KALSHI_KEY_ID"] = "test_key_123"

        # Initialize should succeed
        auth = KalshiAuth(key_id="test_key_123", private_key_path=pem_path)

        # Verify credentials are stored
        assert auth.key_id == "test_key_123"
        assert auth.private_key_path == pem_path
        assert auth.private_key is not None
        assert auth.client is not None
    finally:
        # Cleanup
        os.unlink(pem_path)
        os.environ.pop("KALSHI_KEY_ID", None)


def test_auth_missing_key_id():
    """Test that KalshiAuth raises ValueError when key ID is missing."""
    # Clear environment variable
    os.environ.pop("KALSHI_KEY_ID", None)

    # Should raise ValueError
    with pytest.raises(ValueError, match="KALSHI_KEY_ID must be set"):
        KalshiAuth()


def test_auth_missing_pem_file():
    """Test that KalshiAuth raises FileNotFoundError when PEM file is missing."""
    # Set key ID but use non-existent PEM file
    os.environ["KALSHI_KEY_ID"] = "test_key"

    # Should raise FileNotFoundError
    with pytest.raises(FileNotFoundError, match="Private key file not found"):
        KalshiAuth(private_key_path="nonexistent/path/to/key.pem")


def test_get_client_returns_client():
    """Test that get_client returns the KalshiClient instance."""
    # Create a temporary PEM file
    pem_content = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEArhgdrbUPhBQWTI/JfjPpuV5qWnzin918uj/F/eQ364SVbtL+
m+IsBXwf0o2efbc0dXgsZs17nuQ7yMRDncscoozTUubwMyL3+QDQkTgRFd26nlSW
WTn1jVo8lomHiL9bdnW+CfXnmAdaHvilXMVgQLLa4YSGrW/GWbpOeWTRNg80Ct6h
wvwUvhENrb4G2GMaMwL0ULIHIUi2RDN5xzgFO4XOrzdDLKu4+NQwcDYUfOCvTbtO
N+urLKG3WiwWGcssRMD/FYBobNRLuUPi9brt5WM6zcd21hjc+SWX8QtrbdxyzSqH
7ehNT9v8FiIYGH4aQ/K4GeBxe3Zzkz1cdvECAwIDAQABAoIBAAVfhviRa4XfwHAJ
fT/XZogxmUyEqTi85pIX0Mqmv6RI7PtejyKMuix+XO8SYhXIN0Be5QpUa9NtTa92
TnRXmS3zjojy/SJFTh9emCrubsL2TnTl8HDKWkFMGGDSPgW8iwKeqXuRat3yCb6F
9xIxB09hfC7uRUfW3zZt8RxL18crmoFvTHeU5ZFj7WSZslgFQ0sciT09Uzu1XR/b
UU3AApUpSepWt8IRglExUDYIQ2NK7rUnb/hHVgf/50uq2n6cs8YW1Z0ytZV1pYIl
ZZSI5a/l4d0S4fNly3RcL+4VnEfEIXsSl2X9sLjRnlLXR7qlos1UvlOcGykQcjXj
Fc9ejXkCgYEAyMfvPQodHD00W1N1e+sF+5zCf1x0fjsussqkYUiwozpnSfBTeD05
JVZWsEZ3dbcfAQJ1jSFS37zOQ20ggkot8mx4mJ4gt7gy0G9LW/ypWY/REm4BAFfm
CSE9yxkJpMqSmXxfkPFM4dKUWDGG87uy1q5Orl7fvFxg7AyB6KqgFikCgYEA3flJ
i11OjjRN72dFJSr/0+exEQ+BtI8aLIeJ9lOCFp02rrXsx3TjO5JWPXvPx5hEXsne
Rd0v2NKd97udr+ZYakgjezS49TFrJuW4HaFP+PPuWfeey3Uhfo7Vx13+ncYA4QxW
kWi7Uyzk7Y7fFcqklHm3ENym4GJz+Wql+ZGe5EsCgYAxQ10fzOt3kkzWW5Pn47KE
GeJe/YBXuI2ssKvEcuFkK2BMc/sG9X6f+p8qgR+uck/ZH5FYH2UGIH07bfsb/Ldp
U9QDHklIypktKyGCYGvs3ayeqP715ps6gj13J52GIW322t1X4tzKS7C6Muy5wMQQ
iJQllIGw5bmiMS9utu6wgQKBgQDc1DeNVUtkf7aVGIkam/edKh/m2CVyqvcgG8tt
6tA9jTQshcLE/41c4422Zylj6SEDqBLgMFd8frQ3FEihCSkmuxPJa78h94MhVGJh
3+y+wHZ8vLMWuDWVQaZ+TA2VirmvKmYpDSdnbP9nMr7PYCVxrNEqDkpaarf0B1yN
t4h6lwKBgQCHXh8YCDupyB4z1NF8HJT/2EeYrv3Xiz5UsF0ual2IkaT6oIaOJIXq
rIVcXqB//EOc2gCp4O/Y2JGxViLITxbv9vwqwfHFszMldm3nIMNMJ6kC/bzKKP0v
d5r8f3JhQhXO5uacBiOBjhxV65XT95nvJbZiLKBrApBSkYjoZ12uWg==
-----END RSA PRIVATE KEY-----"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".pem", delete=False) as f:
        f.write(pem_content)
        pem_path = f.name

    try:
        os.environ["KALSHI_KEY_ID"] = "test_key"

        auth = KalshiAuth(key_id="test_key", private_key_path=pem_path)
        client = auth.get_client()

        # Should return the same client instance
        assert client is auth.client
        assert client is not None
    finally:
        # Cleanup
        os.unlink(pem_path)
        os.environ.pop("KALSHI_KEY_ID", None)
