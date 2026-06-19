# Database Schema

## Полная ERD диаграмма

```mermaid
erDiagram

Category ||--o{ Product : contains

Brand ||--o{ Product : brand

User ||--o{ Product : creates

Product ||--o{ ProductPhoto : photos

Product ||--o{ ProductPrice : prices

Product ||--o{ ProductPriceHistory : history

Product ||--|| ProductStats : stats

User ||--o{ Favorite : favorites

Product ||--o{ Favorite : favorite

User ||--o{ CartItem : cart

Product ||--o{ CartItem : cart_item

User ||--o{ Order : creates

Order ||--o{ OrderItem : items

Order ||--o{ OrderNote : notes

Product ||--o{ Review : reviews

User ||--o{ Review : writes

Product ||--o{ Report : reports

User ||--o{ Report : reports

Tag ||--o{ ProductTag : relation

Product ||--o{ ProductTag : relation

PromoCode ||--o{ Order : discount

NotifySubscription }o--|| Product : watches

NotifySubscription }o--|| User : owner

NotificationQueue }o--|| User : recipient
```

---

# Database Modules

```mermaid
flowchart TD

ProductsModule

OrdersModule

CatalogModule

UsersModule

NotificationsModule

ImportModule

ProductsModule --> Product

ProductsModule --> ProductPhoto

ProductsModule --> ProductPrice

ProductsModule --> ProductPriceHistory

ProductsModule --> ProductStats

CatalogModule --> Category

CatalogModule --> Brand

CatalogModule --> Tag

CatalogModule --> ProductTag

UsersModule --> User

UsersModule --> Favorite

UsersModule --> CartItem

UsersModule --> Review

UsersModule --> Report

OrdersModule --> Order

OrdersModule --> OrderItem

OrdersModule --> OrderNote

OrdersModule --> PromoCode

NotificationsModule --> NotificationQueue

NotificationsModule --> NotifySubscription

ImportModule --> Product

ImportModule --> Category

ImportModule --> Brand
```

---

# ENUMS

## ProductStatus

Используется для управления жизненным циклом товара.

| Значение | Назначение     |
| -------- | -------------- |
| ACTIVE   | Активный товар |
| RESERVED | Зарезервирован |
| SOLD     | Продан         |
| ARCHIVED | Архив          |
| DELETED  | Удалён         |

---

## Диаграмма состояний товара

```mermaid
stateDiagram-v2

[*] --> ACTIVE

ACTIVE --> RESERVED

RESERVED --> ACTIVE

ACTIVE --> SOLD

RESERVED --> SOLD

ACTIVE --> ARCHIVED

ARCHIVED --> ACTIVE

ACTIVE --> DELETED

ARCHIVED --> DELETED
```

---

## ProductCondition

| Значение  | Назначение            |
| --------- | --------------------- |
| NEW       | Новый товар           |
| LIKE_NEW  | Состояние нового      |
| USED      | Бывший в употреблении |
| FOR_PARTS | На запчасти           |
| SERVICE   | Услуга                |

---

## PriceType

| Значение   | Назначение         |
| ---------- | ------------------ |
| FIXED      | Фиксированная цена |
| NEGOTIABLE | Возможен торг      |
| FROM       | Цена от            |
| ON_REQUEST | Цена по запросу    |

---

## OrderStatus

| Значение  | Назначение     |
| --------- | -------------- |
| PENDING   | Ожидает оплаты |
| PAID      | Оплачен        |
| SHIPPED   | Отправлен      |
| COMPLETED | Завершён       |
| CANCELLED | Отменён        |

---

## NotificationStatus

| Значение   | Назначение       |
| ---------- | ---------------- |
| PENDING    | Ожидает отправки |
| PROCESSING | Обрабатывается   |
| SENT       | Отправлено       |
| FAILED     | Ошибка отправки  |
| CANCELLED  | Отменено         |

---

# Константы проекта

## Лимиты

| Константа          | Значение | Назначение                   |
| ------------------ | -------- | ---------------------------- |
| MAX_PRODUCT_IMAGES | 9        | Максимум фото товара         |
| MAX_FAVORITES      | 30       | Максимум избранного          |
| MAX_ADMIN_PRODUCTS | 1000     | Лимит товаров администратора |

---

## Ограничения строк

| Константа                  | Значение |
| -------------------------- | -------- |
| CATEGORY_NAME_MAX_LENGTH   | 80       |
| CATEGORY_SLUG_MAX_LENGTH   | 120      |
| SEO_TITLE_MAX_LENGTH       | 150      |
| SEO_DESCRIPTION_MAX_LENGTH | 300      |

---

# SKU Architecture

## Генерация SKU

```mermaid
flowchart LR

Product

Product --> SKUService

SKUService --> GeneratedSKU

GeneratedSKU --> Database
```

---

## Формат

```text
DA0001
DA0002
DA0003

...

DA9999

DB0001
DB0002
```

---

# Search Architecture

## Общая схема

```mermaid
flowchart LR

UserQuery

UserQuery --> Normalize

Normalize --> ReplaceYo

ReplaceYo --> ReplaceHardSign

ReplaceHardSign --> KeyboardFix

KeyboardFix --> SearchIndex

SearchIndex --> ProductRepository

ProductRepository --> Result
```

---

## Нормализация

### Ё → Е

```text
ЛЁГКИЙ
ЛЕГКИЙ
```

---

### Ъ → Ь

```text
ОБЪЕКТИВ
ОБЬЕКТИВ
```

---

### Исправление раскладки

```text
ktqrf
leqka
```

↓

```text
лейка
```

---

# Statistics Architecture

```mermaid
flowchart TD

ProductView

FavoriteAdd

OrderCreated

ProductView --> ProductStats

FavoriteAdd --> ProductStats

OrderCreated --> ProductStats
```

---

# SEO Architecture

## Генерация URL

```mermaid
flowchart LR

ProductTitle

ProductTitle --> SlugGenerator

SlugGenerator --> Slug

Slug --> URL
```

---

## Пример

```text
Leica M500-N
```

↓

```text
leica-m500-n
```

↓

```text
/produkty/leica-m500-n
```

---

# Currency System

```mermaid
flowchart LR

CurrencyRate

CurrencyRate --> ProductPrice

ProductPrice --> PriceUAH

PriceUAH --> Search

PriceUAH --> Catalog
```

---

## Поддерживаемые валюты

| Валюта     | Код |
| ---------- | --- |
| Гривна     | UAH |
| Доллар США | USD |
| Евро       | EUR |

---

# Notification System

```mermaid
flowchart TD

ProductChanged

PriceChanged

OrderChanged

ProductChanged --> NotificationQueue

PriceChanged --> NotificationQueue

OrderChanged --> NotificationQueue

NotificationQueue --> TelegramBot

TelegramBot --> User
```

---

# Audit Trail

## История цены

```mermaid
flowchart LR

OldPrice

OldPrice --> ProductPriceHistory

NewPrice --> ProductPriceHistory

ProductPriceHistory --> Analytics
```

---

# Полная схема ядра TELESHOP

```mermaid
flowchart TD

TelegramBot

MiniApp

FastAPI

Services

Repositories

Database

ImportSystem

NotificationSystem

TelegramBot --> Services

MiniApp --> FastAPI

FastAPI --> Services

Services --> Repositories

Repositories --> Database

ImportSystem --> Services

Services --> NotificationSystem

NotificationSystem --> TelegramBot
```
