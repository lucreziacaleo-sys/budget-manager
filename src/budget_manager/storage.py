import csv 
from pathlib import Path
from .models import Transaction
from .validation import validate_create_transaction

field_names = ["id", "date", "kind", "amount", "category", "currency"]

def load_transaction(filepath: Path) -> tuple[list[Transaction], list[str]]: 
    valid: list[Transaction] = []
    errors: list[str] = []
    seen_ids: set[str] = set()

    if not filepath.exists():
        return valid, errors

    with filepath.open("r", encoding="utf-8", newline="") as f: 
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2): 
            try: 
                tx = validate_create_transaction(
                    tx_id=row.get("id", ""),
                    date_str=row.get("date", ""),
                    kind=row.get("kind", ""),
                    raw_amount=row.get("amount", ""),
                    category=row.get("category", ""),
                    currency=row.get("currency", ""),
                    context=f"Row {row_num}"
                )
                if tx.id in seen_ids: 
                    raise ValueError(f"Row {row_num}: duplicate id '{tx.id}'.")
                seen_ids.add(tx.id)
                valid.append(tx)
            except ValueError as e: 
                errors.append(str(e))

    return valid, errors 

def save_transactions(filepath: Path, transactions: list[Transaction]) -> None: 
    filepath.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = filepath.with_suffix(".tmp")

    with tmp_path.open("w", encoding="utf-8", newline="") as f: 
        writer = csv.DictWriter(f, field_names)
        writer.writeheader()
        for tx in transactions: 
            writer.writerow({
                "id": tx.id, 
                "date": tx.date, 
                "kind": tx.kind,
                "amount": f"{tx.amount:.2f}",
                "category": tx.category, 
                "currency": tx.currency
            })

    tmp_path.replace(filepath)



