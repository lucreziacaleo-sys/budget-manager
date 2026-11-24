import pytest

from budget_manager.services import BudgetService
from budget_manager.storage import load_transaction, save_transactions
from budget_manager.validation import validate_create_transaction

def make_tx(tx_id="T001", date="2026-09-04", kind="expense", amount="18.50",
            category="food", currency="EUR"):
    return validate_create_transaction(tx_id, date, kind, amount, category, currency)


def test_valid_transaction_is_created():
    tx = make_tx()
    assert tx.id == "T001"
    assert tx.amount == 18.50
    assert tx.signed_amount == -18.50

def test_zero_amount_is_rejected():
    with pytest.raises(ValueError, match="amount must be > 0"):
        make_tx(amount="0")

def test_smallest_positive_amount_is_accepted():
    assert make_tx(amount="0.01").amount == 0.01

def test_impossible_date_is_rejected():
    with pytest.raises(ValueError, match="real date"):
        make_tx(date="2026-13-45")

@pytest.mark.parametrize("bad", ["nan", "inf"])
def test_nan_and_inf_are_rejected(bad):
    with pytest.raises(ValueError, match="finite number"):
        make_tx(amount=bad)

def test_summary_keeps_currencies_separate():
    service = BudgetService([
        make_tx("T1", kind="income", amount="100", category="salary", currency="EUR"),
        make_tx("T2", amount="30", currency="EUR"),
        make_tx("T3", amount="10", currency="USD"),
    ])
    report = service.summary()
    assert report["EUR"]["net_balance"] == 70.0
    assert report["USD"]["total_expenses"] == 10.0


def test_save_then_load_round_trip(tmp_path):
    path = tmp_path / "tx.csv"
    original = [make_tx("T1"), make_tx("T2", kind="income", amount="1200", category="salary")]
    save_transactions(path, original)
    loaded, errors = load_transaction(path)
    assert errors == []
    assert loaded == original
    

def test_load_catches_duplicates(tmp_path):
    path = tmp_path / "tx.csv"
    path.write_text(
        "id,date,kind,amount,category,currency\n"
        "T1,2026-09-04,expense,10,food,EUR\n"
        "T1,2026-09-05,expense,4,food,EUR\n",
        encoding="utf-8",
    )
    loaded, errors = load_transaction(path)
    assert len(loaded) == 1
    assert errors == ["Row 3: duplicate id 'T1'."]