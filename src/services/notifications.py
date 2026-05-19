import uuid
from dataclasses import dataclass
from enum import StrEnum


class NotificationChannel(StrEnum):
    EMAIL = "email"
    WEBHOOK = "webhook"


@dataclass
class NotificationPayload:
    user_id: uuid.UUID
    channel: NotificationChannel
    subject: str
    body: str


class NotificationService:
    """Delivers transaction and account event notifications to users.

    Backed by an email provider or a user-registered webhook URL.
    """

    async def send(self, payload: NotificationPayload) -> None:
        raise NotImplementedError

    async def send_transfer_confirmation(
        self,
        *,
        actor_id: uuid.UUID,
        reference_id: uuid.UUID,
        amount_cents: int,
        currency: str,
    ) -> None:
        await self.send(
            NotificationPayload(
                user_id=actor_id,
                channel=NotificationChannel.EMAIL,
                subject="Transfer confirmed",
                body=(
                    f"Your transfer of {amount_cents} {currency} "
                    f"(ref: {reference_id}) has been processed."
                ),
            )
        )
