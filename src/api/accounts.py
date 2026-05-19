import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import CurrentUser, get_current_user
from src.core.audit import write_audit_entry
from src.models.account import Account
from src.models.base import get_session

router = APIRouter(prefix="/v1/accounts", tags=["Accounts"])


class AccountCreate(BaseModel):
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 currency code")


class AccountResponse(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    currency: str
    balance_cents: int = Field(..., description="Balance in minor currency units (cents)")
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


@router.post(
    "/",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def create_account(
    body: AccountCreate,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
) -> Account:
    account = Account(owner_id=current_user.id, currency=body.currency.upper())
    session.add(account)
    await write_audit_entry(
        session,
        actor_id=current_user.id,
        action="create_account",
        resource_type="account",
        resource_id=account.id,
    )
    await session.commit()
    await session.refresh(account)
    return account


@router.get("/{account_id}", response_model=AccountResponse, response_model_exclude_none=True)
async def get_account(
    account_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
) -> Account:
    account = await session.get(Account, account_id)
    if account is None or account.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@router.get("/", response_model=list[AccountResponse], response_model_exclude_none=True)
async def list_accounts(
    limit: int = Query(50, le=200),
    cursor: str | None = None,
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[Account]:
    query = (
        select(Account)
        .where(Account.owner_id == current_user.id)
        .order_by(Account.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(query)
    return list(result.scalars())
