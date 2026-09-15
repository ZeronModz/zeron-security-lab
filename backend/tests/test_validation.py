import pytest

from app.security.validation import validate_url, is_safe_url, ValidationError


def test_validate_url_empty():
    with pytest.raises(ValidationError) as exc_info:
        validate_url("")
    assert exc_info.value.code == "INVALID_URL"


def test_validate_url_whitespace():
    with pytest.raises(ValidationError):
        validate_url("   ")


def test_validate_url_invalid_scheme():
    with pytest.raises(ValidationError) as exc_info:
        validate_url("ftp://example.com")
    assert exc_info.value.code == "INVALID_SCHEME"


def test_validate_url_localhost():
    with pytest.raises(ValidationError) as exc_info:
        validate_url("http://localhost:8080")
    assert exc_info.value.code == "PRIVATE_TARGET"


def test_validate_url_127():
    with pytest.raises(ValidationError) as exc_info:
        validate_url("http://127.0.0.1/admin")
    assert exc_info.value.code == "PRIVATE_TARGET"


def test_validate_url_private_10():
    with pytest.raises(ValidationError) as exc_info:
        validate_url("http://10.0.0.1/")
    assert exc_info.value.code == "PRIVATE_TARGET"


def test_validate_url_private_172():
    with pytest.raises(ValidationError) as exc_info:
        validate_url("http://172.16.0.1/")
    assert exc_info.value.code == "PRIVATE_TARGET"


def test_validate_url_private_192():
    with pytest.raises(ValidationError) as exc_info:
        validate_url("http://192.168.1.1/")
    assert exc_info.value.code == "PRIVATE_TARGET"


def test_validate_url_ipv6_loopback():
    with pytest.raises(ValidationError) as exc_info:
        validate_url("http://[::1]/")
    assert exc_info.value.code == "PRIVATE_TARGET"


def test_validate_url_valid():
    result = validate_url("https://example.com")
    assert result == "https://example.com"


def test_validate_url_valid_with_path():
    result = validate_url("https://example.com/path/to/resource")
    assert result == "https://example.com/path/to/resource"


def test_validate_url_valid_with_query():
    result = validate_url("https://example.com/search?q=test&page=1")
    assert "example.com" in result


def test_is_safe_url_valid():
    assert is_safe_url("https://example.com") is True


def test_is_safe_url_invalid():
    assert is_safe_url("http://localhost") is False
    assert is_safe_url("http://127.0.0.1") is False
    assert is_safe_url("") is False
    assert is_safe_url("ftp://example.com") is False
