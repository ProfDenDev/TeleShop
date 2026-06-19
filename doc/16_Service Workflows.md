# Service Workflows

## Назначение

Данный раздел описывает основные бизнес-процессы TELESHOP.

Каждая диаграмма показывает полный путь выполнения операции через слои системы:

```mermaid
flowchart LR

TelegramBot

MiniApp

FastAPI

Services

Repositories

Database

TelegramBot --> Services
MiniApp --> FastAPI
FastAPI --> Services
Services --> Repositories
Repositories --> Database
```

---

# Product Creation Workflow

## Создание товара

```mermaid
sequenceDiagram

actor Admin

participant Bot as Telegram Bot
participant PS as ProductService
participant SKU as SKUService
participant CR as CategoryRepository
participant BR as BrandRepository
participant PR as ProductRepository
participant PPR as ProductPriceRepository
participant DB as Database

Admin->>Bot: Создать товар

Bot->>PS: create_product(dto)

PS->>SKU: generate_sku()

SKU-->>PS: DA0001

PS->>CR: validate_category()

CR-->>PS: OK

PS->>BR: validate_brand()

BR-->>PS: OK

PS->>PR: create_product()

PR->>DB: INSERT product

DB-->>PR: Product

PR-->>PS: Product

PS->>PPR: create_price()

PPR->>DB: INSERT product_price

DB-->>PPR: Price

PPR-->>PS: Price

PS-->>Bot: Success

Bot-->>Admin: Товар создан
```

---

# Product Status Workflow

## Жизненный цикл товара

```mermaid
stateDiagram-v2

[*] --> ACTIVE

ACTIVE --> RESERVED : reserve()

RESERVED --> ACTIVE : unreserve()

ACTIVE --> SOLD : sell()

RESERVED --> SOLD : sell()

ACTIVE --> ARCHIVED : archive()

ARCHIVED --> ACTIVE : restore()

ACTIVE --> DELETED : delete()

ARCHIVED --> DELETED : delete()
```

---

# Add To Favorites Workflow

## Добавление в избранное

```mermaid
sequenceDiagram

actor User

participant Bot
participant FS as FavoriteService
participant FR as FavoriteRepository
participant DB

User->>Bot: Добавить в избранное

Bot->>FS: add_to_favorites()

FS->>FR: exists()

FR->>DB: SELECT

DB-->>FR: False

FR-->>FS: False

FS->>FR: create()

FR->>DB: INSERT

DB-->>FR: Favorite

FR-->>FS: Favorite

FS-->>Bot: Success

Bot-->>User: Добавлено
```

---

# Add To Cart Workflow

## Добавление товара в корзину

```mermaid
sequenceDiagram

actor User

participant Bot
participant CS as CartService
participant PR as ProductRepository
participant CR as CartRepository
participant DB

User->>Bot: Добавить в корзину

Bot->>CS: add_item()

CS->>PR: get_product()

PR->>DB: SELECT

DB-->>PR: Product

PR-->>CS: Product

CS->>CR: add_item()

CR->>DB: INSERT/UPDATE

DB-->>CR: CartItem

CR-->>CS: CartItem

CS-->>Bot: Success

Bot-->>User: Добавлено в корзину
```

---

# Cart Merge Workflow

## Повторное добавление товара

```mermaid
flowchart TD

Start

Start --> Exists

Exists{Товар уже в корзине?}

Exists -->|Нет| CreateItem

Exists -->|Да| IncreaseQuantity

CreateItem --> Save

IncreaseQuantity --> Save

Save --> Finish
```

---

# Checkout Workflow

## Оформление заказа

```mermaid
sequenceDiagram

actor User

participant Cart
participant Promo
participant Order
participant DB

User->>Cart: checkout()

Cart->>Cart: validate_cart()

Cart->>Promo: validate_promocode()

Promo-->>Cart: Discount

Cart->>Order: create_order()

Order->>DB: INSERT order

DB-->>Order: Order

Order-->>User: Success
```

---

# Order Creation Workflow

```mermaid
sequenceDiagram

participant OrderService
participant OrderRepository
participant CartRepository
participant NotificationService
participant DB

OrderService->>OrderRepository: create_order()

OrderRepository->>DB: INSERT order

DB-->>OrderRepository: Order

OrderRepository-->>OrderService: Order

OrderService->>OrderRepository: create_items()

OrderRepository->>DB: INSERT order_items

OrderService->>CartRepository: clear_cart()

OrderService->>NotificationService: enqueue()

NotificationService-->>OrderService: OK
```

