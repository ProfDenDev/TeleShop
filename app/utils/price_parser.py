# app/utils/price_parser.py
# ver 1.0

"""
Парсер цен TELESHOP.

Поддерживает:

500

500-2000

10.5

10,5

0.55-0.83

0,55-0,83

Результат:
копейки / центы валюты
"""

from decimal import Decimal


def parse_price_value(
    value: str | None,
) -> tuple[int | None, int | None]:
    """
    Возвращает:

    (
        price_from_value,
        price_to_value,
    )

    Все значения:
    в минимальных единицах валюты.

    Примеры:

    500
    ->
    (50000, None)

    500-2000
    ->
    (50000, 200000)

    10.5
    ->
    (1050, None)

    0.55-0.83
    ->
    (55, 83)
    """

    if not value:
        return (
            None,
            None,
        )

    value = value.strip()

    # -------------------------
    # Диапазон
    # -------------------------

    if "-" in value:

        left, right = value.split(
            "-",
            1,
        )

        return (
            _to_minor_units(left),
            _to_minor_units(right),
        )

    # -------------------------
    # Обычная цена
    # -------------------------

    return (
        _to_minor_units(value),
        None,
    )


def _to_minor_units(
    value: str,
) -> int:
    """
    Конвертация в копейки/центы.

    Примеры:

    500
    -> 50000

    10.5
    -> 1050

    10,5
    -> 1050

    0.55
    -> 55
    """

    value = (
        value
        .strip()
        .replace(",", ".")
    )

    decimal_value = Decimal(value)

    return int(
        decimal_value * 100
    )