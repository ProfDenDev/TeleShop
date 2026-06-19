# Admin Panel Architecture

## Назначение

Административный контур TELESHOP предназначен для управления:

* товарами;
* категориями;
* брендами;
* фотографиями;
* ценами;
* заказами;
* пользователями;
* промокодами;
* импортом;
* уведомлениями.

---

# Общая схема

```mermaid
flowchart TD

Admin

Admin --> Dashboard

Dashboard --> Products

Dashboard --> Categories

Dashboard --> Brands

Dashboard --> Orders

Dashboard --> Import

Dashboard --> Users

Dashboard --> PromoCodes

Dashboard --> Notifications
```

---

# Admin Roles

## Роли системы

| Роль            | Описание                     |
| --------------- | ---------------------------- |
| SUPER_ADMIN     | Полный доступ                |
| ADMIN           | Управление магазином         |
| MANAGER         | Работа с товарами и заказами |
| CONTENT_MANAGER | Работа с каталогом           |
| IMPORT_OPERATOR | Импорт данных                |

---

# Permission Matrix

| Раздел       | SUPER_ADMIN | ADMIN | MANAGER | CONTENT |
| ------------ | ----------- | ----- | ------- | ------- |
| Товары       | ✅           | ✅     | ✅       | ✅       |
| Категории    | ✅           | ✅     | ❌       | ✅       |
| Бренды       | ✅           | ✅     | ❌       | ✅       |
| Импорт       | ✅           | ✅     | ❌       | ❌       |
| Заказы       | ✅           | ✅     | ✅       | ❌       |
| Пользователи | ✅           | ❌     | ❌       | ❌       |
| Промокоды    | ✅           | ✅     | ❌       | ❌       |
| Настройки    | ✅           | ❌     | ❌       | ❌       |

---

# Dashboard

## Архитектура

```mermaid
flowchart LR

Dashboard

Dashboard --> ProductStats

Dashboard --> Orders

Dashboard --> Users

Dashboard --> Revenue
```

---

## Виджеты

| Виджет           | Назначение               |
| ---------------- | ------------------------ |
| Всего товаров    | Количество товаров       |
| Активные товары  | Активный каталог         |
| Проданные товары | Статистика продаж        |
| Заказы           | Количество заказов       |
| Пользователи     | Количество пользователей |
| Избранное        | Активность каталога      |
| Просмотры        | Посещаемость             |

---

# Product Management

## Архитектура

```mermaid
flowchart TD

Admin

Admin --> ProductForm

ProductForm --> ProductService

ProductService --> ProductRepository
```

---

## Возможности

| Действие      | Описание            |
| ------------- | ------------------- |
| Создать       | Новый товар         |
| Редактировать | Изменение товара    |
| Архивировать  | Переместить в архив |
| Продать       | Статус SOLD         |
| Резервировать | Статус RESERVED     |
| Удалить       | Логическое удаление |

---

# Product Lifecycle

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
```

---

# Category Management

## Архитектура

```mermaid
flowchart TD

Admin

Admin --> CategoryTree

CategoryTree --> CategoryService

CategoryService --> CategoryRepository
```

---

## Дерево категорий

```mermaid
flowchart TD

Root

Root --> Electronics

Root --> Tools

Root --> Medical

Root --> Phones

Phones --> Apple

Phones --> Samsung

Phones --> Xiaomi
```

---

# Brand Management

## Архитектура

```mermaid
flowchart LR

Admin

Admin --> BrandService

BrandService --> BrandRepository
```

---

## Возможности

| Действие        | Описание            |
| --------------- | ------------------- |
| Создание бренда | Новый бренд         |
| Редактирование  | Изменение данных    |
| Объединение     | Слияние дублей      |
| Удаление        | Логическое удаление |

---

# Photo Management

## Архитектура

```mermaid
flowchart TD

Admin

Admin --> UploadPhoto

UploadPhoto --> TelegramPhotoService