---

# Order Lifecycle Workflow

```mermaid
stateDiagram-v2

[*] --> PENDING

PENDING --> PAID

PAID --> SHIPPED

SHIPPED --> COMPLETED

PENDING --> CANCELLED

PAID --> CANCELLED
```

---

# Price Change Workflow

## Изменение цены товара

```mermaid
sequenceDiagram

actor Admin

participant ProductService
participant ProductPriceRepository
participant PriceHistoryRepository
participant NotificationService
participant DB

Admin->>ProductService: change_price()

ProductService->>ProductPriceRepository: update()

ProductPriceRepository->>DB: UPDATE

DB-->>ProductPriceRepository: OK

ProductPriceRepository-->>ProductService: Price

ProductService->>PriceHistoryRepository: add_record()

PriceHistoryRepository->>DB: INSERT history

ProductService->>NotificationService: notify()

NotificationService-->>ProductService: queued

ProductService-->>Admin: Success
```

---

# Search Workflow

```mermaid
flowchart TD

Query

Query --> Normalize

Normalize --> ReplaceYo

ReplaceYo --> ReplaceHardSign

ReplaceHardSign --> FixKeyboardLayout

FixKeyboardLayout --> BuildQuery

BuildQuery --> ProductRepository

ProductRepository --> Results

Results --> User
```

---

# Product View Workflow

```mermaid
sequenceDiagram

actor User

participant Bot
participant ProductService
participant ProductStatsRepository
participant ProductRepository

User->>Bot: Открыть товар

Bot->>ProductService: get_product()

ProductService->>ProductStatsRepository: increment_views()

ProductStatsRepository-->>ProductService: OK

ProductService->>ProductRepository: get_product()

ProductRepository-->>ProductService: Product

ProductService-->>Bot: Product

Bot-->>User: Product Card
```

---

# XLSX Import Workflow

```mermaid
flowchart TD

UploadXLSX

UploadXLSX --> ParseFile

ParseFile --> ValidateColumns

ValidateColumns --> ValidateRows

ValidateRows --> Preview

Preview --> UserDecision

UserDecision -->|Import| ExecuteImport

UserDecision -->|Cancel| Finish
```

---

# Import Commit Workflow

```mermaid
sequenceDiagram

actor Admin

participant ImportService
participant CategoryRepository
participant BrandRepository
participant ProductRepository
participant ProductPriceRepository
participant DB

Admin->>ImportService: Import

ImportService->>DB: BEGIN

ImportService->>CategoryRepository: create/update

ImportService->>BrandRepository: create/update

ImportService->>ProductRepository: create

ImportService->>ProductPriceRepository: create

ImportService->>DB: COMMIT

ImportService-->>Admin: Success
```

---

# ZIP Photo Import Workflow

```mermaid
flowchart TD

ZIP

ZIP --> Extract

Extract --> FindSKU

FindSKU --> ProductFound

ProductFound --> UploadTelegram

UploadTelegram --> SaveFileId

SaveFileId --> ProductPhoto

ProductPhoto --> Finish
```

---

# Notification Workflow

```mermaid
sequenceDiagram

participant Event
participant NotificationService
participant NotificationQueue
participant TelegramBot
participant User

Event->>NotificationService: notify()

NotificationService->>NotificationQueue: enqueue()

NotificationQueue-->>NotificationService: queued

NotificationQueue->>TelegramBot: send()

TelegramBot->>User: Message

User-->>TelegramBot: received
```

---

# Notification Queue Workflow

```mermaid
stateDiagram-v2

[*] --> PENDING

PENDING --> PROCESSING

PROCESSING --> SENT

PROCESSING --> FAILED

FAILED --> PROCESSING : retry()

FAILED --> CANCELLED

SENT --> [*]

CANCELLED --> [*]
```

---

# Broadcast Workflow

```mermaid
flowchart TD

Admin

Admin --> CreateMessage

CreateMessage --> Preview

Preview --> Confirm

Confirm --> NotificationQueue

NotificationQueue --> TelegramBot

TelegramBot --> Users
```

---

# Full TELESHOP Business Process Map

```mermaid
flowchart TD

Product

Product --> Favorites

Product --> Search

Product --> Cart

Search --> ProductCard

Favorites --> ProductCard

ProductCard --> Cart

Cart --> Checkout

Checkout --> Order

Order --> Notification

Product --> Price

Price --> Notification

Import --> Product

Admin --> Import

Admin --> Product

Admin --> Price

Admin --> Orders

Orders --> Notification
```