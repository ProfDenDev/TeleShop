# Telegram Bot FSM Architecture

## Назначение

Telegram Bot является основным пользовательским интерфейсом TELESHOP.

Построен на:

```text
aiogram 3.x
FSM
Router-based architecture
```

---

# Общая схема

```mermaid
flowchart TD

TelegramUser

TelegramUser --> Router

Router --> Handler

Handler --> Service

Service --> Repository

Repository --> Database
```

---

# Bot Structure

```text
app/bot/

├── handlers/
│
├── keyboards/
│
├── callbacks/
│
├── states/
│
├── filters/
│
├── middlewares/
│
├── routers/
│
└── utils/
```

---

# Router Architecture

```mermaid
flowchart LR

MainRouter

CatalogRouter

SearchRouter

FavoriteRouter

CartRouter

OrderRouter

AdminRouter
```

---

# Main Menu FSM

```mermaid
stateDiagram-v2

[*] --> MainMenu

MainMenu --> Catalog

MainMenu --> Search

MainMenu --> Favorites

MainMenu --> Cart

MainMenu --> Orders

MainMenu --> Contacts
```

---

# Main Menu Buttons

| Кнопка      | Назначение        |
| ----------- | ----------------- |
| 🏪 Каталог  | Категории товаров |
| 🔍 Поиск    | Поиск товаров     |
| ⭐ Избранное | Избранные товары  |
| 🛒 Корзина  | Корзина           |
| 📦 Заказы   | История заказов   |
| ☎ Контакты  | Контакты          |

---

# Catalog FSM

## Навигация

```mermaid
stateDiagram-v2

[*] --> Categories

Categories --> SubCategory

SubCategory --> ProductList

ProductList --> ProductCard

ProductCard --> ProductList

ProductList --> SubCategory

SubCategory --> Categories
```

---

# Catalog Flow

```mermaid
flowchart TD

RootCategories

RootCategories --> Category

Category --> SubCategory

SubCategory --> ProductList

ProductList --> ProductCard
```

---

# Product Card FSM

```mermaid
stateDiagram-v2

[*] --> ProductCard

ProductCard --> Gallery

ProductCard --> AddToFavorites

ProductCard --> AddToCart

ProductCard --> ContactSeller

ProductCard --> ShareProduct
```

---

# Product Card Buttons

| Кнопка        | Действие             |
| ------------- | -------------------- |
| 🛒 Купить     | Добавить в корзину   |
| ⭐ Избранное   | Добавить в избранное |
| 🖼 Фото       | Галерея              |
| 🎥 Видео      | Видео товара         |
| 📤 Поделиться | Ссылка               |
| ☎ Связаться   | Контакты             |

---

# Search FSM

```mermaid
stateDiagram-v2

[*] --> WaitingQuery

WaitingQuery --> Searching

Searching --> Results

Results --> ProductCard

ProductCard --> Results
```

---

# Search Flow

```mermaid
flowchart LR

UserQuery

UserQuery --> SearchService

SearchService --> ProductRepository

ProductRepository --> Results

Results --> User
```

---

# Search States

| State        | Назначение              |
| ------------ | ----------------------- |
| WaitingQuery | Ожидание текста         |
| Searching    | Выполнение поиска       |
| Results      | Отображение результатов |
| ProductCard  | Карточка товара         |

---

# Favorite FSM

```mermaid
stateDiagram-v2

[*] --> Favorites

Favorites --> ProductCard

ProductCard --> RemoveFavorite

RemoveFavorite --> Favorites
```

---

# Cart FSM

```mermaid
stateDiagram-v2

[*] --> Cart

Cart --> UpdateQuantity

Cart --> RemoveItem

Cart --> Checkout

Checkout --> ConfirmOrder

ConfirmOrder --> OrderCreated

OrderCreated --> [*]
```

---

# Cart Flow

```mermaid
flowchart TD

Product

Product --> Cart

Cart --> Checkout

Checkout --> Order
```

---

# Cart Buttons

| Кнопка | Назначение           |
| ------ | -------------------- |
| ➕      | Увеличить количество |
| ➖      | Уменьшить количество |
| ❌      | Удалить товар        |
| 🧹     | Очистить корзину     |
| ✅      | Оформить заказ       |

---

# Checkout FSM

```mermaid
stateDiagram-v2

[*] --> ReviewOrder

ReviewOrder --> ApplyPromo

ApplyPromo --> ConfirmOrder

ConfirmOrder --> CreateOrder

CreateOrder --> Success
```

