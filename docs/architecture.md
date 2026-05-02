## Архитектура

### Общая схема

- **Backend**: Django + DRF + JWT (`backend/`)
- **Frontend**: Vite + React (`frontend/`)
- **API base**: по умолчанию `http://localhost:8000/api`

### Backend структура

Проект Django: `backend/algorithm_service/`

Apps:
- `backend/core/`: базовые/тестовые эндпоинты (например, health/home).
- `backend/users/`: регистрация, профиль, текущий пользователь, покупки.
- `backend/algorithms/`: алгоритмы, модерация, покупка, история цены.

#### Роли и права

Единая логика ролей хранится в `backend/users/services/roles.py`:
- `get_role(user) -> "admin" | "moderator" | "consumer"`
- `is_moderator(user) -> bool`

Фронтенд использует поле `role`, которое отдаёт `/api/users/me/`.

