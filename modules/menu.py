import json
import os
from typing import Optional
from modules.models import MenuItem

MENU_FILE = os.path.join(os.path.dirname(__file__), "../data/menu.json")


def load_menu() -> list:
    if not os.path.exists(MENU_FILE):
        default_menu = [
            {"id": 1, "name": "Burger", "price": 8.50},
            {"id": 2, "name": "Pizza", "price": 12.00},
            {"id": 3, "name": "Fries", "price": 3.50}
        ]
        save_menu(default_menu)
        return default_menu
    with open(MENU_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_menu(menu_data: list):
    os.makedirs(os.path.dirname(MENU_FILE), exist_ok=True)
    with open(MENU_FILE, "w") as f:
        json.dump(menu_data, f, indent=4)


def list_menu():
    menu_data = load_menu()
    if not menu_data:
        print("\n[Menu is currently empty]")
        return
    print("\n--- KEROMA MENU ---")
    for item in menu_data:
        if isinstance(item, dict):
            print(
                f"[{item.get('id', 'N/A')}] {item.get('name', 'Unknown')} - ${item.get('price', 0.0):.2f}")


def add_menu_item(name: str, price: float):
    menu_data = load_menu()
    valid_ids = [item["id"]
                 for item in menu_data if isinstance(item, dict) and "id" in item]
    new_id = max(valid_ids, default=0) + 1

    new_item = MenuItem(new_id, name, price)
    menu_data.append(new_item.to_dict())
    save_menu(menu_data)
    print(f"Added: {name} (${price:.2f})")


def update_menu_item(item_id: int, name: Optional[str] = None, price: Optional[float] = None) -> bool:
    menu_data = load_menu()
    for item in menu_data:
        if item["id"] == item_id:
            if name:
                item["name"] = name
            if price is not None:
                item["price"] = float(price)
            save_menu(menu_data)
            print("Menu item updated successfully.")
            return True
    print("Item ID not found.")
    return False


def delete_menu_item(item_id: int) -> bool:
    menu_data = load_menu()
    new_menu = [item for item in menu_data if item["id"] != item_id]
    if len(new_menu) == len(menu_data):
        print("Item ID not found.")
        return False
    save_menu(new_menu)
    print("Menu item removed successfully.")
    return True