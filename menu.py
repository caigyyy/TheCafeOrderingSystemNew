from __future__ import annotations
from typing import Dict, List
from menu_items import MenuItem


class Menu:
    def __init__(self, menu_id: str, title: str):
        self.menu_id = menu_id
        self.title = title
        self._items: Dict[str, MenuItem] = {}

    def add_item(self, item: MenuItem) -> None:
        self._items[item.id] = item

    def remove_item(self, item_id: str) -> None:
        if item_id not in self._items:
            raise KeyError(f"Menu item not found: {item_id}")
        del self._items[item_id]

    def set_availability(self, item_id: str, available: bool) -> None:
        if item_id not in self._items:
            raise KeyError(f"Menu item not found: {item_id}")
        self._items[item_id].available = available

    def get_item(self, item_id: str) -> MenuItem:
        if item_id not in self._items:
            raise KeyError(f"Menu item not found: {item_id}")
        return self._items[item_id]

    def list_items(self, only_available: bool = False) -> List[MenuItem]:
        items = list(self._items.values())
        if only_available:
            items = [i for i in items if i.available]
        return items
