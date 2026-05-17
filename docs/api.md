## API контракты

Базовый префикс: `/api`

### Аутентификация (JWT)

- `POST /api/token/` — получить `access` и `refresh`
- `POST /api/token/refresh/` — обновить `access`

### Core

- `GET /api/` — приветственное сообщение

### Users

- `POST /api/users/register/` — регистрация
- `GET /api/users/me/` — текущий пользователь (включает `role`, `groups`, `is_staff`, `is_superuser`)
- `PATCH /api/users/me/` — обновление профиля
- `GET /api/users/me/purchases/` — покупки текущего пользователя
- `GET /api/users/search/?username=...` — поиск пользователей
- `GET /api/users/<username>/` — профиль пользователя
- `GET /api/users/<username>/algorithms/` — алгоритмы пользователя

### Algorithms

- `GET /api/algorithms/?q=...` — список алгоритмов (поиск по `q`)
- `POST /api/algorithms/` — создать алгоритм
- `GET /api/algorithms/<id>/` — получить алгоритм
- `PATCH /api/algorithms/<id>/` — обновить (только автор)
- `DELETE /api/algorithms/<id>/` — удалить (только автор)

Покупки и цены:
- `POST /api/algorithms/<id>/purchase/` — “покупка” (создаёт запись покупки)
- `GET /api/algorithms/<id>/price-history/` — история цены (для платных)

Модерация (только модератор):
- `GET /api/algorithms/moderation/` — список pending
- `POST /api/algorithms/moderation/<id>/` — принять/отклонить

