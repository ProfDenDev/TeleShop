"""
Работа с денежными значениями.

Все суммы внутри системы
хранятся в копейках.

Примеры:

100     = 1.00 грн
19999   = 199.99 грн
150000  = 1500.00 грн
"""


def to_kop(value: float | str) -> int:
    """
    Перевести гривны в копейки.

    199.99 -> 19999
    """

    return int(round(float(value) * 100))


def from_kop(value: int) -> float:
    """
    Перевести копейки в гривны.

    19999 -> 199.99
    """

    return value / 100


def format_money(value: int) -> str:
    """
    Форматировать сумму.

    19999 -> 199.99
    """

    return f"{value / 100:.2f}"


def add_money(
    value1: int,
    value2: int
) -> int:
    """
    Сложение денежных сумм.
    """

    return value1 + value2


def subtract_money(
    value1: int,
    value2: int
) -> int:
    """
    Вычитание денежных сумм.

    Минимум 1 копейка.
    """

    return max(
        value1 - value2,
        1
    )


def apply_percent_discount(
    amount: int,
    percent: int
) -> int:
    """
    Применить процентную скидку.

    10000 коп
    10 %

    = 9000 коп
    """

    result = (
        amount
        * (100 - percent)
        // 100
    )

    return max(
        result,
        1
    )
def convert_to_uah(
    amount: int,
    rate_to_uah: int
) -> int:
    """
    amount - копейки валюты
    rate_to_uah - тысячные доли гривны

    Возвращает копейки UAH
    """

    return (
        amount * rate_to_uah
    ) // 1000
def apply_fixed_discount(
    amount: int,
    discount: int
) -> int:
    """
    Фиксированная скидка в копейках.
    """

    return max(
        amount - discount,
        1
    )
