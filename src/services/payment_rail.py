import uuid
from dataclasses import dataclass
from enum import StrEnum


class RailStatus(StrEnum):
    PENDING = "pending"
    SETTLED = "settled"
    FAILED = "failed"


@dataclass
class RailResult:
    external_id: str
    status: RailStatus


class PaymentRailClient:
    """Adapter for the external payment rail (ACH, SEPA, etc.).

    Swap the implementation here without touching core or API code.
    """

    async def submit(
        self,
        reference_id: uuid.UUID,
        amount_cents: int,
        currency: str,
        destination: str,
    ) -> RailResult:
        raise NotImplementedError

    async def get_status(self, external_id: str) -> RailStatus:
        raise NotImplementedError
