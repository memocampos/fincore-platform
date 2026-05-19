from dataclasses import dataclass

from src.core.exceptions import CurrencyMismatchError, InvalidAmountError


@dataclass(frozen=True)
class Money:
    amount_cents: int
    currency: str  # ISO 4217, e.g. "USD"

    def __post_init__(self):
        if not isinstance(self.amount_cents, int):
            raise InvalidAmountError("amount_cents must be an integer, never a float")
        if len(self.currency) != 3:
            raise ValueError(f"currency must be a 3-letter ISO 4217 code, got {self.currency!r}")

    def __add__(self, other: "Money") -> "Money":
        self._assert_same_currency(other)
        return Money(self.amount_cents + other.amount_cents, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._assert_same_currency(other)
        return Money(self.amount_cents - other.amount_cents, self.currency)

    def is_positive(self) -> bool:
        return self.amount_cents > 0

    def is_zero(self) -> bool:
        return self.amount_cents == 0

    def _assert_same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"Cannot operate on {self.currency} and {other.currency}"
            )
