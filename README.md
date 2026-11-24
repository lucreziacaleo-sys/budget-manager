# Personal Budget Manager — Release 1

A command-line app to add, list and summarize personal transactions, with validation
at every entry point and saving to a CSV file.

## Setup

Requires **Python 3.10 or newer**. The app itself needs no extra packages; the tests need `pytest`.

```bash
cd budget-manager
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pytest
```

## Run

From the project folder:

```bash
PYTHONPATH=src python -m budget_manager.cli
```

Windows (PowerShell):

```powershell
$env:PYTHONPATH="src"; python -m budget_manager.cli
```

## How the data files work

| File | Role |
|---|---|
| `data/sample_transactions.csv` | **Read-only sample.** Used only on the first run. It has 5 valid rows and 10 invalid rows, so you can see the validation rules. It is never overwritten. |
| `data/transactions.csv` | **Your data.** Created the first time you save (after adding a transaction or on quit). Loaded on every later run. |

To start over from the sample data, delete `data/transactions.csv`.

Invalid rows are skipped when the file is loaded. Each one is reported with its row number
and the reason, and the app warns that they will not be saved, so nothing disappears
without the user knowing.

## Example session

```
[warning] Skipped invalid record -> Row 7: amount must be > 0.
[warning] Skipped invalid record -> Row 9: date must be a real date in YYYY-MM-DD format.
...
[warning] 10 invalid record(s) will not be saved to transactions.csv.

--- Personal Budget Manager ---
1. Add transaction
2. List transactions
3. Show summary report
q. Save & Quit
Choose 1, 2, 3 or q: 1
ID (e.g. T005): T020
Date (YYYY-MM-DD): 2026-11-20
Kind (expense/income): expense
Amount: 20
Category (food/transport/salary/rent/entertainment/other): food
Currency (EUR/USD/GBP): EUR
Transaction added and saved.

Choose 1, 2, 3 or q: 3

[EUR]
Total Income:    1500.00
Total Expenses:  700.80
Net Balance:     799.20

[USD]
Total Income:    0.00
Total Expenses:  25.00
Net Balance:     -25.00
```

## Validation rules

| Field | Rule | Example of rejected input → message |
|---|---|---|
| `id` | Not empty, unique (checked when adding **and** when loading) | `""` → `id cannot be empty.` · second `T001` → `duplicate id 'T001'.` |
| `date` | A real calendar date, `YYYY-MM-DD` | `2026-13-45` → `date must be a real date in YYYY-MM-DD format.` |
| `kind` | `expense` or `income` | `refund` → `kind must be one of [...]` |
| `amount` | A finite number greater than 0 | `0`, `-5` → `amount must be > 0.` · `nan`, `inf` → `amount must be a finite number.` · `abc` → `amount must be a valid number.` |
| `category` | `food`, `transport`, `salary`, `rent`, `entertainment`, `other` | `shopping` → `unknown category 'shopping'.` |
| `currency` | `EUR`, `USD`, `GBP` | `JPY` → `currency must be one of [...]` |

**Policies**
- **Case-sensitive:** `Expense` or `eur` are rejected, not silently corrected. The user sees a clear message and can type it again.
- **Extra spaces are trimmed:** `" food "` becomes `food`, because that is never ambiguous.
- **Unknown categories are rejected**, not mapped to `other`.

## Test

From the project folder:

```bash
python -m pytest
```

The 9 tests cover:
- **Normal case:** a valid transaction is created correctly.
- **Boundary cases:** amount `0` is rejected, `0.01` is accepted, `nan` and `inf` are rejected, and an impossible date is rejected.
- **Summary:** totals are kept separate per currency.
- **Persistence:** save → load gives back the same transactions, and duplicate IDs in a file are reported with their row number.

## Project structure

```
budget-manager/
├── README.md
├── DESIGN.md
├── AI_DISCLOSURE.md
├── pytest.ini
├── data/
│   └── sample_transactions.csv
├── src/
│   └── budget_manager/
│       ├── __init__.py
│       ├── models.py       # Transaction schema
│       ├── validation.py   # boundary checks, clear error messages
│       ├── services.py     # add, filter, summarize
│       ├── storage.py      # load/save CSV
│       └── cli.py          # menu and prompts only
└── tests/
    └── test_budget.py
```

## Known limitations

- **No currency conversion:** totals are shown separately for each currency.
- **Amounts use `float`:** tiny rounding errors are possible; `Decimal` would be safer for real money.
- **No edit, delete or undo:** undo is the stretch goal and is not part of Release 1.
- **`filter_by_category` is in the service but not in the menu yet.**
- **The whole file is saved after every add:** simple and safe (it writes to a temporary file, then swaps it in), but slower with very large files.

