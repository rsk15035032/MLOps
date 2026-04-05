"""
FastAPI Test Suite (Production-Ready)

This module contains integration tests for the Items API.

Features:
- Header-based authentication testing
- CRUD operation validation
- Error handling verification
- Clean and maintainable test structure

Run with:
    pytest -v
"""

from fastapi.testclient import TestClient
from .main import app

# -------------------------------------------------------------------
# Test Client
# -------------------------------------------------------------------

client = TestClient(app)

# -------------------------------------------------------------------
# Constants (Avoid magic values)
# -------------------------------------------------------------------

VALID_TOKEN = "coneofsilence"
INVALID_TOKEN = "hailhydra"

HEADERS_VALID = {"X-Token": VALID_TOKEN}
HEADERS_INVALID = {"X-Token": INVALID_TOKEN}


# -------------------------------------------------------------------
# Test: Read Existing Item
# -------------------------------------------------------------------

def test_read_item_success():
    """
    Test retrieving an existing item with valid authentication.

    Expected:
        - Status code: 200
        - Correct item data returned
    """
    response = client.get("/items/foo", headers=HEADERS_VALID)

    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


# -------------------------------------------------------------------
# Test: Invalid Token (Read)
# -------------------------------------------------------------------

def test_read_item_invalid_token():
    """
    Test retrieving an item with invalid authentication token.

    Expected:
        - Status code: 400
        - Error message returned
    """
    response = client.get("/items/foo", headers=HEADERS_INVALID)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


# -------------------------------------------------------------------
# Test: Non-Existent Item
# -------------------------------------------------------------------

def test_read_item_not_found():
    """
    Test retrieving a non-existent item.

    Expected:
        - Status code: 404
        - Appropriate error message
    """
    response = client.get("/items/baz", headers=HEADERS_VALID)

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


# -------------------------------------------------------------------
# Test: Create Item (Success)
# -------------------------------------------------------------------

def test_create_item_success():
    """
    Test creating a new item with valid authentication.

    Expected:
        - Status code: 200
        - Created item returned
    """
    payload = {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }

    response = client.post("/items/", headers=HEADERS_VALID, json=payload)

    assert response.status_code == 200
    assert response.json() == payload


# -------------------------------------------------------------------
# Test: Create Item with Invalid Token
# -------------------------------------------------------------------

def test_create_item_invalid_token():
    """
    Test creating an item with invalid authentication.

    Expected:
        - Status code: 400
        - Error message returned
    """
    payload = {
        "id": "bazz",
        "title": "Bazz",
        "description": "Drop the bazz",
    }

    response = client.post("/items/", headers=HEADERS_INVALID, json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


# -------------------------------------------------------------------
# Test: Create Existing Item (Conflict)
# -------------------------------------------------------------------

def test_create_existing_item_conflict():
    """
    Test creating an item that already exists.

    Expected:
        - Status code: 409
        - Conflict error message
    """
    payload = {
        "id": "foo",  # Already exists
        "title": "The Foo ID Stealers",
        "description": "There goes my stealer",
    }

    response = client.post("/items/", headers=HEADERS_VALID, json=payload)

    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}