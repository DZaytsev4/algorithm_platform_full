import os
from pathlib import Path

# Базовые настройки приложения
BASE_URL = "http://localhost:8000/api"  # URL вашего Django бекенда
TOKEN_FILE = Path.home() / ".algorithm_app_token"

# Настройки окна
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

# Цвета для статусов
COLOR_APPROVED = "#d4edda"  # Светло-зеленый
COLOR_REJECTED = "#f8d7da"  # Светло-красный  
COLOR_PENDING = "#fff3cd"   # Светло-желтый
COLOR_NEUTRAL = "#f8f9fa"   # Светло-серый