from __future__ import annotations
from abc import ABC, abstractmethod

class OrderObserver(ABC):
    @abstractmethod
    def update(self, order: "Order") -> None:
        raise NotImplementedError