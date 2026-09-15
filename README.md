# Keroma CLI - Restaurant Management System

A modular, object-oriented Command Line Interface (CLI) application built with Python for managing restaurant operations, user authentication, menu customization, and order processing.

---

## 📌 Project Overview

**Keroma CLI** provides a dual-interface terminal application designed for two user roles:
1. **Customers:** Browse the menu, place orders, view order history, and cancel pending orders.
2. **Management Staff / Admins:** Full CRUD access to manage food items, view customer orders, and update order statuses in real-time.

The application leverages Python's Object-Oriented Programming (OOP) paradigms with structured JSON file-based persistence for storing user accounts, menu items, and order histories.

---

## 🏗️ System Architecture & Directory Structure

```text
keroma-cli/
│
├── data/                  # Persistent JSON storage
│   ├── menu.json          # Menu catalog data
│   ├── orders.json        # Order records
│   └── users.json         # User credentials and roles
│
├── modules/               # Core application logic & models
│   ├── __init__.py
│   ├── auth.py            # User login, registration, and hashing logic
│   ├── menu.py            # Menu CRUD operations and catalog management
│   ├── models.py          # OOP Data Models (User, MenuItem, Order)
│   └── orders.py          # Order creation, processing, and state updates
│
├── tests/                 # Automated pytest unit test suite
│   ├── __init__.py
│   ├── conftest.py        # Shared pytest fixtures and mock environments
│   ├── test_auth.py       # Authentication unit tests
│   ├── test_menu.py       # Menu management unit tests
│   └── test_orders.py     # Order workflow unit tests
│
├── main.py                # Application entry point & interactive CLI loop
├── pytest.ini             # Pytest configuration settings
└── README.md              # System documentation
```

---

## ✨ Features

### 🔐 User Authentication (`modules/auth.py`)
* Secure user registration and login.
* Role-based access control (`Customer` vs. `Management Staff` / `Admin`).
* Data validation against empty entries or duplicate usernames.

### 🍔 Menu Management (`modules/menu.py`)
* **Create:** Add new items with assigned category, name, price, and description.
* **Read:** Display formatted menu catalog to staff and customers.
* **Update:** Modify existing menu item attributes.
* **Delete:** Remove outdated items safely from catalog storage.

### 📦 Order Processing (`modules/orders.py`)
* Interactive order placement with automatic total calculation.
* Lifecycle tracking: `Pending` ➔ `Preparing` ➔ `Ready` ➔ `Completed`.
* Order cancellation for active pending items.
* Role-restricted order viewing (Users see their own; Staff see all).

---

## 🚀 Getting Started

### Prerequisites

* **Python:** `3.9+` installed on your machine.
* **Git:** Version control system.

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/keroma-cli.git
   cd keroma-cli
   ```

2. **Create and Activate a Virtual Environment (Recommended):**
   * **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/venv/activate
     ```
   * **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. **Install Dependencies:**
   ```bash
   pip install pytest
   ```

---

## 💻 Running the Application

Execute the entry point script from the root directory:

```bash
python main.py
```

### Navigating the Interface
* Select options by typing numbers corresponding to menu options (`1`, `2`, `3`, etc.).
* First-time users should select **Register** to create a customer account.

---

## 🧪 Running Automated Tests

The codebase includes a full automated unit test suite managed by `pytest`.

To execute all tests from the root directory:

```bash
pytest
```

### Test Flags & Variations

* **Verbose Mode (Detailed Test Cases):**
  ```bash
  pytest -v
  ```
* **Run a Specific Module:**
  ```bash
  pytest tests/test_auth.py
  ```
* **Stop Execution on First Failure:**
  ```bash
  pytest -x
  ```

---

## 👥 Collaborative Git Workflow

The project was developed across three dedicated feature branches:

1. `feature/auth-and-models` – Data models and user authentication logic.
2. `feature/menu-management` – Menu CRUD functionality and storage.
3. `feature/order-processing` – Order workflows and status transitions.