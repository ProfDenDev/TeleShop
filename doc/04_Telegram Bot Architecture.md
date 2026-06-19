# Telegram Bot Architecture

## Общая схема

```mermaid
flowchart TD

User[Telegram User]

User --> MainMenu

MainMenu --> Categories

MainMenu --> Search

MainMenu --> Favorites

MainMenu --> Cart

MainMenu --> Orders

MainMenu --> Contacts

Categories --> ProductCard

Search --> ProductCard

Favorites --> ProductCard

ProductCard --> Cart

Cart --> Checkout

Checkout --> OrderCreated
```

---

# Структура Bot Layer

```text
app/bot/

├── handlers/
├── keyboards/
├── middlewares/
├── filters/
├── states/
├── callbacks/
├── utils/
└── routers.py
```

---

# Handler Architecture

```mermaid
flowchart LR

TelegramUpdate

TelegramUpdate --> Router

Router --> Handler

Handler --> Service

Service --> Repository

Repository --> Database
```

---

# Главный экран

```mermaid
flowchart TD

Start

Start --> MainMenu

MainMenu --> Categories

MainMenu --> Search

MainMenu --> Favorites

MainMenu --> Cart

MainMenu --> Orders

MainMenu --> Contacts
```

---

## Главное меню

| Кнопка       | Действие          |
| ------------ | ----------------- |
| 🏪 Категории | Каталог товаров   |
| 🔍 Поиск     | Поиск товаров     |
| ⭐ Избранное  | Избранное         |
| 🛒 Корзина   | Корзина           |
| 📦 Заказы    | История заказов   |
| ☎️ Контакты  | Контакты магазина |

---

# Каталог

## Навигация

```mermaid
flowchart TD

Categories

Categories --> RootCategory

RootCategory --> SubCategory

SubCategory --> ProductList

ProductList --> ProductCard
```

---

# Карточка товара

## Сценарий

```mermaid
sequenceDiagram

User->>Bot: Открыть товар

Bot->>ProductService: get_product()

ProductService->>ProductRepository: get_by_id()

ProductRepository-->>ProductService: Product

ProductService-->>Bot: Product

Bot-->>User: Карточка товара
```

---

## Кнопки товара

| Кнопка        | Действие             |
| ------------- | -------------------- |
| 🛒 В корзину  | Добавить товар       |
| ⭐ В избранное | Добавить в избранное |
| 📷 Фото       | Галерея              |
| 🎥 Видео      | Видеообзор           |
| 🔗 Поделиться | Ссылка               |
| 📞 Связаться  | Контакты продавца    |

---

# Поиск

## Архитектура

```mermaid
flowchart LR

Query

Query --> Normalize

Normalize --> SearchService

SearchService --> ProductRepository

ProductRepository --> Result
```

---

## Поддержка поиска

| Возможность        | Поддержка |
| ------------------ | --------- |
| По названию        | Да        |
| По SKU             | Да        |
| По бренду          | Да        |
| По описанию        | Да        |
| По тегам           | Да        |
| Без регистра       | Да        |
| Ё → Е              | Да        |
| Ъ → Ь              | Да        |
| Неверная раскладка | Да        |

---

# FSM Поиск

```mermaid
stateDiagram-v2

[*] --> WaitingQuery

WaitingQuery --> Searching

Searching --> ShowResults

ShowResults --> WaitingQuery

ShowResults --> [*]
```

---

# Избранное

## Сценарий

```mermaid
sequenceDiagram

User->>Bot: Добавить в избранное

Bot->>FavoriteService: add()

FavoriteService->>FavoriteRepository: add()

FavoriteRepository->>Database: INSERT
```

---

## Ограничения

```python
MAX_FAVORITES = 30
```

---

# Корзина

## Сценарий

```mermaid
flowchart TD

ProductCard

ProductCard --> AddToCart

AddToCart --> Cart

Cart --> Checkout
```

---

## Кнопки корзины

| Кнопка | Действие             |
| ------ | -------------------- |
| ➕      | Увеличить количество |
| ➖      | Уменьшить количество |
| ❌      | Удалить товар        |
| 🧹     | Очистить корзину     |
| ✅      | Оформить заказ       |

---

# FSM Корзина

```mermaid
stateDiagram-v2

[*] --> Cart

Cart --> Checkout

Checkout --> Confirm

Confirm --> OrderCreated

OrderCreated --> [*]
```

---

# Оформление заказа

## Сценарий

```mermaid
sequenceDiagram

User->>Bot: Оформить заказ

Bot->>CartService: get_cart()

CartService-->>Bot: Cart

Bot->>OrderService: create_order()

OrderService->>OrderRepository: create()

OrderRepository->>Database: INSERT Order

OrderRepository-->>OrderService: Order

OrderService-->>Bot: Success

Bot-->>User: Заказ создан
```

---

# История заказов

```mermaid
flowchart TD

Orders

Orders --> OrderList

OrderList --> OrderDetails

OrderDetails --> RepeatOrder

OrderDetails --> ContactSeller
```

---

# Статусы заказа

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

# Уведомления

## Архитектура

```mermaid
flowchart LR

Product

Product --> NotifySubscription

NotifySubscription --> NotificationQueue

NotificationQueue --> TelegramBot

TelegramBot --> User
```

---

# Фото товара

## Архитектура

```mermaid
flowchart TD

TelegramPhoto

TelegramPhoto --> TelegramPhotoService

TelegramPhotoService --> ProductPhoto

ProductPhoto --> Database
```

---

# Альбом фотографий

```mermaid
flowchart LR

Product

Product --> ProductPhoto

ProductPhoto --> TelegramAlbumService

TelegramAlbumService --> MediaGroup
```

---

# Административный раздел

## Возможности

| Раздел       | Функция                   |
| ------------ | ------------------------- |
| Товары       | Управление товарами       |
| Категории    | Управление категориями    |
| Бренды       | Управление брендами       |
| Импорт       | XLSX импорт               |
| Фото         | Импорт ZIP                |
| Заказы       | Управление заказами       |
| Промокоды    | Управление скидками       |
| Пользователи | Управление пользователями |
| Уведомления  | Массовые рассылки         |

---

# Admin Flow

```mermaid
flowchart TD

Admin

Admin --> Products

Admin --> Categories

Admin --> Brands

Admin --> Orders

Admin --> Import

Admin --> PromoCodes

Admin --> Notifications
```

---

# Полная схема Telegram Bot

```mermaid
flowchart TD

TelegramUser

TelegramUser --> Bot

Bot --> MainMenu

MainMenu --> Categories

MainMenu --> Search

MainMenu --> Favorites

MainMenu --> Cart

MainMenu --> Orders

Categories --> ProductCard

Search --> ProductCard

Favorites --> ProductCard

ProductCard --> Cart

Cart --> Checkout

Checkout --> Order

Order --> NotificationQueue

NotificationQueue --> TelegramUser
```
