import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Product Intelligence API" in resp.json()["message"]

def test_search_empty():
    resp = client.get("/search?query=nonexistentproduct")
    assert resp.status_code == 200
    assert resp.json() == []
