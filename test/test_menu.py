import os
import json
import pytest

from modules import menu


@pytest.fixture
def mock_menu_file(tmp_path, monkeypatch):
    test_file = tmp_path / "test_menu.json"
    monkeypatch.setattr(menu, "MENU_FILE", str(test_file))
    return test_file


def test_load_menu_creates_default(mock_menu_file):
    result = menu.load_menu()

    assert len(result) == 3
    assert result[0]["name"] == "Burger"
    assert os.path.exists(mock_menu_file)


def test_load_menu_invalid_json(mock_menu_file):
    with open(mock_menu_file, "w") as f:
        f.write("not valid json")

    assert menu.load_menu() == []


def test_list_menu(mock_menu_file, capsys):
    menu.load_menu()

    menu.list_menu()

    captured = capsys.readouterr()

    assert "KEROMA MENU" in captured.out
    assert "[1] Burger - $8.50" in captured.out
    assert "[2] Pizza - $12.00" in captured.out


def test_add_menu_item(mock_menu_file, capsys):
    menu.load_menu()

    menu.add_menu_item("Salad", 5.99)
    captured = capsys.readouterr()

    assert "Added: Salad ($5.99)" in captured.out

    items = menu.load_menu()
    assert len(items) == 4
    assert items[-1]["name"] == "Salad"
    assert items[-1]["id"] == 4
    assert items[-1]["price"] == 5.99


def test_update_menu_item_success(mock_menu_file, capsys):
    menu.load_menu()

    result = menu.update_menu_item(1, name="Cheeseburger", price=9.50)
    captured = capsys.readouterr()

    assert result is True
    assert "Menu item updated successfully." in captured.out

    items = menu.load_menu()
    assert items[0]["name"] == "Cheeseburger"
    assert items[0]["price"] == 9.50


def test_update_menu_item_not_found(mock_menu_file, capsys):
    menu.load_menu()

    result = menu.update_menu_item(99, name="Ghost Item")
    captured = capsys.readouterr()

    assert result is False
    assert "Item ID not found." in captured.out


def test_delete_menu_item_success(mock_menu_file, capsys):
    menu.load_menu()

    result = menu.delete_menu_item(1)
    captured = capsys.readouterr()

    assert result is True
    assert "Menu item removed successfully." in captured.out

    items = menu.load_menu()
    assert len(items) == 2
    assert items[0]["id"] == 2  # Pizza should now be the first item


def test_delete_menu_item_not_found(mock_menu_file, capsys):
    menu.load_menu()

    result = menu.delete_menu_item(99)
    captured = capsys.readouterr()

    assert result is False
    assert "Item ID not found." in captured.out