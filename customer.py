from dataclasses import dataclass


@dataclass
class Customer:
    customer_id: str
    full_name: str
    phone: str
