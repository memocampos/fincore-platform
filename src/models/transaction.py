import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    # Negative = debit, positive = credit. Stored separately from entry_type for
    # easy summation without conditional logic.
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    entry_type: Mapped[str] = mapped_column(String(10), nullable=False)  # "debit" | "credit"
    # Shared across the debit and credit legs of one transfer so they can be paired.
    reference_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True, index=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
