import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import CurrentUser, get_current_user
from src.core.exceptions import (
    AccountInactiveError,
    AccountNotFoundError,
    CurrencyMismatchError,
    InsufficientFundsError,
    InvalidAmountError,
)
from src.core.ledger import transfer
from src.core.money import Money
from src.models.base import get_session

router = APIRouter(prefix="/v1/transfers", tags=["Transfers"])


class TransferRequest(BaseModel):
    from_account_id: uuid.UUID
    to_account_id: uuid.UUID
    amount_cents: int = Field(..., gt=0, description="Amount in minor currency units (cents)")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 currency code")
    description: str | None = None


class TransferResponse(BaseModel):
    reference_id: uuid.UUID
    from_account_id: uuid.UUID
    to_account_id: uuid.UUID
    amount_cents: int
    currency: str


@router.post(
    "/",
    response_model=TransferResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def initiate_transfer(
    body: TransferRequest,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
) -> TransferResponse:
    try:
        debit, _ = await transfer(
            session,
            from_account_id=body.from_account_id,
            to_account_id=body.to_account_id,
            amount=Money(body.amount_cents, body.currency.upper()),
            actor_id=current_user.id,
            description=body.description,
        )
        await session.commit()
    except (AccountNotFoundError, CurrencyMismatchError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except (AccountInactiveError, InsufficientFundsError, InvalidAmountError) as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    return TransferResponse(
        reference_id=debit.reference_id,
        from_account_id=body.from_account_id,
        to_account_id=body.to_account_id,
        amount_cents=body.amount_cents,
        currency=body.currency.upper(),
    )
