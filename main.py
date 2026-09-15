from modules.auth import register_user, login_user
from modules.menu import list_menu, add_menu_item, update_menu_item, delete_menu_item
from modules.orders import create_order, view_user_orders, view_all_orders, cancel_order, update_order_status


def customer_menu(username: str):
    while True:
        print(f"\n=== KEROMA CUSTOMER MENU ({username}) ===")
        print("1. View Menu")
        print("2. Place Order")
        print("3. View My Orders")
        print("4. Cancel Order")
        print("5. Logout")

        choice = input("Select an option: ")

        if choice == "1":
            list_menu()
        elif choice == "2":
            list_menu()
            raw_ids = input(
                "\nEnter Item IDs to order (separated by commas, e.g., 1,2): ")
            try:
                item_ids = [int(i.strip())
                            for i in raw_ids.split(",") if i.strip().isdigit()]
                if item_ids:
                    create_order(username, item_ids)
                else:
                    print("No valid item IDs entered.")
            except ValueError:
                print("Invalid input.")
        elif choice == "3":
            view_user_orders(username)
        elif choice == "4":
            view_user_orders(username)
            try:
                order_id = int(input("Enter Order ID to cancel: "))
                cancel_order(order_id, username)
            except ValueError:
                print("Invalid Order ID.")
        elif choice == "5":
            break


def staff_menu(username: str):
    while True:
        print(f"\n=== KEROMA STAFF MENU ({username}) ===")
        print("1. View Menu")
        print("2. Add Menu Item")
        print("3. Update Menu Item")
        print("4. Delete Menu Item")
        print("5. View All Customer Orders")
        print("6. Update Order Status")
        print("7. Logout")

        choice = input("Select an option: ")

        if choice == "1":
            list_menu()
        elif choice == "2":
            name = input("Enter meal name: ")
            try:
                price = float(input("Enter price: "))
                add_menu_item(name, price)
            except ValueError:
                print("Invalid price.")
        elif choice == "3":
            list_menu()
            try:
                item_id = int(input("Enter item ID to update: "))
                name_input = input(
                    "Enter new name (leave blank to keep current): ").strip()
                price_input = input(
                    "Enter new price (leave blank to keep current): ").strip()

                name = name_input if name_input else None
                price = float(price_input) if price_input else None

                update_menu_item(item_id, name, price)
            except ValueError:
                print("Invalid numeric input.")
        elif choice == "4":
            list_menu()
            try:
                item_id = int(input("Enter item ID to delete: "))
                delete_menu_item(item_id)
            except ValueError:
                print("Invalid Item ID.")
        elif choice == "5":
            view_all_orders()
        elif choice == "6":
            view_all_orders()
            try:
                order_id = int(input("Enter Order ID to update: "))
                status = input(
                    "Enter new status (Pending/Preparing/Ready/Completed): ")
                update_order_status(order_id, status)
            except ValueError:
                print("Invalid Order ID.")
        elif choice == "7":
            break


def main():
    while True:
        print("\n=== WELCOME TO KEROMA CLI ===")
        print("1. Register Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            print("Select Role: 1. Customer  2. Management Staff")
            role_choice = input("Option: ")
            role = "Management Staff" if role_choice == "2" else "Customer"
            success, msg = register_user(username, password, role)
            print(msg)

        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            success, user = login_user(username, password)
            if success and user:
                u_name = user["username"]
                u_role = user["role"]

                print(f"\nLogin successful! Welcome {u_name} ({u_role})")
                if u_role in ["Management Staff", "Admin"]:
                    staff_menu(u_name)
                else:
                    customer_menu(u_name)
            else:
                print("\nInvalid username or password.")
        elif choice == "3":
            print("Thank you for choosing Keroma, Goodbye!")
            break


if __name__ == "__main__":
    main()