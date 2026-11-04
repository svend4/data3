from __future__ import annotations

import argparse
from decimal import Decimal
from pathlib import Path

from .services import add_expense, add_income, summarize
from .storage import load_state, save_state


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Budget Assist DE CLI prototype")
    parser.add_argument("--storage", default="data/budget.json", help="Path to storage JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize storage")
    init_parser.add_argument("--currency", default="EUR")

    income_parser = subparsers.add_parser("add-income", help="Add income")
    income_parser.add_argument("--amount", required=True)
    income_parser.add_argument("--source", required=True)

    expense_parser = subparsers.add_parser("add-expense", help="Add expense")
    expense_parser.add_argument("--amount", required=True)
    expense_parser.add_argument("--category", required=True)
    expense_parser.add_argument("--note")

    subparsers.add_parser("summary", help="Show summary")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    storage_path = Path(args.storage)
    state = load_state(storage_path)

    if args.command == "init":
        state.currency = args.currency
        save_state(storage_path, state)
        print(f"Storage initialized at {storage_path} ({state.currency}).")
        return

    if args.command == "add-income":
        updated = add_income(state, Decimal(args.amount), args.source)
        save_state(storage_path, updated)
        print("Income added.")
        return

    if args.command == "add-expense":
        updated = add_expense(state, Decimal(args.amount), args.category, args.note)
        save_state(storage_path, updated)
        print("Expense added.")
        return

    if args.command == "summary":
        totals = summarize(state)
        print(
            f"Income: {totals['income']} {state.currency}\n"
            f"Expense: {totals['expense']} {state.currency}\n"
            f"Balance: {totals['balance']} {state.currency}"
        )


if __name__ == "__main__":
    main()
