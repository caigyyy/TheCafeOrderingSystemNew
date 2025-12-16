from __future__ import annotations
from observers import OrderObserver
from typing import TYPE_CHECKING
from enums import OrderStatus

if TYPE_CHECKING:
    from order import Order
    from gui_tk import CafeApp


class GuiOrderObserver(OrderObserver):
    def __init__(self, app: "CafeApp") -> None:
        self.app = app

    def update(self, order: "Order") -> None:
        try:
            self.app._refresh_order_table()
            self.app._refresh_totals()
            self._update_status_label(order)
        except Exception:
            pass

    def _update_status_label(self, order: "Order") -> None:
        cust_name = self.app.customer.full_name if self.app.customer else ""
        if order.status == OrderStatus.NEW:
            text = f"Status: Order created ({cust_name})"
        elif order.status == OrderStatus.PREPARING:
            text = "Preparing Order: Estimated 4 mins"
        elif order.status == OrderStatus.READY:
            text = "Order: Ready"
        elif order.status == OrderStatus.CANCELLED:
            text = "Order: Cancelled"
        else:
            text = f"Status: {order.status.value}"
        self.app.customer_status_lbl.configure(text=text)
