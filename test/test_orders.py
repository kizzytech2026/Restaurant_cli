import os
import json
import pytest

from modules import orders
from modules import menu


@pytest.fixture
def mock_orders_environment(tmp_path, monkeypatch):
    test_orders_file = tmp_path / "test_orders.json"
    test_menu_file = tmp_path / "test_menu.json"

    monkeypatch.setattr(orders, "ORDERS_FILE", str(test_orders_file))
    monkeypatch.setattr(menu, "MENU_FILE", str(test_menu_file))

    default_menu = [
        {"id": 1, "name": "Burger", "price": 8.50},
        {"id": 2, "name": "Pizza", "price": 12.00}
    ]
    menu.save_menu(default_menu)

    return test_orders_file


def test_load_orders_empty(mock_orders_environment):
    result = orders.load_orders()
    assert result == []


def test_load_orders_invalid_json(mock_orders_environment):
    with open(mock_orders_environment, "w") as f:
        f.write("invalid json")
    assert orders.load_orders() == []


def test_create_order_success(mock_orders_environment, capsys):
    success = orders.create_order("john_doe", [1, 2])
    captured = capsys.readouterr()

    assert success is True
    assert "Order #1 placed successfully! Total: $20.50" in captured.out

    all_orders = orders.load_orders()
    assert len(all_orders) == 1
    assert all_orders[0]["username"] == "john_doe"
    assert all_orders[0]["total"] == 20.50
    assert all_orders[0]["status"] == "Pending"


def test_create_order_invalid_items(mock_orders_environment, capsys):
    success = orders.create_order("john_doe", [99])
    captured = capsys.readouterr()

    assert success is False
    assert "No valid items selected" in captured.out
    assert orders.load_orders() == []


def test_view_user_orders(mock_orders_environment, capsys):
    orders.create_order("alice", [1])
    orders.create_order("bob", [2])

    capsys.readouterr()  # Clear buffer
    orders.view_user_orders("alice")
    captured = capsys.readouterr()

    assert "ORDERS FOR alice" in captured.out
    assert "Burger" in captured.out
    assert "Pizza" not in captured.out


def test_view_user_orders_none(mock_orders_environment, capsys):
    orders.view_user_orders("ghost_user")
    captured = capsys.readouterr()
    assert "No orders found." in captured.out


def test_view_all_orders(mock_orders_environment, capsys):
    orders.create_order("alice", [1])
    orders.create_order("bob", [2])

    capsys.readouterr()
    orders.view_all_orders()
    captured = capsys.readouterr()

    assert "ALL RESTAURANT ORDERS" in captured.out
    assert "alice" in captured.out
    assert "bob" in captured.out


def test_cancel_order_success(mock_orders_environment, capsys):
    orders.create_order("alice", [1])

    success = orders.cancel_order(1, "alice")
    captured = capsys.readouterr()

    assert success is True
    assert "Order #1 cancelled." in captured.out

    updated_orders = orders.load_orders()
    assert updated_orders[0]["status"] == "Cancelled"


def test_cancel_order_unauthorized_or_completed(mock_orders_environment, capsys):
    orders.create_order("alice", [1])

    success = orders.cancel_order(1, "bob")
    assert success is False

    orders.update_order_status(1, "Completed")
    success = orders.cancel_order(1, "alice")
    captured = capsys.readouterr()

    assert success is False
    assert "Cannot cancel order with status 'Completed'." in captured.out


def test_update_order_status(mock_orders_environment, capsys):
    orders.create_order("alice", [1])

    success = orders.update_order_status(1, "Preparing")
    captured = capsys.readouterr()

    assert success is True
    assert "Order #1 status updated to: Preparing" in captured.out

    updated_orders = orders.load_orders()
    assert updated_orders[0]["status"] == "Preparing"