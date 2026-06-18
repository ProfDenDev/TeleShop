# app/constants/price_types.py
# ver 2.0

"""
Типы цен TELESHOP.

Используются:
- ProductPrice
- XLSX импорт
- Telegram Bot
- Mini App
"""

# Обычная цена
FIXED = "FIXED"

# От
FROM = "FROM"

# До
TO = "TO"

# Диапазон
RANGE = "RANGE"

# Бесплатно
FREE = "FREE"

# По запросу
ON_REQUEST = "ON_REQUEST"

# Договорная
NEGOTIABLE = "NEGOTIABLE"


ALL_PRICE_TYPES = (
    FIXED,
    FROM,
    TO,
    RANGE,
    FREE,
    ON_REQUEST,
    NEGOTIABLE,
)