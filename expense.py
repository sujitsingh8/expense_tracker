from datetime import date


class Expense:
    # Valid categories for an expense
    CATEGORIES = ['Food', 'Transport', 'Shopping', 'Entertainment', 'Health', 'Bills', 'Other']

    def __init__(self, amount, category, description, expense_date=None):
        self.amount = float(amount)
        self.category = category
        self.description = description
        # If no date given, use today's date
        self.expense_date = expense_date if expense_date else str(date.today())

    def __str__(self):
        return f"[{self.expense_date}] {self.category} | ₹{self.amount:.2f} | {self.description}"

    def to_dict(self):
        # Convert to dictionary so it can be saved as a CSV row
        return {
            'date': self.expense_date,
            'category': self.category,
            'amount': self.amount,
            'description': self.description
        }

    @staticmethod
    def from_dict(row):
        # Create an Expense object from a CSV row (dictionary)
        return Expense(
            amount=row['amount'],
            category=row['category'],
            description=row['description'],
            expense_date=row['date']
        )