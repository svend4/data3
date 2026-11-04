from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from .models import BudgetState, Transaction


def _transaction_to_dict(transaction: Transaction) -> dict[str, Any]:
    payload = asdict(transaction)
    payload["amount"] = str(transaction.amount)
    payload["created_at"] = transaction.created_at.isoformat()
    return payload


def _transaction_from_dict(payload: dict[str, Any]) -> Transaction:
    return Transaction(
        transaction_id=payload["transaction_id"],
        kind=payload["kind"],
        amount=Decimal(payload["amount"]),
        category=payload["category"],
        note=payload.get("note"),
        created_at=datetime.fromisoformat(payload["created_at"]),
    )


def load_state(path: Path) -> BudgetState:
    if not path.exists():
        return BudgetState(currency="EUR")
    raw = json.loads(path.read_text(encoding="utf-8"))
    return BudgetState(
        currency=raw.get("currency", "EUR"),
        incomes=[_transaction_from_dict(item) for item in raw.get("incomes", [])],
        expenses=[_transaction_from_dict(item) for item in raw.get("expenses", [])],
    )


def save_state(path: Path, state: BudgetState) -> None:
    payload = {
        "currency": state.currency,
        "incomes": [_transaction_to_dict(item) for item in state.incomes],
        "expenses": [_transaction_to_dict(item) for item in state.expenses],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
