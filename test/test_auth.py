import os
import json
import pytest

from modules import auth


@pytest.fixture
def mock_users_file(tmp_path, monkeypatch):
    test_file = tmp_path / "test_users.json"

    monkeypatch.setattr(auth, "USERS_FILE", str(test_file))

    return test_file


def test_load_users_empty(mock_users_file):
    users = auth.load_users()

    assert users == []


def test_load_users_invalid_json(mock_users_file):
    with open(mock_users_file, "w") as f:
        f.write("not valid json")

    assert auth.load_users() == []


def test_register_user_success(mock_users_file):
    success, msg = auth.register_user("testuser", "pass123")

    assert success is True
    assert "Account created successfully" in msg

    users = auth.load_users()
    assert len(users) == 1
    assert users[0]["username"] == "testuser"
    assert users[0]["role"] == "Customer"


def test_register_user_duplicate(mock_users_file):
    auth.register_user("existinguser", "pass123")

    success, msg = auth.register_user("existinguser", "newpass")

    assert success is False
    assert msg == "Username already exists."


def test_login_user_success(mock_users_file):
    auth.register_user("loginuser", "securepass")
    success, user_data = auth.login_user("loginuser", "securepass")

    assert success is True
    assert user_data is not None
    assert user_data["username"] == "loginuser"


def test_login_user_failure(mock_users_file):
    auth.register_user("loginuser", "securepass")

    success, user_data = auth.login_user("loginuser", "wrongpass")

    assert success is False
    assert user_data is None
