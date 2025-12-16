from enum import Enum


class OrderStatus(str, Enum):
    NEW = "New"
    PREPARING = "Preparing"
    READY = "Ready"
    CANCELLED = "Cancelled"


class PaymentStatus(str, Enum):
    PENDING = "Pending"
    PAID = "Paid"
    FAILED = "Failed"
