from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import config

class LoginDialog(QDialog):
    login_success = pyqtSignal()
    
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api = api_client
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(400, 300)
        self.setModal(True)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Заголовок
        title_label = QLabel("Algorithm Manager")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Вкладки
        self.tabs = QTabWidget()
        
        # Вкладка входа
        login_tab = QWidget()
        login_layout = QVBoxLayout(login_tab)
        login_layout.setContentsMargins(20, 20, 20, 20)
        
        # Поля входа
        form_layout = QFormLayout()
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Введите имя пользователя")
        
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Введите пароль")
        self.login_password.setEchoMode(QLineEdit.Password)
        
        form_layout.addRow("Имя пользователя:", self.login_username)
        form_layout.addRow("Пароль:", self.login_password)
        
        login_layout.addLayout(form_layout)
        
        # Кнопка входа
        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.do_login)
        self.login_btn.setDefault(True)
        login_layout.addWidget(self.login_btn)
        
        # Вкладка регистрации
        register_tab = QWidget()
        register_layout = QVBoxLayout(register_tab)
        register_layout.setContentsMargins(20, 20, 20, 20)
        
        # Поля регистрации
        reg_form_layout = QFormLayout()
        
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Введите имя пользователя")
        
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Введите email")
        
        self.reg_password1 = QLineEdit()
        self.reg_password1.setPlaceholderText("Введите пароль")
        self.reg_password1.setEchoMode(QLineEdit.Password)
        
        self.reg_password2 = QLineEdit()
        self.reg_password2.setPlaceholderText("Подтвердите пароль")
        self.reg_password2.setEchoMode(QLineEdit.Password)
        
        reg_form_layout.addRow("Имя пользователя*:", self.reg_username)
        reg_form_layout.addRow("Email*:", self.reg_email)
        reg_form_layout.addRow("Пароль*:", self.reg_password1)
        reg_form_layout.addRow("Подтверждение*:", self.reg_password2)
        
        register_layout.addLayout(reg_form_layout)
        
        # Кнопка регистрации
        self.register_btn = QPushButton("Зарегистрироваться")
        self.register_btn.clicked.connect(self.do_register)
        register_layout.addWidget(self.register_btn)
        
        self.tabs.addTab(login_tab, "Вход")
        self.tabs.addTab(register_tab, "Регистрация")
        layout.addWidget(self.tabs)
        
        # Статус
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        
        # Кнопка выхода
        exit_btn = QPushButton("Выход")
        exit_btn.clicked.connect(self.reject)
        layout.addWidget(exit_btn)
        
        # Стили
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
                border-radius: 4px;
            }
        """)
    
    def do_login(self):
        """Выполнение входа"""
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()
        
        if not username or not password:
            self.show_error("Заполните все поля")
            return
        
        # Блокируем кнопку на время выполнения
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Вход...")
        QApplication.processEvents()
        
        if self.api.login(username, password):
            self.show_success("Успешный вход!")
            QTimer.singleShot(500, self.accept_login)
        else:
            self.show_error("Ошибка входа. Проверьте данные.")
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Войти")
    
    def do_register(self):
        """Выполнение регистрации"""
        username = self.reg_username.text().strip()
        email = self.reg_email.text().strip()
        password1 = self.reg_password1.text().strip()
        password2 = self.reg_password2.text().strip()
        
        # Проверка полей
        if not all([username, email, password1, password2]):
            self.show_error("Заполните все обязательные поля")
            return
        
        if password1 != password2:
            self.show_error("Пароли не совпадают")
            return
        
        if len(password1) < 8:
            self.show_error("Пароль должен содержать минимум 8 символов")
            return
        
        # Блокируем кнопку
        self.register_btn.setEnabled(False)
        self.register_btn.setText("Регистрация...")
        QApplication.processEvents()
        
        if self.api.register(username, email, password1, password2):
            self.show_success("Регистрация успешна! Теперь войдите.")
            self.tabs.setCurrentIndex(0)
            self.login_username.setText(username)
            self.login_password.setText(password1)
        else:
            self.show_error("Ошибка регистрации. Возможно, пользователь уже существует.")
        
        self.register_btn.setEnabled(True)
        self.register_btn.setText("Зарегистрироваться")
    
    def show_error(self, message: str):
        """Показать ошибку"""
        self.status_label.setText(f"❌ {message}")
        self.status_label.setStyleSheet("color: #d32f2f; font-weight: bold;")
    
    def show_success(self, message: str):
        """Показать успех"""
        self.status_label.setText(f"✅ {message}")
        self.status_label.setStyleSheet("color: #388e3c; font-weight: bold;")
    
    def accept_login(self):
        """Принять вход и закрыть диалог"""
        self.login_success.emit()
        self.accept()
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.reject()