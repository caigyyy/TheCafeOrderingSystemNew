from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from order import Order


@dataclass
class Bill:
    bill_id: str
    issue_at: datetime
    sub_total: float
    tax: float
    total: float

    @staticmethod
    def generate_from(order: Order, bill_id: str, tax_rate: float) -> "Bill":
        sub = float(order.calculate_total())
        tax = round(sub * float(tax_rate), 2)
        total = round(sub + tax, 2)
        return Bill(
            bill_id=bill_id,
            issue_at=datetime.utcnow(),
            sub_total=round(sub, 2),
            tax=tax,
            total=total,
        )

    def to_text(self, order: Order, cafe_name: str = "Local Café") -> str:
        lines = []
        lines.append(f"{cafe_name}")
        lines.append(f"Bill ID: {self.bill_id}")
        lines.append(f"Issued: {self.issue_at.isoformat(timespec='seconds')}Z")
        lines.append(f"Order ID: {order.order_id}")
        lines.append("-" * 34)
        for ol in order.get_lines():
            name = ol.item.name
            qty = ol.qty
            unit = ol.unit_price
            total = ol.line_total()
            lines.append(f"{qty} x {name} @ {unit:.2f} = {total:.2f}")
        lines.append("-" * 34)
        lines.append(f"Subtotal: {self.sub_total:.2f}")
        lines.append(f"Tax:      {self.tax:.2f}")
        lines.append(f"TOTAL:    {self.total:.2f}")
        return "\n".join(lines)
