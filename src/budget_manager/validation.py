import math 
from datetime import date
from .models import Transaction

allowed_kinds = {"expense", "income"}
allowed_categories = {"food", "transport", "salary", "rent", "entertainment", "other"}
allowed_currencies = {"EUR", "USD", "GBP"}

def validate_create_transaction(
    tx_id: str,
    date_str: str,
    kind: str,
    raw_amount: str | float,
    category: str,
    currency: str,
    context: str = ""
) -> Transaction: 
    prefix = f"{context}: " if context else ""

    clean_id = tx_id.strip()
    if not clean_id: 
        raise ValueError(f"{prefix}id cannot be empty.")

    clean_date = date_str.strip()
    try: 
        date.fromisoformat(clean_date)
    except ValueError:
        raise ValueError(f"{prefix}date must be a real date in YYYY-MM-DD format.")

    clean_kind = kind.strip()
    if clean_kind not in allowed_kinds: 
        raise ValueError(f"{prefix}kind must be one of {allowed_kinds}.")

    try: 
        amount = float(raw_amount)
    except (ValueError, TypeError): 
        raise ValueError(f"{prefix}amount must be a valid number.")
    if math.isnan(amount) or math.isinf(amount):
        raise ValueError(f"{prefix}amount must be a finite number.")
    if amount <= 0: 
        raise ValueError(f"{prefix}amount must be > 0.")

    clean_category = category.strip()
    if clean_category not in allowed_categories: 
        raise ValueError(f"{prefix}unknown category '{clean_category}'. Allowed: {allowed_categories}.")

    clean_currency = currency.strip()
    if clean_currency not in allowed_currencies: 
        raise ValueError(f"{prefix}currency must be one of {allowed_currencies}.")

    return Transaction(
        id=clean_id,
        date=clean_date,
        kind=clean_kind,
        amount=amount,
        category=clean_category,
        currency=clean_currency
    )
    