from __future__ import annotations
from dataclasses import dataclass
from menu_items import MenuItem


@dataclass
class OrderLine:
    item: MenuItem
    qty: int

    @property
    def unit_price(self) -> float:
        return float(self.item.price)

    def line_total(self) -> float:
        return self.unit_price * self.qty
