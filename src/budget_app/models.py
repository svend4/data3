from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List


@dataclass
class Transaction:
    transaction_id: str
    kind: str
    amount: Decimal
    category: str
    note: str | None
    created_at: datetime


@dataclass
class BudgetState:
    currency: str
    incomes: List[Transaction] = field(default_factory=list)
    expenses: List[Transaction] = field(default_factory=list)
