#!/usr/bin/env python3
"""
Главный файл приложения Algorithm Manager Desktop
"""

import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_client import APIClient
from ui.main_window import MainWindow
import config

def setup_application():
    """Настройка приложения"""
    app = QApplication(sys.argv)
    
    # Настройка шрифтов
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Настройка стиля
    app.setStyle("Fusion")
    
    return app

def check_server_connection(api_client):
    """Проверка соединения с сервером"""
    try:
        # Пробуем получить список алгоритмов без токена
        response = api_client._make_request('GET', '/algorithms/')
        if response:
            print(f"Сервер доступен. Статус: {response.status_code}")
            return True
        return False
    except Exception as e:
        print(f"Ошибка подключения к серверу: {e}")
        return False

def main():
    """Главная функция"""
    try:
        # Создаем приложение
        app = setup_application()
        
        # Создаем API клиент
        api_client = APIClient()
        
        # Проверяем соединение с сервером
        if not check_server_connection(api_client):
            reply = QMessageBox.warning(
                None, "Ошибка соединения",
                f"Не удается подключиться к серверу по адресу: {config.BASE_URL}\n"
                "Убедитесь, что:\n"
                "1. Сервер Django запущен\n"
                "2. Адрес сервера правильный\n"
                "3. Сервер доступен из сети\n\n"
                "Хотите продолжить в автономном режиме?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                sys.exit(1)
        
        # Создаем главное окно
        window = MainWindow(api_client)
        window.show()
        
        # Запускаем приложение
        return app.exec_()
        
    except Exception as e:
        # Обработка неожиданных ошибок
        error_msg = f"Критическая ошибка:\n{str(e)}\n\n{traceback.format_exc()}"
        print(error_msg)
        
        QMessageBox.critical(
            None, "Критическая ошибка",
            f"Произошла критическая ошибка:\n{str(e)}\n\n"
            "Попробуйте перезапустить приложение."
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())