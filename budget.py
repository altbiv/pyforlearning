import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier

DATA_FILE = "budgeting_data.json"

class User:
    def __init__(self, username, password, budget=0, expenses=None, currency="INR"):
        self.username = username
        self.password = password
        self.budget = budget
        self.expenses = expenses if expenses else []
        self.currency = currency
        self.ensure_categories()
        self.model = self.train_ai_model()  # Train the AI model when the user is created

    def ensure_categories(self):
        # Add missing categories to old data
        for expense in self.expenses:
            if "category" not in expense:
                expense["category"] = "Misc"

    def set_budget(self, amount):
        if amount < 0:
            print("Budget cannot be negative.")
            return
        self.budget = amount

    def add_expense(self, name, amount, category, date_time=None):
        if amount < 0:
            print("Expense amount cannot be negative.")
            return
        expense = {"name": name, "amount": amount, "category": category}
        if date_time:
            expense["date_time"] = date_time
        self.expenses.append(expense)
        self.advanced_ai_suggestions()  # Trigger AI suggestions after adding an expense

    def view_budget(self):
        total_expenses = sum(expense["amount"] for expense in self.expenses)
        remaining_budget = self.budget - total_expenses
        print(f"\nTotal Budget: {self.currency} {self.budget}")
        print(f"Total Expenses: {self.currency} {total_expenses}")
        print(f"Remaining Budget: {self.currency} {remaining_budget}")

    def view_expenses(self):
        print("\nExpenses:")
        for expense in self.expenses:
            date_time_str = f" on {expense['date_time']}" if "date_time" in expense else ""
            print(f"{expense['name']} - {self.currency} {expense['amount']} [{expense['category']}] {date_time_str}")

    def set_currency(self, currency):
        self.currency = currency
        print(f"Currency set to {currency}")

    def clear_data(self):
        self.budget = 0
        self.expenses = []
        print("All budget data cleared.")

    def train_ai_model(self):
        # For demonstration purposes, we'll create a dummy dataset.
        # In a real-world scenario, you'd collect and preprocess actual data.
        X = np.array([
            [1000, 200], [1000, 950], [1000, 1000], [1000, 1100],
            [500, 200], [500, 450], [500, 500], [500, 600]
        ])  # Example features: [budget, total_expenses]
        y = np.array(['Within Budget', 'Close to Budget', 'Overspend', 'Overspend',
                      'Within Budget', 'Close to Budget', 'Close to Budget', 'Overspend'])  # Labels
        
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, y)
        return model

    def advanced_ai_suggestions(self):
        total_expenses = sum(expense["amount"] for expense in self.expenses)
        features = np.array([self.budget, total_expenses]).reshape(1, -1)
        
        prediction = self.model.predict(features)[0]
        
        if prediction == 'Overspend':
            print("\n[AI Suggestion] You are likely to overspend. Consider reducing expenses in non-essential categories.")
        elif prediction == 'Close to Budget':
            print("\n[AI Suggestion] You're close to your budget limit. Focus on essential expenses.")
        else:
            print("\n[AI Suggestion] You are within your budget. Keep up the good financial management!")

    def plot_expenses(self):
        print("\nChoose a graph type to visualize your expenses:")
        print("1. Bar Chart")
        print("2. Pie Chart")
        print("3. Line Chart")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            self.plot_bar_chart()
        elif choice == "2":
            self.plot_pie_chart()
        elif choice == "3":
            self.plot_line_chart()
        else:
            print("Invalid choice. Please try again.")

    def plot_bar_chart(self):
        categories = [expense['category'] for expense in self.expenses]
        amounts = [expense['amount'] for expense in self.expenses]
        plt.bar(categories, amounts)
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel(f"Amount ({self.currency})")
        plt.show()

    def plot_pie_chart(self):
        categories = [expense['category'] for expense in self.expenses]
        amounts = [expense['amount'] for expense in self.expenses]
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title("Expenses Distribution")
        plt.show()

    def plot_line_chart(self):
        dates = [expense['date_time'] for expense in self.expenses if 'date_time' in expense]
        amounts = [expense['amount'] for expense in self.expenses if 'date_time' in expense]
        plt.plot(dates, amounts)
        plt.title("Expenses Over Time")
        plt.xlabel("Date")
        plt.ylabel(f"Amount ({self.currency})")
        plt.xticks(rotation=45)
        plt.show()

