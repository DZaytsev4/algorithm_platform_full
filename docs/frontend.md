## Frontend (Vite/React)

### Требования

- Node.js 18+ (рекомендуется 20+)

### Установка

```bash
cd frontend
npm install
```

### Запуск

```bash
cd frontend
npm run dev
```

По умолчанию dev-сервер работает на `http://localhost:3000`.

### Настройка API base URL

В `frontend/src/service/api.ts` используется `VITE_API_BASE_URL` (если задан), иначе `http://localhost:8000/api`.

Пример `.env` для фронтенда:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

