import json
from datetime import datetime

def load_expenses():
    try:
        with open("expenses.json", "r") as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = []
    return expenses

def get_id():
    expenses = load_expenses()
    return max(expenses["id"] for expense in expenses) + 1 if expenses else 1

def save_expense(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f)

def add_expense(description: str, amount: int):
    expenses = load_expenses()
    id = get_id()
    expenses.append(
        {
            "ID": id,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Description": description,
            "Amount": amount,
        }
    )
    save_expense(expenses)
    print(f"Expense added successfully (ID: {id})")

def list_expenses():

def expense_summary():

def delete_expense():