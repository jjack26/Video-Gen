"""Explicit reservation-based spending safeguards. Offline only."""
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

def dollars(value: str | int | Decimal) -> Decimal:
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("invalid amount") from exc
    if not amount.is_finite() or amount < 0:
        raise ValueError("amount must be finite and nonnegative")
    return amount

@dataclass
class Budget:
    per_run_limit: Decimal = Decimal("2")
    monthly_limit: Decimal = Decimal("30")
    monthly_spent: Decimal = Decimal("0")
    run_spent: dict[str, Decimal] = field(default_factory=dict)
    reservations: dict[str, tuple[str, Decimal]] = field(default_factory=dict)
    stopped: bool = False

    def __post_init__(self):
        self.per_run_limit = dollars(self.per_run_limit)
        self.monthly_limit = dollars(self.monthly_limit)
        self.monthly_spent = dollars(self.monthly_spent)

    def reserve(self, operation_id: str, run_id: str, estimate: str) -> None:
        if self.stopped:
            raise PermissionError("kill switch active")
        if not operation_id or not run_id or operation_id in self.reservations:
            raise ValueError("invalid or duplicate reservation")
        amount = dollars(estimate)
        pending_month = sum((v for _, v in self.reservations.values()), Decimal("0"))
        pending_run = sum((v for r, v in self.reservations.values() if r == run_id), Decimal("0"))
        if self.monthly_spent + pending_month + amount > self.monthly_limit:
            raise PermissionError("monthly budget exceeded")
        if self.run_spent.get(run_id, Decimal("0")) + pending_run + amount > self.per_run_limit:
            raise PermissionError("run budget exceeded")
        self.reservations[operation_id] = (run_id, amount)

    def settle(self, operation_id: str, actual: str) -> None:
        if operation_id not in self.reservations:
            raise ValueError("unknown reservation")
        run_id, estimate = self.reservations[operation_id]
        amount = dollars(actual)
        if amount > estimate:
            raise PermissionError("actual charge exceeds reservation; reconcile manually")
        self.monthly_spent += amount
        self.run_spent[run_id] = self.run_spent.get(run_id, Decimal("0")) + amount
        del self.reservations[operation_id]

    def cancel(self, operation_id: str) -> None:
        del self.reservations[operation_id]
