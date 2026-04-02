"""Tests for security utilities."""

import uuid

import pytest

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "secure_password_123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_access_token_roundtrip():
    user_id = uuid.uuid4()
    household_id = uuid.uuid4()
    role = "owner"

    token = create_access_token(user_id, household_id, role)
    payload = decode_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["hid"] == str(household_id)
    assert payload["role"] == role
    assert payload["type"] == "access"


def test_refresh_token_roundtrip():
    user_id = uuid.uuid4()
    household_id = uuid.uuid4()

    token, token_id = create_refresh_token(user_id, household_id)
    payload = decode_token(token)

    assert payload["sub"] == str(user_id)
    assert payload["hid"] == str(household_id)
    assert payload["tid"] == str(token_id)
    assert payload["type"] == "refresh"


def test_access_token_contains_expiry():
    token = create_access_token(uuid.uuid4(), uuid.uuid4(), "owner")
    payload = decode_token(token)
    assert "exp" in payload
    assert "iat" in payload
