from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
from uuid import uuid4

from customer import Customer
from order import Order
from enums import OrderStatus


@dataclass
class OrderSystem:
    orders: Dict[str, Order] = field(default_factory=dict)

    def create_order(self, customer: Customer) -> Order:
        order_id = str(uuid4())
        o = Order(order_id=order_id, status=OrderStatus.NEW)
        self.orders[o.order_id] = o
        return o

    def get_order(self, order_id: str) -> Order:
        if order_id not in self.orders:
            raise KeyError(f"Order not found: {order_id}")
        return self.orders[order_id]
