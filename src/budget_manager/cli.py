from pathlib import Path
from .validation import validate_create_transaction
from .services import BudgetService
from .storage import load_transaction, save_transactions

project_root = Path(__file__).resolve().parents[2]
seed_file = project_root / "data" / "sample_transactions.csv"
data_file = project_root / "data" / "transactions.csv"

def main() -> None: 
    source = data_file if data_file.exists() else seed_file
    initial_txs, load_errors = load_transaction(source)
    for err in load_errors:
        print(f"[warning] Skipped invalid record -> {err}")
    if load_errors: 
        print(f"[warning] {len(load_errors)} invalid record(s) will not be saved to {data_file.name}.")

    service = BudgetService(initial_txs)

    while True: 
        print("\n--- Personal Budget Manager ---")
        print("1. Add transaction")
        print("2. List transactions")
        print("3. Show summary report")
        print("q. Save & Quit")

        choice = input("Select an option between 1, 2, 3, or q: ").strip().lower()

        if choice == "1": 
            try: 
                tx_id = input("ID (e.g. T005): ")
                date_str = input("Date (YYYY-MM-DD): ")
                kind = input("Kind (expense/income): ")
                amount = input("Amount: ")
                category = input("Category (food/transport/salary/rent/entertainment/other): ")
                currency = input("Currency (EUR/USD/GBP): ")

                tx = validate_create_transaction(tx_id, date_str, kind, amount, category, currency)
                service.add(tx)
                save_transactions(data_file, service.list_all())
                print("Transaction added and saved.")
            except ValueError as e: 
                print(f"Error: {e}")

        elif choice == "2": 
            txs = service.list_all()
            if not txs: 
                print("No transaction found.")
            for tx in txs: 
             print(f"{tx.id} | {tx.date} | {tx.kind:<7} | {tx.amount:>8.2f} {tx.currency} | {tx.category}")
        elif choice == "3": 
            report = service.summary()
            if not report: 
                print("No transaction found.")
            for currency, totals in sorted(report.items()):
                print(f"\n[{currency}]")
                print(f"Total Income:    {totals['total_income']:.2f}")
                print(f"Total Expenses:  {totals['total_expenses']:.2f}")
                print(f"Net Balance:     {totals['net_balance']:.2f}")
           

        elif choice == "q": 
            save_transactions(data_file, service.list_all())
            print("Goodbye!")
            break 
        else: 
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()


     
