# Expense Tracker CLI

https://roadmap.sh/projects/expense-tracker

A simple expense tracker application to manage your finances.

---

## Requirements

- Python 3.x
- No external dependencies

---

## How to Run
```bash
python expense_tracker.py <command> <arguments>
```

---

## Commands

| Command | Arguments | Description |
|---|---|---|
| `add` | `--description`, `--amount`, `--category` | Add a new expense |
| `update` | `--id`, `[--description]`, `[--amount]`, `[--category]` | Update an existing expense |
| `delete` | `--id` | Remove an expense entry |
| `list` | `[--month]`, `[--category]` | List all expenses (optional filters) |
| `summary` | `[--month]`, `[--category]` | Total all expenses (optional filters) |
| `export-to-csv` | `--name` | Export data to csv file |

---

## Example Usage
```bash
# Add an expense
python expense_tracker.py add --description "Coffee" --amount 4.5 --category "Food"

# Update an expense
python expense_tracker.py update --id 1 --amount 5.0

# Remove an expense
python expense_tracker.py delete --id 1

# List all expenses
python expense_tracker.py list

# View summary for a specific month (March)
python expense_tracker.py summary --month 3

# Export data
python expense_tracker.py export-to-csv --name my_finances.csv
```

---

## Data Properties

Each expense is stored in `expenses.json` with the following properties:
```json
{
    "ID": 1,
    "Date": "2026-03-24",
    "Description": "Lunch",
    "Amount": 15.0,
    "Category": "Food"
}
```