TelegramPhotoService --> ProductPhoto
```

---

## Возможности

| Действие      | Описание            |
| ------------- | ------------------- |
| Добавить фото | Загрузка            |
| Удалить фото  | Удаление            |
| Главное фото  | Назначение          |
| Сортировка    | Порядок отображения |

---

## Ограничения

```python
MAX_PRODUCT_IMAGES = 9
```

---

# Price Management

## Архитектура

```mermaid
flowchart TD

Admin

Admin --> ProductPrice

ProductPrice --> ProductPriceHistory
```

---

## Возможности

| Действие            | Описание          |
| ------------------- | ----------------- |
| Изменить цену       | Новая цена        |
| Изменить валюту     | UAH/USD/EUR       |
| Изменить тип цены   | FIXED/FROM/RANGE  |
| Просмотреть историю | История изменений |

---

# Order Management

## Архитектура

```mermaid
flowchart TD

Orders

Orders --> OrderDetails

OrderDetails --> StatusChange

StatusChange --> NotificationQueue
```

---

## Доступные действия

| Действие    | Статус              |
| ----------- | ------------------- |
| Подтвердить | PENDING → PAID      |
| Отправить   | PAID → SHIPPED      |
| Завершить   | SHIPPED → COMPLETED |
| Отменить    | PENDING → CANCELLED |

---

# Order Workflow

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

# User Management

## Архитектура

```mermaid
flowchart TD

Admin

Admin --> Users

Users --> UserProfile

UserProfile --> UserService
```

---

## Возможности

| Действие         | Описание            |
| ---------------- | ------------------- |
| Просмотр профиля | Информация          |
| Блокировка       | is_blocked          |
| Разблокировка    | Снять блокировку    |
| История заказов  | Заказы пользователя |
| Избранное        | Список избранного   |

---

# Promo Code Management

## Архитектура

```mermaid
flowchart LR

Admin

Admin --> PromoCode

PromoCode --> Orders
```

---

## Возможности

| Действие                 | Описание        |
| ------------------------ | --------------- |
| Создать купон            | Новый промокод  |
| Изменить скидку          | Процент/сумма   |
| Ограничить использование | usage_limit     |
| Отключить                | is_active=False |

---

# Import Management

## Архитектура

```mermaid
flowchart TD

Admin

Admin --> XLSX

Admin --> ZIP

Admin --> OLX

XLSX --> ImportPreview

ZIP --> ImportPreview

OLX --> ImportPreview

ImportPreview --> ImportService
```

---

## Возможности

| Действие    | Описание        |
| ----------- | --------------- |
| Импорт XLSX | Товары          |
| Импорт ZIP  | Фото            |
| Импорт OLX  | Выгрузка        |
| Preview     | Проверка ошибок |
| Rollback    | Откат импорта   |

---

# Notification Management

## Архитектура

```mermaid
flowchart TD

Admin

Admin --> Broadcast

Broadcast --> NotificationQueue

NotificationQueue --> TelegramBot
```

---

## Возможности

| Действие           | Описание           |
| ------------------ | ------------------ |
| Массовая рассылка  | Всем пользователям |
| По категории       | Выбранной группе   |
| По подписке        | Подписчикам        |
| Повторить отправку | Retry              |

---

# Audit Logging

## Архитектура

```mermaid
flowchart LR

AdminAction

AdminAction --> AuditLog

AuditLog --> Database
```

---

## Логируемые действия

| Событие                  |
| ------------------------ |
| Создание товара          |
| Изменение товара         |
| Изменение цены           |
| Изменение категории      |
| Создание заказа          |
| Изменение статуса заказа |
| Импорт                   |
| Массовая рассылка        |
| Блокировка пользователя  |

---

# Полная схема Admin System

```mermaid
flowchart TD

Admin

Admin --> Dashboard

Dashboard --> Products

Dashboard --> Categories

Dashboard --> Brands

Dashboard --> Orders

Dashboard --> Users

Dashboard --> Import

Dashboard --> PromoCodes

Dashboard --> Notifications

Products --> ProductService

Categories --> CategoryService

Brands --> BrandService

Orders --> OrderService

Import --> ImportService

Notifications --> NotificationService

ProductService --> Database

CategoryService --> Database

BrandService --> Database

OrderService --> Database

ImportService --> Database

NotificationService --> Database
```
