import pytest

from app.security.auth import (
    generate_api_key,
    hash_api_key,
    verify_api_key,
    create_jwt_token,
    decode_jwt_token,
)


def test_generate_api_key():
    key = generate_api_key()
    assert key.startswith("zsl_")
    assert len(key) > 10


def test_hash_and_verify_api_key():
    key = generate_api_key()
    hashed = hash_api_key(key)
    assert verify_api_key(key, hashed) is True
    assert verify_api_key("wrong_key", hashed) is False


def test_create_and_decode_jwt():
    token = create_jwt_token({"sub": "test_user", "role": "admin"})
    payload = decode_jwt_token(token)
    assert payload is not None
    assert payload["sub"] == "test_user"
    assert payload["role"] == "admin"


def test_decode_invalid_jwt():
    payload = decode_jwt_token("invalid.token.here")
    assert payload is None


def test_decode_expired_jwt():
    from datetime import timedelta
    token = create_jwt_token({"sub": "test"}, expires_delta=timedelta(seconds=-1))
    payload = decode_jwt_token(token)
    assert payload is None
