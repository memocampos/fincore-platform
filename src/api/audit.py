import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import CurrentUser, get_current_user
from src.models.audit_log import AuditLog
from src.models.base import get_session

router = APIRouter(prefix="/v1/audit", tags=["Audit"])


class AuditLogResponse(BaseModel):
    id: uuid.UUID
    actor_id: uuid.UUID
    action: str
    resource_type: str
    resource_id: uuid.UUID
    payload: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


@router.get("/", response_model=list[AuditLogResponse], response_model_exclude_none=True)
async def list_audit_entries(
    resource_id: uuid.UUID | None = None,
    limit: int = Query(50, le=200),
    session: AsyncSession = Depends(get_session),
    current_user: CurrentUser = Depends(get_current_user),
) -> list[AuditLog]:
    query = (
        select(AuditLog)
        .where(AuditLog.actor_id == current_user.id)
        .order_by(AuditLog.created_at.desc())
        .limit(limit)
    )
    if resource_id:
        query = query.where(AuditLog.resource_id == resource_id)
    result = await session.execute(query)
    return list(result.scalars())
