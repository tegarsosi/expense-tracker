import argparse
import csv
import json
from datetime import datetime
from typing import Any

MONTHS = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

def load_expenses():
    try:
        with open("expenses.json", "r") as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = []
    return expenses

def get_id():
    expenses = load_expenses()
    return max(expense["ID"] for expense in expenses) + 1 if expenses else 1

def save_expense(expenses):
    with open("expenses.json", "w") as f:
        json.dump(expenses, f)

def add_expense(
    description: str,
    amount: float,
    category: str
):
    expenses = load_expenses()
    if amount <= 0:
        print("Amount must be greater than 0")
        return
    id = get_id()
    expenses.append(
        {
            "ID": id,
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Description": description,
            "Amount": amount,
            "Category": category
        }
    )
    save_expense(expenses)
    print(f"Expense added successfully (ID: {id})")

def update_expense(
    id: int,
    description: str = None,
    amount: float = None,
    category: str = None
):
    expenses = load_expenses()
    if amount is not None and amount <= 0:
        print("Amount must be greater than 0")
        return
    for expense in expenses:
        if expense["ID"] == id:
            if description:
                expense["Description"] = description
            if amount:
                expense["Amount"] = amount
            if category:
                expense["Category"] = category
            expense["Date"] = datetime.now().strftime("%Y-%m-%d")
            break
    else:
        print(f"Expense not found (ID: {id})")
        return
    save_expense(expenses)
    print(f"Expense updated successfully (ID: {id})")

def list_expenses(month: int = None, category: str = None):
    expenses = load_expenses()
    if month:
        expenses = [e for e in expenses if datetime.strptime(e["Date"], "%Y-%m-%d").month == month]
    if category:
        expenses = [e for e in expenses if e["Category"] == category]
    if len(expenses) < 1:
        print("No entry")
        return
    
    print("ID".ljust(5) + "Date".ljust(15) + "Description".ljust(20) + "Amount".ljust(10) + "Category".ljust(15))
    for expense in expenses:
        print(
            str(expense["ID"]).ljust(5) +
            expense["Date"].ljust(15) +
            expense["Description"].ljust(20) +
            str(expense["Amount"]).ljust(10) +
            expense["Category"].ljust(15)
        )

def sum_expenses(month: int = None, category: str = None):
    expenses = load_expenses()
    if month:
        expenses = [e for e in expenses if datetime.strptime(e["Date"], "%Y-%m-%d").month == month]
    if category:
        expenses = [e for e in expenses if e["Category"] == category]
    if len(expenses) < 1:
        print("No entry to sum")
        return
    
    total = 0
    for expense in expenses:
        total += expense["Amount"]

    if month:
        print(f"Total expenses for {MONTHS[str(month)]}: €{total}")
    else:
        print(f"Total expenses: €{total}")

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

def export_to_csv(name: str):
    expenses = load_expenses()
    if not expenses:
        print("No data to export!")
        return
    fieldnames = list(expenses[0].keys())
    with open(name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)
    
    print(f"Successfully saved to {name}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # add subcommand
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", type=str, required=True)
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", type=str, required=True)

    # update subcommand
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", type=int, required=True)
    update_parser.add_argument("--description", type=str, required=False)
    update_parser.add_argument("--amount", type=float, required=False)
    update_parser.add_argument("--category", type=str, required=False)

    # delete subcommand
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    # list subcommand
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--month", type=int, required=False)
    list_parser.add_argument("--category", type=str, required=False)

    # summary subcommand
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", type=int, required=False)
    summary_parser.add_argument("--category", type=str, required=False)

    # export-to-csv subcommand
    export_parser = subparsers.add_parser("export-to-csv")
    export_parser.add_argument("--name", type=str, required=True)

    # parse
    args = parser.parse_args()
    if args.command:
        if args.command == "add":
            add_expense(args.description, args.amount, args.category)
        elif args.command == "update":
            update_expense(args.id, args.description, args.amount, args.category)
        elif args.command == "delete":
            delete_expense(args.id)
        elif args.command == "list":
            list_expenses(args.month, args.category)
        elif args.command == "summary":
            sum_expenses(args.month, args.category)
        elif args.command == "export-to-csv":
            export_to_csv(args.name)
    else:
        print("Usage: python expense_tracker.py <command> --<subcommand> <args>")
        print("Commands:")
        print("  add --description <description> --amount <amount> --category <category>")
        print("  update --id <id> --description <description> --amount <amount> --category <category>")
        print("  delete --id <id>")
        print("  list")
        print("  list --month <month>")
        print("  summary")
        print("  summary --month <month>")
        print("  export-to-csv --name <filename>")