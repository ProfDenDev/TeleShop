from enum import StrEnum


class OrderStatus(StrEnum):

    PENDING = "PENDING"

    CONFIRMED = "CONFIRMED"

    RESERVED = "RESERVED"

    PAID = "PAID"

    SHIPPED = "SHIPPED"

    COMPLETED = "COMPLETED"

    CANCELLED = "CANCELLED"