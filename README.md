# 💸 Personal Expense Tracker

A terminal-based personal finance tool built with Python. Track your daily expenses, categorize them, analyze spending patterns, and visualize your habits through charts — all from the command line, with each user's data stored separately.

---

## Features

- **Multi-user support** — Each user gets a unique ID and their own private data file
- **Add & delete expenses** — Log expenses with amount, category, date, and description
- **Category filtering** — View expenses under any specific category instantly
- **Summary & stats** — See total spending and breakdowns by category and month
- **Charts & visualizations** — Bar chart, pie chart, and monthly trend line using Matplotlib
- **Persistent storage** — All data is saved as CSV files, no database needed
- **Re-login support** — Switch between users within the same session

---

## Project Structure

```
expense-tracker/
│
├── main.py          # Entry point — handles UI, menus, and user flow
├── tracker.py       # ExpenseTracker class — core logic, file I/O, and pandas analysis
├── expense.py       # Expense data model with serialization helpers
├── charts.py        # Matplotlib chart functions (bar, pie, monthly trend)
│
├── data/            # Auto-created folder — stores per-user CSV files
│   └── USR1234.csv  # Example: one CSV per user ID
│
└── users.json       # Stores user ID → name mappings
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| Pandas | Data analysis and CSV handling |
| Matplotlib | Chart visualizations |
| JSON | User registry storage |
| CSV | Per-user expense storage |

---


## How It Works

When you launch the app, you either register as a new user or log in with your existing User ID. New users get a generated ID like `SUJ7823` — save it for future logins.

Once logged in, a menu lets you:

1. Add an expense (amount → category → description)
2. View all recorded expenses with a running total
3. Filter expenses by category
4. Delete any expense by its number
5. View a full summary with category and monthly breakdowns
6. View charts (bar, pie, or trend line)
7. Exit or switch to another user account

All data is automatically saved to `data/<userID>.csv` after every add or delete.

---

## Expense Categories

```
Food | Transport | Shopping | Entertainment | Health | Bills | Other
```

---

## Example Session

```
========================================
     PERSONAL EXPENSE TRACKER
========================================
1. I'm a new user
2. I'm an existing user
========================================
Select (1 or 2): 1

Enter your name: Sujit

Welcome, Sujit!
Your User ID is: SUJ4821
Please save this ID to log in next time.

========================================
     PERSONAL EXPENSE TRACKER
========================================
1. Add Expense
2. View All Expenses
...
```

---

## Charts

| Chart | Description |
|---|---|
| Bar Chart | Total spending per category |
| Pie Chart | Percentage distribution of expenses |
| Monthly Trend | Line graph showing spending over months |

---
