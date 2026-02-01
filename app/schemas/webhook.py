from pydantic import BaseModel
from typing import Literal, Optional, Any
from datetime import datetime


class WebhookEvent(BaseModel):
    event: Literal[
        "PAYMENT_CREATED",
        "PAYMENT_CONFIRMED", 
        "PAYMENT_RECEIVED",
        "PAYMENT_OVERDUE",
        "PAYMENT_DELETED",
        "PAYMENT_RESTORED",
        "PAYMENT_REFUNDED",
        "PAYMENT_RECEIVED_IN_CASH_UNDONE",
        "PAYMENT_CHARGEBACK_REQUESTED",
        "PAYMENT_CHARGEBACK_DISPUTE",
        "PAYMENT_AWAITING_CHARGEBACK_REVERSAL",
        "PAYMENT_DUNNING_RECEIVED",
        "PAYMENT_DUNNING_REQUESTED",
        "PAYMENT_BANK_SLIP_VIEWED",
        "PAYMENT_CHECKOUT_VIEWED"
    ]
    payment: dict[str, Any]


class WebhookResponse(BaseModel):
    received: bool
    payment_id: Optional[str] = None
    event: str
    processed_at: datetime
