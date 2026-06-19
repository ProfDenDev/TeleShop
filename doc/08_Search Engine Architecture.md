# Search Engine Architecture

## Общая схема поиска

```mermaid
flowchart LR

UserQuery

UserQuery --> Normalize

Normalize --> QueryBuilder

QueryBuilder --> ProductRepository

ProductRepository --> SearchResults

SearchResults --> User
```

---

# SearchService

## Назначение

Центральный сервис поиска TELESHOP.

Обеспечивает:

* поиск товаров
* поиск категорий
* поиск брендов
* исправление раскладки
* нормализацию текста
* фильтрацию результатов

---

## Методы

| Метод                 | Назначение                     |
| --------------------- | ------------------------------ |
| search_products()     | Поиск товаров                  |
| search_categories()   | Поиск категорий                |
| search_brands()       | Поиск брендов                  |
| normalize_query()     | Нормализация текста            |
| replace_yo()          | Замена Ё→Е                     |
| replace_hard_sign()   | Замена Ъ→Ь                     |
| fix_keyboard_layout() | Исправление раскладки          |
| build_search_vector() | Формирование поискового текста |

---

# Поисковые поля

## Product

```mermaid
flowchart TD

Product

Product --> Title

Product --> SKU

Product --> Brand

Product --> Description

Product --> Tags

Product --> Manufacturer
```

---

## Индексируемые поля

| Поле              | Используется |
| ----------------- | ------------ |
| title             | Да           |
| sku               | Да           |
| manufacturer_name | Да           |
| manufacturer_sku  | Да           |
| barcode           | Да           |
| short_description | Да           |
| full_description  | Да           |
| search_text       | Да           |
| tags              | Да           |
| brand_name        | Да           |

---

# Нормализация

## Этапы

```mermaid
flowchart TD

Query

Query --> LowerCase

LowerCase --> ReplaceYo

ReplaceYo --> ReplaceHardSign

ReplaceHardSign --> FixLayout

FixLayout --> Search
```

---

## Примеры

### Ё → Е

```text
ЛЁГКИЙ

↓

ЛЕГКИЙ
```

---

### Ъ → Ь

```text
ОБЪЕКТИВ

↓

ОБЬЕКТИВ
```

---

### Исправление раскладки

```text
ktqrf

↓

лейка
```

---

# Каталог

## Архитектура

```mermaid
flowchart TD

RootCategory

RootCategory --> Category

Category --> SubCategory

SubCategory --> Products
```

---

# Category Tree

## Пример

```text
Электроника
 ├─ Телефоны
 │   ├─ Apple
 │   ├─ Samsung
 │   └─ Xiaomi
 │
 ├─ Компьютеры
 │   ├─ Ноутбуки
 │   ├─ ПК
 │   └─ Мониторы
 │
 └─ Фото и Видео
```

---

# Фильтры каталога

## Диаграмма

```mermaid
flowchart LR

Products

Products --> CategoryFilter

Products --> BrandFilter

Products --> PriceFilter

Products --> ConditionFilter

Products --> AvailabilityFilter
```

---

## Фильтры

| Фильтр       | Назначение    |
| ------------ | ------------- |
| Category     | Категория     |
| Brand        | Бренд         |
| Price        | Цена          |
| Condition    | Состояние     |
| Availability | Наличие       |
| Featured     | Рекомендуемые |
| Discount     | Со скидкой    |
| Tag          | По тегу       |

---

# Price Filter

## Диапазон

```mermaid
flowchart LR

MinPrice --> Search

MaxPrice --> Search
```

---

## Пример

```text
От 1000 грн

До 5000 грн
```

---

# Brand Filter

## Схема

```mermaid
flowchart LR

Brand

Brand --> ProductRepository

ProductRepository --> Products
```

---

# Tag Filter

## Схема

```mermaid
flowchart LR

Tag

Tag --> ProductTag

ProductTag --> Product
```

---

# Favorites Architecture

## Общая схема

```mermaid
flowchart TD

User

User --> Favorite

Favorite --> Product

Favorite --> ProductStats
```

---

# FavoriteService

## Методы

| Метод                     | Назначение      |
| ------------------------- | --------------- |
| add_to_favorites()        | Добавить        |
| remove_from_favorites()   | Удалить         |
| exists()                  | Проверка        |
| get_user_favorites()      | Получить список |
| count_product_favorites() | Подсчёт         |

---

## Ограничение

```python
MAX_FAVORITES = 30
```

---

# Recommendation System

## Архитектура

```mermaid
flowchart TD

ProductViews

Favorites

Orders

ProductViews --> ProductStats

Favorites --> ProductStats

Orders --> ProductStats

ProductStats --> RecommendationEngine

RecommendationEngine --> FeaturedProducts
```

---

# Источники рекомендаций

| Источник  | Вес           |
| --------- | ------------- |
| Просмотры | Высокий       |
| Продажи   | Очень высокий |
| Избранное | Высокий       |
| Новинка   | Средний       |
| Featured  | Максимальный  |

---

# ProductStats

## Формирование статистики

```mermaid
flowchart TD

ViewProduct

AddFavorite

CreateOrder

ViewProduct --> ProductStats

AddFavorite --> ProductStats

CreateOrder --> ProductStats
```

---

## Показатели

| Поле            | Назначение         |
| --------------- | ------------------ |
| views_count     | Просмотры          |
| favorites_count | Избранное          |
| orders_count    | Продажи            |
| last_view_at    | Последний просмотр |

---

# Featured Products

## Логика

```mermaid
flowchart TD

Product

Product --> is_featured

is_featured --> FeaturedCatalog
```

---

## Используемые поля

| Поле           | Назначение                 |
| -------------- | -------------------------- |
| is_featured    | Показывать в рекомендациях |
| featured_until | Дата окончания продвижения |
| sort_priority  | Приоритет отображения      |

---

# Search Performance

## Схема

```mermaid
flowchart LR

SearchQuery

SearchQuery --> search_text_normalized

search_text_normalized --> SearchIndex

SearchIndex --> ProductRepository
```

---

# Search Ranking

## Приоритет выдачи

```mermaid
flowchart TD

SKU

Title

Brand

Tags

Description

SKU --> Result

Title --> Result

Brand --> Result

Tags --> Result

Description --> Result
```

---

## Порядок релевантности

| Приоритет | Поле         |
| --------- | ------------ |
| 1         | SKU          |
| 2         | Title        |
| 3         | Brand        |
| 4         | Tags         |
| 5         | Manufacturer |
| 6         | Description  |

---

# Полная схема Search System

```mermaid
flowchart TD

User

User --> SearchService

SearchService --> Normalize

Normalize --> ProductRepository

ProductRepository --> Product

Product --> ProductStats

ProductStats --> RecommendationEngine

RecommendationEngine --> Result

Result --> User
```
