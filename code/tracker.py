import pandas as pd
import os
from expense import Expense


class ExpenseTracker:

    def __init__(self, user_id):
        self.FILE = os.path.join('data', f'{user_id}.csv')
        os.makedirs('data', exist_ok=True)
        self.expenses = []
        self._load()

    # ── File I/O ─────────────────────────────────────────────────────────────

    def _load(self):
        # Load expenses from CSV if file exists
        if os.path.exists(self.FILE):
            try:
                df = pd.read_csv(self.FILE)
                self.expenses = [Expense.from_dict(row) for _, row in df.iterrows()]
            except Exception:
                self.expenses = []

    def _save(self):
        # Save all expenses to CSV
        if self.expenses:
            df = pd.DataFrame([e.to_dict() for e in self.expenses])
            df.to_csv(self.FILE, index=False)
        else:
            # If no expenses, write an empty file with headers
            pd.DataFrame(columns=['date', 'category', 'amount', 'description']).to_csv(self.FILE, index=False)

    # ── Core Operations ───────────────────────────────────────────────────────

    def add(self, amount, category, description):
        expense = Expense(amount, category, description)
        self.expenses.append(expense)
        self._save()

    def delete(self, index):
        # index is 1-based (as shown to user)
        if 1 <= index <= len(self.expenses):
            removed = self.expenses.pop(index - 1)
            self._save()
            return removed
        else:
            raise IndexError("Invalid expense number.")

    def all_expenses(self):
        return self.expenses

    def by_category(self, category):
        return [e for e in self.expenses if e.category.lower() == category.lower()]

    # ── Pandas Analysis ───────────────────────────────────────────────────────

    def _to_dataframe(self):
        if not self.expenses:
            return pd.DataFrame(columns=['date', 'category', 'amount', 'description'])
        df = pd.DataFrame([e.to_dict() for e in self.expenses])
        df['amount'] = pd.to_numeric(df['amount'])
        df['date'] = pd.to_datetime(df['date'])
        return df

    def total_spent(self):
        df = self._to_dataframe()
        return df['amount'].sum() if not df.empty else 0

    def category_summary(self):
        df = self._to_dataframe()
        if df.empty:
            return pd.Series(dtype=float)
        return df.groupby('category')['amount'].sum().sort_values(ascending=False)

    def monthly_summary(self):
        df = self._to_dataframe()
        if df.empty:
            return pd.Series(dtype=float)
        df['month'] = df['date'].dt.to_period('M')
        return df.groupby('month')['amount'].sum().sort_index()