def save_data(users):
    data = {username: vars(user) for username, user in users.items()}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            users = {username: User(**user_data) for username, user_data in data.items()}
            return users
    return {}

def register(users):
    username = input("Enter a username: ").strip()
    if username in users:
        print("Username already exists!")
        return
    password = input("Enter a password: ").strip()
    users[username] = User(username, password)
    save_data(users)
    print("User registered successfully!")

def login(users):
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    if username in users and users[username].password == password:
        print(f"Welcome back, {username}!")
        return users[username]
    else:
        print("Invalid username or password!")
        return None

def main():
    users = load_data()
    current_user = None

    while True:
        if current_user:
            print("\n1. Set Budget")
            print("2. Add Expense")
            print("3. View Budget")
            print("4. View Expenses")
            print("5. Change Currency")
            print("6. Clear Budget Data")
            print("7. Plot Expenses")
            print("8. Logout")
            print("9. Help")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                amount = float(input(f"Enter your budget amount in {current_user.currency}: ").strip())
                current_user.set_budget(amount)
                save_data(users)
                print(f"Budget set to {current_user.currency} {amount}")
            elif choice == "2":
                name = input("Enter the expense name: ").strip()
                amount = float(input(f"Enter the expense amount in {current_user.currency}: ").strip())
                print("Select a category:")
                categories = ["Food", "Utility Bills", "Transport", "Shopping", "Misc"]
                for i, category in enumerate(categories, 1):
                    print(f"{i}. {category}")
                category_choice = int(input("Choose a category number: ").strip())
                category = categories[category_choice - 1]

                add_date_time = input("Do you want to add the date and time for this expense? (y/n): ").strip().lower()
                date_time = None
                if add_date_time == "y":
                    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                current_user.add_expense(name, amount, category, date_time)
                save_data(users)
                print(f"Added expense: {name} - {current_user.currency} {amount} [{category}]")
            elif choice == "3":
                current_user.view_budget()
            elif choice == "4":
                current_user.view_expenses()
            elif choice == "5":
                currency = input("Enter the new currency (e.g., INR, USD, EUR): ").strip()
                current_user.set_currency(currency)
                save_data(users)
            elif choice == "6":
                confirmation = input("Are you sure you want to clear all budget data? (y/n): ").strip().lower()
                if confirmation == "y":
                    current_user.clear_data()
                    save_data(users)
            elif choice == "7":
                current_user.plot_expenses()
            elif choice == "8":
                current_user = None
                print("Logged out successfully!")
            elif choice == "9":
                print("\nHelp Menu:")
                print("1. Set Budget: Set your budget amount.")
                print("2. Add Expense: Add an expense with a name, amount, and category.")
                print("3. View Budget: View your total budget, expenses, and remaining budget.")
                print("4. View Expenses: View all recorded expenses.")
                print("5. Change Currency: Change the currency used in the app.")
                print("6. Clear Budget Data: Clear all budget data.")
                print("7. Plot Expenses: Visualize your expenses with different types of charts.")
                print("8. Logout: Log out of the current session.")
            else:
                print("Invalid option. Please try again.")
        else:
            print("\n1. Register")
            print("2. Login")
            print("3. Help")
            print("4. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                register(users)
            elif choice == "2":
                current_user = login(users)
            elif choice == "3":
                print("\nHelp Menu:")
                print("1. Register: Create a new account.")
                print("2. Login: Log in to your existing account.")
                print("3. Help: View the help menu.")
                print("4. Exit: Exit the application.")
            elif choice == "4":
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
