from .models import Transaction 

class BudgetService: 
    def __init__(self, initial_transactions: list[Transaction] | None = None):
        self._transactions: list[Transaction] = list(initial_transactions) if initial_transactions else []

    def add(self, tx: Transaction) -> None: 
        if any(existing.id == tx.id for existing in self._transactions): 
            raise ValueError(f"Transaction ID '{tx.id}' already exists.")
        self._transactions.append(tx)

    def list_all(self) -> list[Transaction]: 
        return list(self._transactions)

    def filter_by_category(self, category: str) -> list[Transaction]: 
        target = category.strip()
        return[tx for tx in self._transactions if tx.category == target]

    def summary(self) -> dict[str, dict[str, float]]:
        report: dict[str, dict[str, float]] = {}
        for tx in self._transactions:
            totals = report.setdefault(
                tx.currency,
                {"total_income": 0.0, "total_expenses": 0.0, "net_balance": 0.0},
            )
            if tx.kind == "income":
                totals["total_income"] += tx.amount
            else:
                totals["total_expenses"] += tx.amount
            totals["net_balance"] += tx.signed_amount
        return report