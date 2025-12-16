from __future__ import annotations
from datetime import datetime
from uuid import uuid4

from enums import PaymentStatus
from payment import Payment


class PaymentService:
    def process_payment(self, amount: float) -> Payment:
        # Simple simulation: always succeeds (can be extended later).
        p = Payment(payment_id=str(uuid4()), amount=float(amount))
        p.status = PaymentStatus.PAID
        p.paid_at = datetime.utcnow()
        return p

    def refund(self, payment_id: str) -> Payment:
        # Placeholder for a real refund workflow.
        p = Payment(payment_id=payment_id, amount=0.0)
        p.status = PaymentStatus.PAID
        p.paid_at = datetime.utcnow()
        return p
