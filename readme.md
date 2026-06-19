# TELESHOP

TELESHOP — Telegram Marketplace / Telegram Shop на Python.

Проект представляет собой современный Telegram-магазин с поддержкой:

* Telegram Bot (aiogram 3.x)
* Telegram Mini App
* FastAPI API
* SQLite / PostgreSQL
* Repository Pattern
* Service Layer Architecture
* Импорта товаров из XLSX, ZIP и OLX
* Избранного
* Корзины
* Заказов
* Уведомлений
* Каталога товаров
* Полнотекстового поиска

---

## Архитектура

Полная архитектурная документация находится в файле:

```text
TELESHOP_ALL_19_DOCS.md
```

Документ содержит:

* Общую архитектуру
* Database Design
* API Architecture
* Telegram Bot Architecture
* Repository Layer
* Database Schema
* Import System
* Search Engine
* Pricing & Commerce
* Notification System
* Admin Panel
* FSM Architecture
* Mini App & FastAPI
* Repository Contracts
* Service Workflows
* Database Models Specification

---

## Технологический стек

### Backend

* Python 3.11+
* aiogram 3.x
* FastAPI
* SQLAlchemy 2.x
* Alembic
* Pydantic

### Database

* SQLite (development)
* PostgreSQL (production)

### Frontend

* Telegram Mini App
* HTML
* CSS
* JavaScript

---

## Основные возможности

### Каталог товаров

* категории
* подкатегории
* бренды
* SEO slug
* фильтрация

### Поиск

* поиск по названию
* поиск по SKU
* поиск по бренду
* поиск по описанию
* исправление раскладки
* нормализация текста

### Корзина

* добавление товаров
* изменение количества
* оформление заказа

### Избранное

* список избранных товаров
* подписка на изменение цены

### Импорт

Поддерживаются:

* XLSX
* ZIP с фотографиями
* OLX JSON

### Уведомления

* изменение цены
* появление товара
* статусы заказов
* массовые рассылки

---

## Структура проекта

```text
app/

├── admin/
├── api/
├── bot/
├── constants/
├── database/
├── imports/
├── services/
├── tasks/
├── utils/
├── locales/
└── seeds/
```

---

## Архитектурные принципы

* Repository Pattern
* Service Layer
* Soft Delete
* Integer Money Storage
* UUID для публичных идентификаторов
* Telegram File Storage
* SQLite First, PostgreSQL Ready

---

## Статус проекта

```text
WORK IN PROGRESS
```

Документация актуальна и отражает текущее состояние архитектуры проекта TELESHOP.
