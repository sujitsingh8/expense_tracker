from tracker import ExpenseTracker
from expense import Expense
import charts
import json
import os
import random
import string


USERS_FILE = 'users.json'


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def generate_user_id(name, existing_ids):
    prefix = ''.join(c for c in name[:3].upper() if c.isalpha()).ljust(3, 'X')
    while True:
        digits = ''.join(random.choices(string.digits, k=4))
        uid = prefix + digits
        if uid not in existing_ids:
            return uid


def user_login():
    print("\n" + "=" * 40)
    print("     PERSONAL EXPENSE TRACKER")
    print("=" * 40)
    print("1. I'm a new user")
    print("2. I'm an existing user")
    print("=" * 40)

    while True:
        choice = input("Select (1 or 2): ").strip()
        if choice in ('1', '2'):
            break
        print("Please enter 1 or 2.")

    users = load_users()

    if choice == '1':
        # New user registration
        while True:
            name = input("\nEnter your name: ").strip()
            if name:
                break
            print("Name cannot be empty.")

        user_id = generate_user_id(name, users)
        users[user_id] = name
        save_users(users)

        print(f"\nWelcome, {name}!")
        print(f"Your User ID is: {user_id}")
        print("Please save this ID to log in next time.")

        return user_id, name

    else:
        # Existing user login
        while True:
            user_id = input("\nEnter your User ID: ").strip().upper()
            if user_id in users:
                name = users[user_id]
                print(f"\nWelcome back, {name}!")
                return user_id, name
            else:
                print("User ID not found. Please check and try again.")


tracker = None


def print_menu():
    print("\n" + "=" * 40)
    print("     PERSONAL EXPENSE TRACKER")
    print("=" * 40)
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. View by Category")
    print("4. Delete an Expense")
    print("5. Summary & Stats")
    print("6. Show Charts")
    print("7. Exit")
    print("8. relogin")
    print("=" * 40)


def add_expense():
    print("\n-- Add Expense --")
    print("(Enter 0 at any prompt to go back to main menu)")

    while True:
        # Get amount
        while True:
            raw = input("\nAmount (₹): ").strip()
            if raw == "0":
                print("Back to main menu.")
                return
            try:
                amount = float(raw)
                if amount <= 0:
                    print("Amount must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        # Get category
        print("\nCategories:")
        for i, cat in enumerate(Expense.CATEGORIES, start=1):
            print(f"  {i}. {cat}")
        while True:
            raw = input("Choose category number (or 0 to go back): ").strip()
            if raw == "0":
                print("Back to main menu.")
                return
            try:
                cat_index = int(raw)
                if 1 <= cat_index <= len(Expense.CATEGORIES):
                    category = Expense.CATEGORIES[cat_index - 1]
                    break
                print(f"Enter a number between 1 and {len(Expense.CATEGORIES)}.")
            except ValueError:
                print("Please enter a number.")

        description = input("Description: ").strip()
        if not description:
            description = "No description"

        tracker.add(amount, category, description)
        print(f"Expense of ₹{amount:.2f} added under '{category}'. Add another or enter 0 to go back.")


def view_all():
    expenses = tracker.all_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    print(f"\n-- All Expenses ({len(expenses)} total) --")
    for i, expense in enumerate(expenses, start=1):
        print(f"{i:>3}. {expense}")

    print(f"\n     Total Spent: ₹{tracker.total_spent():.2f}")


def view_by_category():
    while True:
        print("\nCategories:")
        for i, cat in enumerate(Expense.CATEGORIES, start=1):
            print(f"  {i}. {cat}")

        raw = input("Choose category number (or 0 to go back): ").strip()
        if raw == "0":
            return
        try:
            cat_index = int(raw)
            if not (1 <= cat_index <= len(Expense.CATEGORIES)):
                print(f"Enter a number between 1 and {len(Expense.CATEGORIES)}.")
                continue
            category = Expense.CATEGORIES[cat_index - 1]
        except ValueError:
            print("Please enter a number.")
            continue

        results = tracker.by_category(category)
        if not results:
            print(f"No expenses found under '{category}'.")
            continue

        total = sum(e.amount for e in results)
        print(f"\n-- {category} Expenses --")
        for i, expense in enumerate(results, start=1):
            print(f"{i:>3}. {expense}")
        print(f"\n     Total: ₹{total:.2f}")


def delete_expense():
    while True:
        view_all()
        if not tracker.all_expenses():
            return

        try:
            index = int(input("\nEnter expense number to delete (or 0 to go back): "))
            if index == 0:
                return
            removed = tracker.delete(index)
            print(f"Deleted: {removed}")
        except ValueError:
            print("Please enter a valid number.")
        except IndexError as e:
            print(e)


def show_summary():
    if not tracker.all_expenses():
        print("\nNo expenses recorded yet.")
        return

    print("\n-- Summary --")
    print(f"Total Spent: ₹{tracker.total_spent():.2f}")

    print("\nBy Category:")
    cat_summary = tracker.category_summary()
    for category, amount in cat_summary.items():
        print(f"  {category:<15} ₹{amount:.2f}")

    print("\nBy Month:")
    monthly = tracker.monthly_summary()
    for month, amount in monthly.items():
        print(f"  {str(month):<12} ₹{amount:.2f}")


def show_charts():
    if not tracker.all_expenses():
        print("\nNo expenses to chart yet.")
        return

    while True:
        print("\n-- Charts --")
        print("1. Bar Chart (by Category)")
        print("2. Pie Chart (by Category)")
        print("3. Monthly Trend")
        print("0. Back to Main Menu")

        try:
            choice = int(input("Choose chart (0-3): "))
        except ValueError:
            print("Invalid choice.")
            continue

        if choice == 0:
            return

        cat_summary = tracker.category_summary()
        monthly = tracker.monthly_summary()

        if choice == 1:
            charts.show_category_bar(cat_summary)
        elif choice == 2:
            charts.show_category_pie(cat_summary)
        elif choice == 3:
            charts.show_monthly_trend(monthly)
        else:
            print("Invalid choice.")


def main():
    global tracker
    user_id, name = user_login()
    tracker = ExpenseTracker(user_id)

    while True:
        print_menu()

        try:
            choice = int(input("Choose an option (1-8): "))
        except ValueError:
            print("Please enter a number between 1 and 8.")
            continue

        if choice == 1:
            add_expense()
        elif choice == 2:
            view_all()
        elif choice == 3:
            view_by_category()
        elif choice == 4:
            delete_expense()
        elif choice == 5:
            show_summary()
        elif choice == 6:
            show_charts()
        elif choice == 7:
            print("Goodbye! Keep tracking your expenses.")
            break
        elif choice == 8:
            user_id, name = user_login()
            tracker = ExpenseTracker(user_id)
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == '__main__':
    main()