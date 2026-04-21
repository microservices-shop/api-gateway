# API Gateway

> Микросервис для интернет-магазина электроники. Главный репозиторий: [microservices-shop/overview](https://github.com/microservices-shop/overview)

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.132-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![httpx](https://img.shields.io/badge/httpx-0.28-0096D6?style=for-the-badge)
![Pydantic](https://img.shields.io/badge/Pydantic-2.12-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![structlog](https://img.shields.io/badge/structlog-25.5-000000?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-24-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## Описание

Единая точка входа для всех клиентских запросов в микросервисную архитектуру интернет-магазина.

API Gateway принимает запросы от фронтенда через Nginx, проверяет JWT токены для защищённых эндпоинтов и маршрутизирует запросы к микросервисам (Auth, Product, Cart, Order). Централизует аутентификацию, логирование и retry логику — микросервисы получают уже валидированные запросы с данными пользователя в заголовках.

**Основной функционал:**
- **Маршрутизация запросов** — перенаправление запросов в Auth Service, Product Service, Cart Service, Order Service по префиксам путей
- **Централизованная аутентификация** — проверка JWT токенов и извлечение данных пользователя (user_id, email, role) для передачи во внутренние сервисы через заголовки
- **Retry механизм** — автоматические повторные попытки при недоступности сервисов с exponential backoff
- **Структурированное логирование** — request tracing с автоматическим добавлением request_id

## Структура проекта

```
api-gateway/
├── src/
│   ├── routes/
│   │   ├── auth.py                
│   │   ├── products.py            
│   │   ├── categories.py          
│   │   ├── attributes.py          
│   │   ├── cart.py                
│   │   ├── order.py              
│   │   └── users.py               
│   ├── services/
│   │   └── health.py              
│   ├── middleware/
│   │   └── request_logger.py     
│   ├── schemas/                   # Pydantic схемы
│   ├── proxy.py                   # HTTP клиент для проксирования
│   ├── dependencies.py            # JWT валидация и зависимости
│   ├── config.py                  # Конфигурация (pydantic-settings)
│   ├── logger.py                  
│   ├── exceptions.py              
│   └── main.py                    # Точка входа приложения
├── pyproject.toml                 
├── .env.example                  
└── README.md
```

## API

Сервис запускается на порту **8000**. Интерактивная документация доступна по адресу `http://localhost:8000/docs` (Swagger UI).


## Аутентификация

API Gateway проверяет JWT токены для защищённых эндпоинтов:

1. Извлекает `Authorization: Bearer <token>` из заголовков запроса
2. Валидирует подпись токена с помощью `JWT_SECRET_KEY`
3. Извлекает данные пользователя: `user_id`, `email`, `role`
4. Добавляет заголовки `X-User-Id`, `X-User-Email`, `X-User-Role` при проксировании запроса во внутренние сервисы

## Установка и запуск

### Требования

- Python 3.12+

### Разработка

```bash
# Установка зависимостей
uv sync

cp .env.example .env

# Запуск сервиса
uvicorn src.main:app --reload --port 8000 --no-access-log
```

### Production

```bash
docker-compose up --build -d
```
