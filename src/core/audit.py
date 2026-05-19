import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.audit_log import AuditLog


async def write_audit_entry(
    session: AsyncSession,
    *,
    actor_id: uuid.UUID,
    action: str,
    resource_type: str,
    resource_id: uuid.UUID,
    payload: dict | None = None,
) -> AuditLog:
    entry = AuditLog(
        actor_id=actor_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        payload=payload,
    )
    session.add(entry)
    return entry
