import json
import os
from modules.models import User, Customer, Admin

USERS_FILE = os.path.join(os.path.dirname(__file__), "../data/users.json")


def load_users() -> list:
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_users(users_data: list):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users_data, f, indent=4)


def register_user(username: str, password: str, role: str = "Customer"):
    users_data = load_users()
    for u in users_data:
        if u["username"] == username:
            return False, "Username already exists."

    new_id = len(users_data) + 1

    if role in ["Admin", "Management Staff"]:
        user_obj = Admin(new_id, username, password)
    else:
        user_obj = Customer(new_id, username, password)

    users_data.append(user_obj.to_dict())
    save_users(users_data)
    return True, f"Account created successfully as {role}."


def login_user(username: str, password: str):
    users_data = load_users()
    for u in users_data:
        if u["username"] == username:
            user_obj = User(u["id"], u["username"], u["password"], u["role"])
            if user_obj.check_password(password):
                return True, user_obj.to_dict()
    return False, None
