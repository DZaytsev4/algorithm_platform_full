# Algorithm Platform

Платформа для работы с алгоритмами: **Django REST Framework** на бэкенде и **React + Vite** на фронтенде, оба запускаются через Docker Compose.

## Быстрый старт

1. Клонируйте репозиторий:

```bash
git clone https://github.com/DZaytsev4/algorithm_platform_full.git
cd algorithm_platform_full
```

2. Запустите все сервисы через Docker Compose:

```bash
docker compose up --build
```

3. Откройте фронтенд в браузере:

- `http://localhost:5173`

4. API доступен по адресу:

- `http://127.0.0.1:8000/api`

## Что важно знать

- `docker compose up --build` поднимает:
  - PostgreSQL
  - Django backend
  - React frontend
- Backend слушает на `http://127.0.0.1:8000`
- Frontend слушает на `http://localhost:5173`
- Фронтенд использует `VITE_API_BASE_URL=http://localhost:8000/api`

## Работа с Docker

Остановить сервисы:

```bash
docker compose down
```

Посмотреть логи:

```bash
docker compose logs -f
```

Запустить только backend:

```bash
docker compose up --build backend
```

Запустить только frontend:

```bash
docker compose up --build frontend
```

## Запуск тестов

Тесты выполняются внутри контейнера backend.

```bash
docker compose run --rm backend python manage.py test
```

Отдельные группы:

```bash
docker compose run --rm backend python manage.py test users.tests
docker compose run --rm backend python manage.py test algorithms.tests
```

## Заполнение стартовых данных

Для создания базовых пользователей и алгоритмов используйте команду:

```bash
docker compose run --rm backend python manage.py seed_initial_data
```

Это создаст:
- `admin` / `adminpass123`
- `moderator` / `modpass123`
- `user1` / `user1pass123`
- `user2` / `user2pass123`
- 5 алгоритмов: 3 бесплатных и 2 платных

## Доступ к базе PostgreSQL

PostgreSQL запускается в контейнере и проброшен на локальный порт `5433`.

Для подключения через PGAdmin используйте:
- Host name / address: `localhost`
- Port: `5433`
- Maintenance database: `postgres` или `algorithm_platform`
- Username: `algorithm_user`
- Password: `algorithm_password`
- Database: `algorithm_platform`

Если вы запускаете PGAdmin тоже в контейнере или другом сервисе внутри Docker-сети, хост может быть `postgres`.

## Основные группы тестов

### `backend/users/tests.py`
- `UserViewsTests` — проверка API регистрации, аутентификации, профилей, поиска пользователей и доступа к алгоритмам пользователя.
- `UserFormsTests` — валидация регистрационной формы, проверка пароля и дубликатов email.
- `UserSerializersTests` — регистрационные сериализаторы, валидация полей и выходные данные пользователя.

### `backend/algorithms/tests.py`
- `AlgorithmModelTests` — тесты модели `Algorithm`, поведение статусов, теги, права редактирования, строковое представление.
- `AlgorithmSerializerTests` — валидация сериализатора, обязательные поля, computed-поля и статус по умолчанию.
- `PermissionTests` — логика кастомного пермишена `IsModerator`.
- `AlgorithmBusinessLogicTests` — временные метки, модерация и отклонение алгоритмов.
- `AlgorithmValidationTests` — проверки ограничений модели (`name`, `code` и т.п.).
- `AlgorithmViewsTests` — интеграционные API-тесты списка, поиска, создания, редактирования, удаления, запуска алгоритма и модерации.

> Тесты бэкенда выполняются в Docker. Фронтенд в проекте не имеет отдельного набора тестов.

## CI / GitHub Actions

В проекте используется GitHub Actions для автоматизированного запуска тестов и отчётности.

- `.github/workflows/unit-tests.yml` — Django unit-тесты для алгоритмов: модели, сериализаторы, права и бизнес-логику.
- `.github/workflows/user-tests.yml` — проверка пользовательских сценариев API: создание, изменение и удаление алгоритмов, доступ обычных пользователей.
- `.github/workflows/moderator-tests.yml` — модераторские сценарии: доступ к списку модерации, одобрение и отклонение.
- `.github/workflows/search-coverage-tests.yml` — тест фильтрации поиска и полный запуск `AlgorithmViewsTests` с отчётом покрытия.
- `.github/workflows/users-comprehensive-tests.yml` — полный набор `users` тестов, отчёт о покрытии и security scan для модуля `users`.

> CI использует Python 3.9 и PostgreSQL в GitHub Actions, а локально проект поднимается через Docker Compose.

## Быстрая справка команд

| Задача | Команда |
|---|---|
| Запустить проект | `docker compose up --build` |
| Остановить проект | `docker compose down` |
| Запустить все тесты | `docker compose run --rm backend python manage.py test` |
| Проверить логи | `docker compose logs -f` |
| Запустить только backend | `docker compose up --build backend` |
| Запустить только frontend | `docker compose up --build frontend` |

## Дополнительно

- Backend и frontend запускаются через Docker Compose.
- PostgreSQL настроен в `docker-compose.yml` и проброшен на порт `5433` локально.
- Backend автоматически выполняет миграции через `backend/entrypoint.sh`.
- Фронтенд использует `VITE_API_BASE_URL=http://localhost:8000/api`.
