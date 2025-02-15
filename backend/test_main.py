import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_order():
    # Test creating a new order
    response = client.post(
        "/orders",
        json={"message": "I would like 2 burgers, 1 fries, and 1 drink"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Successfully added order" in data
    order = data["Successfully added order"]
    assert order["burgers"] == 2
    assert order["fries"] == 1
    assert order["drinks"] == 1

def test_negative_order():
    # Test creating an order with negative numbers
    response = client.post(
        "/orders",
        json={"message": "I want -2 burgers and -1 fries"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "Invalid input. Please provide a valid order or cancellation request."

def test_get_orders():
    # Test getting all orders
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert "orderHistory" in data
    assert isinstance(data["orderHistory"], list)

def test_remove_order():
    # First create an order
    response = client.post(
        "/orders",
        json={"message": "I want 1 burger"}
    )
    order_id = response.json()["Successfully added order"]["id"]
    
    # Then test removing it
    response = client.post(
        "/orders",
        json={"message": f"Cancel order {order_id}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Successfully removed order" in data
    assert data["Successfully removed order"] == order_id

def test_remove_nonexistent_order():
    # Test removing an order that doesn't exist
    response = client.post(
        "/orders",
        json={"message": "Cancel order 9999"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] == "Order not found" 