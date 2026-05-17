## Backend (Django)

### Требования

- Python 3.10+ (рекомендуется 3.11)

### Установка

Из корня репозитория:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Запуск

```bash
python backend/manage.py migrate
python backend/manage.py runserver 0.0.0.0:8000
```

### Переменные окружения

Поддерживаются:

- `DJANGO_SECRET_KEY`: секретный ключ Django
- `DJANGO_DEBUG`: `"True"` или `"False"`

Если переменные не заданы, используются значения по умолчанию (для dev).

### CORS

Разрешённые origin-ы настраиваются в `backend/algorithm_service/settings.py`.
По умолчанию добавлены порты `3000` (Vite в этом проекте) и дополнительные `5173/4173` как частые значения.

