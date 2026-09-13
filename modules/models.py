from typing import List, Dict, Any, Union


class User:

    def __init__(self, user_id: int, username: str, password: str, role: str = "Customer"):
        self.id = user_id
        self.username = username
        self._password = password  # Encapsulated (protected) attribute
        self.role = role

    def check_password(self, password: str) -> bool:
        return self._password == password

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "password": self._password,
            "role": self.role
        }


class Customer(User):

    def __init__(self, user_id: int, username: str, password: str):
        super().__init__(user_id, username, password, role="Customer")


class Admin(User):

    def __init__(self, user_id: int, username: str, password: str):
        super().__init__(user_id, username, password, role="Management Staff")


class MenuItem:

    def __init__(self, item_id: int, name: str, price: float):
        self.id = item_id
        self.name = name
        self.price = float(price)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }


class Order:

    def __init__(self, order_id: int, username: str, items: Any, total: float, status: str = "Pending"):
        self.id = order_id
        self.username = username
        self.items = items
        self.total = float(total)
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        serialized_items = []
        for item in self.items:
            if hasattr(item, "to_dict"):
                serialized_items.append(item.to_dict())
            elif isinstance(item, dict):
                serialized_items.append(item)

        return {
            "id": self.id,
            "username": self.username,
            "items": serialized_items,
            "total": self.total,
            "status": self.status
        }
