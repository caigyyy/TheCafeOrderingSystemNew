from __future__ import annotations
from dataclasses import dataclass


@dataclass
class MenuItem:
    id: str
    name: str
    description: str
    price: float
    available: bool = True


@dataclass
class FoodItem(MenuItem):
    dietary_info: str = ""


@dataclass
class DrinkItem(MenuItem):
    size: str = "M"
    is_hot: bool = True
