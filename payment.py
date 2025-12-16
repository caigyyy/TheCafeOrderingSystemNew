from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from enums import PaymentStatus


@dataclass
class Payment:
    payment_id: str
    amount: float
    paid_at: Optional[datetime] = None
    status: PaymentStatus = PaymentStatus.PENDING