---

# Order FSM

```mermaid
stateDiagram-v2

[*] --> Orders

Orders --> OrderDetails

OrderDetails --> RepeatOrder

OrderDetails --> ContactManager
```

---

# Order Creation Sequence

```mermaid
sequenceDiagram

User->>Bot: Оформить заказ

Bot->>CartService: get_cart()

CartService-->>Bot: Cart

Bot->>OrderService: create_order()

OrderService->>OrderRepository: create()

OrderRepository-->>OrderService: Order

OrderService-->>Bot: Success

Bot-->>User: Заказ создан
```

---

# Callback Architecture

## Формат

```text
action:id
```

---

## Примеры

```text
product:125

category:12

favorite:add:125

favorite:remove:125

cart:add:125

cart:remove:125

order:456
```

---

# Callback Flow

```mermaid
flowchart LR

CallbackQuery

CallbackQuery --> CallbackFactory

CallbackFactory --> Handler

Handler --> Service
```

---

# Keyboard Architecture

```mermaid
flowchart TD

KeyboardBuilder

KeyboardBuilder --> ReplyKeyboard

KeyboardBuilder --> InlineKeyboard
```

---

# Reply Keyboards

| Клавиатура        | Назначение          |
| ----------------- | ------------------- |
| MainMenuKeyboard  | Главное меню        |
| AdminMenuKeyboard | Меню администратора |
| ContactKeyboard   | Контакты            |

---

# Inline Keyboards

| Клавиатура       | Назначение      |
| ---------------- | --------------- |
| ProductKeyboard  | Карточка товара |
| CategoryKeyboard | Категория       |
| FavoriteKeyboard | Избранное       |
| CartKeyboard     | Корзина         |
| OrderKeyboard    | Заказ           |

---

# Middleware Architecture

```mermaid
flowchart LR

Update

Update --> LoggingMiddleware

LoggingMiddleware --> UserMiddleware

UserMiddleware --> LanguageMiddleware

LanguageMiddleware --> Handler
```

---

# User Middleware

## Задачи

* регистрация пользователя;
* обновление активности;
* загрузка профиля;
* проверка блокировки.

---

# Language Middleware

## Задачи

* выбор языка;
* локализация сообщений;
* перевод интерфейса.

---

# Admin FSM

## Общая схема

```mermaid
stateDiagram-v2

[*] --> AdminMenu

AdminMenu --> Products

AdminMenu --> Categories

AdminMenu --> Orders

AdminMenu --> Import

AdminMenu --> Users

AdminMenu --> PromoCodes
```

---

# Product Creation FSM

```mermaid
stateDiagram-v2

[*] --> EnterTitle

EnterTitle --> EnterCategory

EnterCategory --> EnterBrand

EnterBrand --> EnterPrice

EnterPrice --> EnterDescription

EnterDescription --> UploadPhotos

UploadPhotos --> Confirm

Confirm --> ProductCreated
```

---

# XLSX Import FSM

```mermaid
stateDiagram-v2

[*] --> UploadXLSX

UploadXLSX --> Preview

Preview --> Validation

Validation --> Import

Import --> Completed
```

---

# Photo Import FSM

```mermaid
stateDiagram-v2

[*] --> UploadZIP

UploadZIP --> Extract

Extract --> Validation

Validation --> ImportPhotos

ImportPhotos --> Completed
```

---

# Broadcast FSM

```mermaid
stateDiagram-v2

[*] --> CreateMessage

CreateMessage --> Preview

Preview --> Confirm

Confirm --> Send

Send --> Completed
```

---

# Bot Services Interaction

```mermaid
flowchart TD

Bot

Bot --> ProductService

Bot --> SearchService

Bot --> FavoriteService

Bot --> CartService

Bot --> OrderService

Bot --> NotificationService
```

---

# Complete Telegram Bot Diagram

```mermaid
flowchart TD

TelegramUser

TelegramUser --> MainMenu

MainMenu --> Catalog

MainMenu --> Search

MainMenu --> Favorites

MainMenu --> Cart

MainMenu --> Orders

Catalog --> ProductCard

Search --> ProductCard

Favorites --> ProductCard

ProductCard --> Cart

Cart --> Checkout

Checkout --> Order

Order --> NotificationQueue

NotificationQueue --> TelegramUser

Admin --> AdminMenu

AdminMenu --> Products

AdminMenu --> Orders

AdminMenu --> Import

AdminMenu --> Notifications
```
