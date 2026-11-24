from dataclasses import dataclass

@dataclass(frozen=True)

class Transaction: 
    id: str
    date: str
    kind: str
    amount: float
    category: str
    currency: str

    @property
    def signed_amount(self) -> float: 
        return self.amount if self.kind == "income" else -self.amount
    