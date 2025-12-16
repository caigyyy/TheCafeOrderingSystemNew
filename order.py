from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from enums import OrderStatus
from menu_items import MenuItem
from order_line import OrderLine
from observers import OrderObserver


@dataclass
class Order:
    order_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: OrderStatus = OrderStatus.NEW
    _lines: List[OrderLine] = field(default_factory=list)
    _observers: List[OrderObserver] = field(default_factory=list)

    def add_item(self, item: MenuItem, qty: int) -> None:
        if not item.available:
            raise ValueError(f"Item '{item.name}' is not available.")
        if qty <= 0:
            raise ValueError("qty must be > 0")

        existing = self._find_line(item.id)
        if existing:
            existing.qty += qty
        else:
            self._lines.append(OrderLine(item=item, qty=qty))
        self.notify_observers()

    def remove_item(self, item_id: str) -> None:
        before = len(self._lines)
        self._lines = [l for l in self._lines if l.item.id != item_id]
        if len(self._lines) == before:
            raise KeyError(f"Item not found in order: {item_id}")
        self.notify_observers()

    def set_status(self, status: OrderStatus) -> None:
        self.status = status
        self.notify_observers()

    def calculate_total(self) -> float:
        return sum(l.line_total() for l in self._lines)

    def add_observer(self, obs: OrderObserver) -> None:
        if obs not in self._observers:
            self._observers.append(obs)

    def remove_observer(self, obs: OrderObserver) -> None:
        if obs in self._observers:
            self._observers.remove(obs)

    def notify_observers(self) -> None:
        for obs in list(self._observers):
            obs.update(self)

    def get_lines(self) -> List[OrderLine]:
        return list(self._lines)

    def _find_line(self, item_id: str) -> Optional[OrderLine]:
        for line in self._lines:
            if line.item.id == item_id:
                return line
        return None
