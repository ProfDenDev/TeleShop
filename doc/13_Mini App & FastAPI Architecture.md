# Mini App & FastAPI Architecture

## Назначение

Mini App является вторым интерфейсом TELESHOP.

Позволяет работать с магазином через Telegram WebApp.

---

# Общая архитектура

```mermaid
flowchart TD

TelegramUser

TelegramUser --> TelegramMiniApp

TelegramMiniApp --> FastAPI

FastAPI --> Services

Services --> Repositories

Repositories --> Database
```

---

# Architecture Overview

```mermaid
flowchart LR

Frontend

Frontend --> FastAPI

FastAPI --> ServiceLayer

ServiceLayer --> RepositoryLayer

RepositoryLayer --> SQLite
```

---

# Frontend Stack

## Технологии

| Компонент            | Технология          |
| -------------------- | ------------------- |
| UI                   | HTML                |
| Styles               | CSS                 |
| Logic                | JavaScript          |
| Telegram Integration | Telegram WebApp SDK |
| API                  | REST API            |
| Auth                 | Telegram InitData   |

---

# Mini App Modules

```mermaid
flowchart TD

HomePage

CatalogPage

ProductPage

FavoritesPage

CartPage

OrdersPage

ProfilePage
```

---

# Home Page

## Назначение

Главная страница приложения.

---

## Блоки

```mermaid
flowchart TD

Home

Home --> FeaturedProducts

Home --> Categories

Home --> Promotions

Home --> Search
```

---

# Catalog Page

## Архитектура

```mermaid
flowchart TD

Catalog

Catalog --> Categories

Categories --> ProductList

ProductList --> ProductCard
```

---

## Возможности

| Функция      |
| ------------ |
| Категории    |
| Подкатегории |
| Фильтры      |
| Сортировка   |
| Пагинация    |
| Поиск        |

---

# Product Page

## Архитектура

```mermaid
flowchart TD

Product

Product --> Gallery

Product --> Description

Product --> Price

Product --> RelatedProducts

Product --> AddToCart
```

---

## Компоненты

| Блок           |
| -------------- |
| Фото           |
| Цена           |
| Описание       |
| Характеристики |
| Видео          |
| Отзывы         |
| Рекомендации   |

---

# Favorites Page

```mermaid
flowchart LR

Favorites

Favorites --> ProductList

ProductList --> ProductCard
```

---

# Cart Page

## Архитектура

```mermaid
flowchart TD

Cart

Cart --> CartItems

CartItems --> Checkout
```

---

# Checkout Page

```mermaid
flowchart TD

Cart

Cart --> PromoCode

PromoCode --> TotalPrice

TotalPrice --> CreateOrder
```

---

# Orders Page

```mermaid
flowchart TD

Orders

Orders --> OrderList

OrderList --> OrderDetails
```

---

# Profile Page

## Данные пользователя

| Поле            |
| --------------- |
| Telegram ID     |
| Username        |
| Телефон         |
| Язык            |
| История заказов |

---

# Authentication

## Схема авторизации

```mermaid
sequenceDiagram

Telegram->>MiniApp: initData

MiniApp->>FastAPI: initData

FastAPI->>AuthService: validate()

AuthService-->>FastAPI: User

FastAPI-->>MiniApp: JWT Session
```

---

# Auth Flow

```mermaid
flowchart LR

TelegramInitData

TelegramInitData --> Validate

Validate --> User

User --> Session
```

---

# FastAPI Structure

```text
app/api/

├── routers/
├── dependencies/
├── middleware/
├── schemas/
├── responses/
└── exceptions/
```

---

# API Routers

```mermaid
flowchart TD

ProductsRouter

CategoriesRouter

BrandsRouter

SearchRouter

FavoritesRouter

CartRouter

OrdersRouter

UsersRouter
```

---

# Products Router

## Endpoints

| Method | Endpoint       |
| ------ | -------------- |
| GET    | /products      |
| GET    | /products/{id} |
| POST   | /products      |
| PATCH  | /products/{id} |
| DELETE | /products/{id} |

---

# Categories Router

| Method | Endpoint         |
| ------ | ---------------- |
| GET    | /categories      |
| GET    | /categories/tree |
| GET    | /categories/{id} |

---

# Search Router

| Method | Endpoint         |
| ------ | ---------------- |
| GET    | /search          |
| GET    | /search/products |

---

# Favorites Router

| Method | Endpoint        |
| ------ | --------------- |
| GET    | /favorites      |
| POST   | /favorites      |
| DELETE | /favorites/{id} |

---

# Cart Router

| Method | Endpoint     |
| ------ | ------------ |
| GET    | /cart        |
| POST   | /cart/add    |
| PATCH  | /cart/update |
| DELETE | /cart/remove |

---

# Orders Router

| Method | Endpoint     |
| ------ | ------------ |
| GET    | /orders      |
| GET    | /orders/{id} |
| POST   | /orders      |

---

# API Request Flow

```mermaid
sequenceDiagram

MiniApp->>FastAPI: HTTP Request

FastAPI->>Service

Service->>Repository

Repository->>Database

Database-->>Repository

Repository-->>Service

Service-->>FastAPI

FastAPI-->>MiniApp
```

---

# Service Layer

```mermaid
flowchart TD

ProductService

CategoryService

FavoriteService

CartService

OrderService

SearchService

NotificationService
```

---

# Repository Layer

```mermaid
flowchart TD

ProductRepository

CategoryRepository

BrandRepository

FavoriteRepository

CartRepository

OrderRepository

NotificationRepository
```

---

# API Error Handling

## Архитектура

```mermaid
flowchart LR

Exception

Exception --> ErrorHandler

ErrorHandler --> APIResponse
```

---

## Формат ошибки

```json
{
  "success": false,
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product not found"
  }
}
```

---

# API Success Response

```json
{
  "success": true,
  "data": {}
}
```

---

# Pagination

## Формат

```mermaid
flowchart LR

Request

Request --> limit

Request --> offset

Request --> sort

Request --> filters
```

---

## Пример

```http
GET /products?limit=20&offset=0
```

---

# Deployment Architecture

```mermaid
flowchart TD

Telegram

Telegram --> MiniApp

MiniApp --> Nginx

Nginx --> FastAPI

FastAPI --> SQLite

FastAPI --> BackgroundTasks

BackgroundTasks --> NotificationQueue
```

---

# Future PostgreSQL Migration

```mermaid
flowchart LR

SQLite

SQLite --> SQLAlchemy

SQLAlchemy --> PostgreSQL
```

---

# Full Mini App Architecture

```mermaid
flowchart TD

TelegramUser

TelegramUser --> MiniApp

MiniApp --> FastAPI

FastAPI --> ProductService

FastAPI --> SearchService

FastAPI --> CartService

FastAPI --> OrderService

ProductService --> ProductRepository

SearchService --> ProductRepository

CartService --> CartRepository

OrderService --> OrderRepository

ProductRepository --> Database

CartRepository --> Database

OrderRepository --> Database
```

---

# TELESHOP System Overview

```mermaid
flowchart TD

TelegramUser

TelegramUser --> TelegramBot

TelegramUser --> MiniApp

TelegramBot --> ServiceLayer

MiniApp --> FastAPI

FastAPI --> ServiceLayer

ServiceLayer --> RepositoryLayer

RepositoryLayer --> Database

ImportSystem --> ServiceLayer

NotificationSystem --> TelegramBot

AdminPanel --> ServiceLayer
```
