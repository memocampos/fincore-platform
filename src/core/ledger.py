import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.audit import write_audit_entry
from src.core.exceptions import (
    AccountInactiveError,
    AccountNotFoundError,
    CurrencyMismatchError,
    InvalidAmountError,
    InsufficientFundsError,
)
from src.core.money import Money
from src.models.account import Account
from src.models.transaction import Transaction


async def transfer(
    session: AsyncSession,
    *,
    from_account_id: uuid.UUID,
    to_account_id: uuid.UUID,
    amount: Money,
    actor_id: uuid.UUID,
    description: str | None = None,
) -> tuple[Transaction, Transaction]:
    if not amount.is_positive():
        raise InvalidAmountError("Transfer amount must be positive")

    # SELECT FOR UPDATE on both rows in one round-trip prevents TOCTOU races
    # when concurrent transfers touch the same accounts.
    result = await session.execute(
        select(Account)
        .where(Account.id.in_([from_account_id, to_account_id]))
        .with_for_update()
    )
    accounts = {row.id: row for row in result.scalars()}

    src = accounts.get(from_account_id)
    dst = accounts.get(to_account_id)

    if src is None:
        raise AccountNotFoundError(f"Account {from_account_id} not found")
    if dst is None:
        raise AccountNotFoundError(f"Account {to_account_id} not found")
    if not src.is_active:
        raise AccountInactiveError(f"Account {from_account_id} is inactive")
    if not dst.is_active:
        raise AccountInactiveError(f"Account {to_account_id} is inactive")
    if src.currency != amount.currency:
        raise CurrencyMismatchError(
            f"Source account currency {src.currency} does not match transfer currency {amount.currency}"
        )
    if dst.currency != amount.currency:
        raise CurrencyMismatchError(
            f"Destination account currency {dst.currency} does not match transfer currency {amount.currency}"
        )
    if src.balance_cents < amount.amount_cents:
        raise InsufficientFundsError("Insufficient funds")

    reference_id = uuid.uuid4()

    src.balance_cents -= amount.amount_cents
    dst.balance_cents += amount.amount_cents

    debit = Transaction(
        account_id=from_account_id,
        amount_cents=-amount.amount_cents,
        currency=amount.currency,
        entry_type="debit",
        reference_id=reference_id,
        description=description,
    )
    credit = Transaction(
        account_id=to_account_id,
        amount_cents=amount.amount_cents,
        currency=amount.currency,
        entry_type="credit",
        reference_id=reference_id,
        description=description,
    )
    session.add(debit)
    session.add(credit)

    await write_audit_entry(
        session,
        actor_id=actor_id,
        action="transfer",
        resource_type="account",
        resource_id=from_account_id,
        payload={
            "to_account_id": str(to_account_id),
            "amount_cents": amount.amount_cents,
            "currency": amount.currency,
            "reference_id": str(reference_id),
        },
    )

    return debit, credit
