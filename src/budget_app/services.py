from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from .models import BudgetState, Transaction


def add_income(state: BudgetState, amount: Decimal, source: str) -> BudgetState:
    transaction = Transaction(
        transaction_id=str(uuid4()),
        kind="income",
        amount=amount,
        category=source,
        note=None,
        created_at=datetime.utcnow(),
    )
    return replace(state, incomes=[*state.incomes, transaction])


def add_expense(state: BudgetState, amount: Decimal, category: str, note: str | None) -> BudgetState:
    transaction = Transaction(
        transaction_id=str(uuid4()),
        kind="expense",
        amount=amount,
        category=category,
        note=note,
        created_at=datetime.utcnow(),
    )
    return replace(state, expenses=[*state.expenses, transaction])


def summarize(state: BudgetState) -> dict[str, Decimal]:
    total_income = sum((item.amount for item in state.incomes), Decimal("0"))
    total_expense = sum((item.amount for item in state.expenses), Decimal("0"))
    return {
        "income": total_income,
        "expense": total_expense,
        "balance": total_income - total_expense,
    }
