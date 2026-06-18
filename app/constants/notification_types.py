from enum import StrEnum


class NotificationType(StrEnum):

    BACK_IN_STOCK = "BACK_IN_STOCK"

    PRICE_DROP = "PRICE_DROP"

    SIMILAR = "SIMILAR"

    ORDER_STATUS_CHANGED = "ORDER_STATUS_CHANGED"


