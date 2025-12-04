import requests
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import config

class APIClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.BASE_URL
        self.token = None
        self.load_token()
    
    def load_token(self):
        """Загружает токен из файла"""
        try:
            if config.TOKEN_FILE.exists():
                with open(config.TOKEN_FILE, 'r') as f:
                    data = json.load(f)
                    self.token = data.get('access')
        except Exception:
            self.token = None
    
    def save_token(self, access_token: str) -> bool:
        """Сохраняет токен в файл"""
        try:
            with open(config.TOKEN_FILE, 'w') as f:
                json.dump({'access': access_token}, f)
            self.token = access_token
            return True
        except Exception:
            return False
    
    def clear_token(self):
        """Удаляет токен"""
        try:
            if config.TOKEN_FILE.exists():
                config.TOKEN_FILE.unlink()
            self.token = None
        except Exception:
            pass
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[requests.Response]:
        """Общий метод для выполнения запросов"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                timeout=10,
                **kwargs
            )
            return response
        except requests.exceptions.ConnectionError:
            print(f"Ошибка подключения к серверу: {url}")
            return None
        except requests.exceptions.Timeout:
            print(f"Таймаут подключения к серверу: {url}")
            return None
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return None
    
    def login(self, username: str, password: str) -> bool:
        """Аутентификация"""
        data = {
            'username': username,
            'password': password
        }
        response = self._make_request('POST', '/token/', json=data)
        
        if response and response.status_code == 200:
            try:
                tokens = response.json()
                if 'access' in tokens:
                    return self.save_token(tokens['access'])
            except:
                pass
        return False
    
    def register(self, username: str, email: str, password1: str, password2: str) -> bool:
        """Регистрация"""
        data = {
            'username': username,
            'email': email,
            'password': password1,
            'password2': password2
        }
        response = self._make_request('POST', '/users/register/', json=data)
        return response is not None and response.status_code == 201
    
    def get_algorithms(self, search: str = "", show_all: bool = False) -> List[Dict]:
        """Получение списка алгоритмов"""
        params = {'q': search} if search else {}
        response = self._make_request('GET', '/algorithms/', params=params)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                # Проверяем, что это список
                if isinstance(data, list):
                    # Если не показывать все, фильтруем по статусу approved
                    if not show_all:
                        filtered_data = []
                        for item in data:
                            if isinstance(item, dict):
                                status = item.get('status')
                                # Показываем только одобренные алгоритмы
                                if status == 'approved':
                                    filtered_data.append(item)
                        return filtered_data
                    return data
                elif isinstance(data, dict) and 'results' in data:
                    # Если пагинация включена
                    results = data.get('results', [])
                    if not show_all:
                        filtered_results = []
                        for item in results:
                            if isinstance(item, dict):
                                status = item.get('status')
                                if status == 'approved':
                                    filtered_results.append(item)
                        return filtered_results
                    return results
                else:
                    print(f"Неожиданный формат ответа: {type(data)}")
                    return []
            except Exception as e:
                print(f"Ошибка парсинга JSON: {e}")
                return []
        return []
    
    def get_algorithm(self, algorithm_id: int) -> Optional[Dict]:
        """Получение одного алгоритма"""
        response = self._make_request('GET', f'/algorithms/{algorithm_id}/')
        
        if response and response.status_code == 200:
            try:
                return response.json()
            except:
                pass
        return None
    
    def create_algorithm(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Создание алгоритма"""
        response = self._make_request('POST', '/algorithms/', json=data)
        
        if response and response.status_code == 201:
            try:
                return response.json()
            except:
                pass
        return None
    
    def update_algorithm(self, algorithm_id: int, data: Dict[str, Any]) -> bool:
        """Обновление алгоритма"""
        response = self._make_request('PUT', f'/algorithms/{algorithm_id}/', json=data)
        return response is not None and response.status_code == 200
    
    def delete_algorithm(self, algorithm_id: int) -> bool:
        """Удаление алгоритма"""
        response = self._make_request('DELETE', f'/algorithms/{algorithm_id}/')
        return response is not None and response.status_code == 204
    
    def get_moderation_list(self) -> List[Dict]:
        """Список на модерацию (только для модераторов)"""
        response = self._make_request('GET', '/algorithms/moderation/')
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    return data
                return []
            except:
                pass
        return []
    
    def moderate_algorithm(self, algorithm_id: int, status: str, reason: str = "") -> bool:
        """Модерация алгоритма"""
        data = {
            'status': status,
            'rejection_reason': reason if status == 'rejected' else ''
        }
        response = self._make_request('POST', f'/algorithms/moderation/{algorithm_id}/', json=data)
        return response is not None and response.status_code == 200
    
    def get_current_user(self) -> Optional[Dict]:
        """Получение данных текущего пользователя"""
        response = self._make_request('GET', '/users/me/')
        
        if response and response.status_code == 200:
            try:
                return response.json()
            except:
                pass
        return None
    
    def get_user_algorithms(self, username: str) -> List[Dict]:
        """Получение алгоритмов пользователя (все, включая отклоненные)"""
        response = self._make_request('GET', f'/users/{username}/algorithms/')
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    return data
                return []
            except:
                pass
        return []