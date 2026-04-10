import matplotlib.pyplot as plt


def show_category_bar(category_summary):
    if category_summary.empty:
        print("No data to plot.")
        return

    categories = category_summary.index.tolist()
    amounts = category_summary.values.tolist()

    plt.figure(figsize=(8, 5))
    bars = plt.bar(categories, amounts, color='steelblue', edgecolor='black')

    # Add amount label on top of each bar
    for bar, amount in zip(bars, amounts):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 10,
            f'₹{amount:.0f}',
            ha='center', va='bottom', fontsize=10
        )

    plt.title('Spending by Category', fontsize=14)
    plt.xlabel('Category')
    plt.ylabel('Amount (₹)')
    plt.tight_layout()
    plt.show()


def show_category_pie(category_summary):
    if category_summary.empty:
        print("No data to plot.")
        return

    plt.figure(figsize=(7, 7))
    plt.pie(
        category_summary.values,
        labels=category_summary.index,
        autopct='%1.1f%%',
        startangle=140
    )
    plt.title('Expense Distribution by Category', fontsize=14)
    plt.tight_layout()
    plt.show()


def show_monthly_trend(monthly_summary):
    if monthly_summary.empty:
        print("No data to plot.")
        return

    months = [str(m) for m in monthly_summary.index]
    amounts = monthly_summary.values.tolist()

    plt.figure(figsize=(9, 5))
    plt.plot(months, amounts, marker='o', color='tomato', linewidth=2, markersize=7)

    # Label each point
    for i, (month, amount) in enumerate(zip(months, amounts)):
        plt.text(i, amount + 20, f'₹{amount:.0f}', ha='center', fontsize=9)

    plt.title('Monthly Spending Trend', fontsize=14)
    plt.xlabel('Month')
    plt.ylabel('Total Spent (₹)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
