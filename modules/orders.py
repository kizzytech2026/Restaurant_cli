import json
import os
from typing import List
from modules.menu import load_menu
from modules.models import Order, MenuItem

ORDERS_FILE = os.path.join(os.path.dirname(__file__), "../data/orders.json")


def load_orders() -> list:
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_orders(orders_data: list):
    os.makedirs(os.path.dirname(ORDERS_FILE), exist_ok=True)
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders_data, f, indent=4)


def create_order(username: str, item_ids: list) -> bool:
    menu_data = load_menu()
    selected_dicts = [
        item for item in menu_data
        if isinstance(item, dict) and item.get("id") in item_ids
    ]

    if not selected_dicts:
        print("\nNo valid items selected or items do not exist.")
        return False

    orders_data = load_orders()
    total = sum(float(item.get("price", 0.0)) for item in selected_dicts)
    new_id = max((o.get("id", 0) for o in orders_data), default=0) + 1

    selected_items: list = [
        MenuItem(item["id"], item["name"], item["price"])
        for item in selected_dicts
    ]

    new_order = Order(new_id, username, selected_items,
                      total, status="Pending")
    orders_data.append(new_order.to_dict())
    save_orders(orders_data)

    print(f"\nOrder #{new_id} placed successfully! Total: ${total:.2f}")
    return True


def view_user_orders(username: str):
    orders_data = load_orders()
    user_orders = [o for o in orders_data if o.get("username") == username]
    if not user_orders:
        print("\nNo orders found.")
        return
    print(f"\n--- ORDERS FOR {username} ---")
    for o in user_orders:
        item_names = ", ".join([i["name"] for i in o.get(
            "items", []) if isinstance(i, dict) and "name" in i])
        print(
            f"Order #{o['id']} | Items: {item_names} | Total: ${o['total']:.2f} | Status: {o['status']}")


def view_all_orders():
    orders_data = load_orders()
    if not orders_data:
        print("\nNo active orders in the system.")
        return
    print("\n--- ALL RESTAURANT ORDERS ---")
    for o in orders_data:
        item_names = ", ".join([i["name"] for i in o.get(
            "items", []) if isinstance(i, dict) and "name" in i])
        print(
            f"Order #{o['id']} (Customer: {o['username']}) | Total: ${o['total']:.2f} | Status: {o['status']}")


def cancel_order(order_id: int, username: str) -> bool:
    orders_data = load_orders()
    for o in orders_data:
        if o.get("id") == order_id and o.get("username") == username:
            if o.get("status") in ["Completed", "Cancelled"]:
                print(f"Cannot cancel order with status '{o.get('status')}'.")
                return False
            o["status"] = "Cancelled"
            save_orders(orders_data)
            print(f"Order #{order_id} cancelled.")
            return True
    print("Order not found or permission denied.")
    return False


def update_order_status(order_id: int, new_status: str) -> bool:
    orders_data = load_orders()
    for o in orders_data:
        if o.get("id") == order_id:
            o["status"] = new_status
            save_orders(orders_data)
            print(f"Order #{order_id} status updated to: {new_status}")
            return True
    print("Order ID not found.")
    return False