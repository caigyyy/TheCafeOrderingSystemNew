from __future__ import annotations
from observers import OrderObserver
from order import Order


class KitchenDisplay(OrderObserver):
    def update(self, order: Order) -> None:
        # Simple console “display”
        print(f"[KitchenDisplay] Order {order.order_id} status={order.status.value} items={len(order.get_lines())}")

    def show(self, order_id: str, status) -> None:
        print(f"[KitchenDisplay] Order {order_id} -> {status}")


class BillingService(OrderObserver):
    def update(self, order: Order) -> None:
        # Could trigger bill recalculation or UI update in a real system
        print(f"[BillingService] Order {order.order_id} changed; subtotal={order.calculate_total():.2f}")
