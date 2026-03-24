import argparse
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

def update_expense(id: str, description: str = None, amount: int = None):
    expenses = load_expenses()
    for expense in expenses:
        if expense["ID"] == int(id):
            if description:
                expense["Description"] = description
            if amount:
                expense["Amount"] = amount
            expense["Date"] = datetime.now().strftime("%Y-%m-%d")
            break
    else:
        print(f"Expense not found (ID: {id})")
        return
    save_expense(expenses)
    print(f"Expense updated successfully (ID: {id})")

# def list_expenses():

# def expense_summary():

def delete_expense(id: int):
    expenses = load_expenses()
    for expense in expenses:
        if expense["ID"] == id:
            expenses.remove(expense)
            break
    else:
        print(f"Expense entry not found (ID: {id})")
        return
    save_expense(expenses)
    print(f"Expense deleted successfully (ID: {id})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # add subcommand
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", type=str, required=True)
    add_parser.add_argument("--amount", type=int, required=True)

    # update subcommand
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", type=int, required=True)
    update_parser.add_argument("--description", type=str, required=False)
    update_parser.add_argument("--amount", type=int, required=False)

    # delete subcommand
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    # parse
    args = parser.parse_args()
    if args.command == "add":
        add_expense(args.description, args.amount)
    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)
    elif args.command == "delete":
        delete_expense(args.id)