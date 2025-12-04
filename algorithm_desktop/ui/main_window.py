from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import config
from .login_dialog import LoginDialog
from .algorithm_form import AlgorithmForm

class MainWindow(QMainWindow):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api = api_client
        self.current_user = None
        self.init_ui()
        self.load_current_user()
        
    def init_ui(self):
        self.setWindowTitle("Algorithm Manager")
        self.setGeometry(100, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Верхняя панель
        top_panel = QWidget()
        top_layout = QHBoxLayout(top_panel)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Логотип/название
        title_label = QLabel("📊 Algorithm Manager")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Информация о пользователе
        self.user_label = QLabel("Гость")
        self.user_label.setStyleSheet("color: #666;")
        
        # Поиск
        search_layout = QHBoxLayout()
        search_layout.setSpacing(5)
        
        search_label = QLabel("Поиск:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию, тегам, автору...")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(self.on_search_changed)
        
        self.search_btn = QPushButton("🔍")
        self.search_btn.setFixedSize(30, 30)
        self.search_btn.setToolTip("Поиск")
        self.search_btn.clicked.connect(self.search_algorithms)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        
        # Кнопки действий
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setFixedSize(30, 30)
        self.refresh_btn.setToolTip("Обновить")
        self.refresh_btn.clicked.connect(self.load_algorithms)
        
        self.create_btn = QPushButton("➕ Создать")
        self.create_btn.clicked.connect(self.create_algorithm)
        self.create_btn.setEnabled(False)  # По умолчанию выключена
        
        self.logout_btn = QPushButton("🚪 Выход")
        self.logout_btn.clicked.connect(self.logout)
        
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.create_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.logout_btn)
        
        # Собираем верхнюю панель
        top_layout.addWidget(title_label)
        top_layout.addWidget(self.user_label)
        top_layout.addStretch()
        top_layout.addLayout(search_layout)
        top_layout.addLayout(btn_layout)
        
        main_layout.addWidget(top_panel)
        
        # Вкладки
        self.tabs = QTabWidget()
        
        # Вкладка "Все алгоритмы"
        self.all_algorithms_tab = QWidget()
        self.init_all_algorithms_tab()
        
        # Вкладка "Мои алгоритмы"
        self.my_algorithms_tab = QWidget()
        self.init_my_algorithms_tab()
        
        # Вкладка "Модерация"
        self.moderation_tab = QWidget()
        self.init_moderation_tab()
        
        self.tabs.addTab(self.all_algorithms_tab, "Все алгоритмы")
        self.tabs.addTab(self.my_algorithms_tab, "Мои алгоритмы")
        self.tabs.addTab(self.moderation_tab, "Модерация")
        
        main_layout.addWidget(self.tabs)
        
        # Статус бар
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("Готово")
        self.status_bar.addWidget(self.status_label)
        
        # Таймер для автообновления
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_refresh)
        self.timer.start(60000)  # Каждую минуту
        
        # Стили
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                padding: 8px 16px;
                margin-right: 2px;
                background-color: #e0e0e0;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #f0f0f0;
            }
            QPushButton {
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)
        
    def init_all_algorithms_tab(self):
        """Инициализация вкладки всех алгоритмов"""
        layout = QVBoxLayout(self.all_algorithms_tab)
        
        # Таблица алгоритмов
        self.all_algorithms_table = QTableWidget()
        self.all_algorithms_table.setColumnCount(7)
        self.all_algorithms_table.setHorizontalHeaderLabels([
            "ID", "Название", "Автор", "Теги", "Статус", "Дата", "Действия"
        ])
        
        # Настройка таблицы
        self.all_algorithms_table.horizontalHeader().setStretchLastSection(True)
        self.all_algorithms_table.setAlternatingRowColors(True)
        self.all_algorithms_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.all_algorithms_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Настройка колонок
        self.all_algorithms_table.setColumnWidth(0, 50)   # ID
        self.all_algorithms_table.setColumnWidth(1, 200)  # Название
        self.all_algorithms_table.setColumnWidth(2, 120)  # Автор
        self.all_algorithms_table.setColumnWidth(3, 150)  # Теги
        self.all_algorithms_table.setColumnWidth(4, 100)  # Статус
        self.all_algorithms_table.setColumnWidth(5, 120)  # Дата
        
        layout.addWidget(self.all_algorithms_table)
        
    def init_my_algorithms_tab(self):
        """Инициализация вкладки моих алгоритмов"""
        layout = QVBoxLayout(self.my_algorithms_tab)
        
        # Таблица моих алгоритмов
        self.my_algorithms_table = QTableWidget()
        self.my_algorithms_table.setColumnCount(7)
        self.my_algorithms_table.setHorizontalHeaderLabels([
            "ID", "Название", "Статус", "Модератор", "Дата создания", "Дата обновления", "Действия"
        ])
        
        # Настройка таблицы
        self.my_algorithms_table.horizontalHeader().setStretchLastSection(True)
        self.my_algorithms_table.setAlternatingRowColors(True)
        self.my_algorithms_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.my_algorithms_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.my_algorithms_table)
        
    def init_moderation_tab(self):
        """Инициализация вкладки модерации"""
        layout = QVBoxLayout(self.moderation_tab)
        
        # Панель инструментов модерации
        mod_toolbar = QHBoxLayout()
        
        mod_label = QLabel("Алгоритмы на модерации:")
        mod_label.setStyleSheet("font-weight: bold;")
        
        self.mod_refresh_btn = QPushButton("🔄 Обновить")
        self.mod_refresh_btn.clicked.connect(self.load_moderation_list)
        
        mod_toolbar.addWidget(mod_label)
        mod_toolbar.addStretch()
        mod_toolbar.addWidget(self.mod_refresh_btn)
        
        layout.addLayout(mod_toolbar)
        
        # Таблица модерации
        self.moderation_table = QTableWidget()
        self.moderation_table.setColumnCount(8)
        self.moderation_table.setHorizontalHeaderLabels([
            "ID", "Название", "Автор", "Теги", "Дата создания", "Статус", "Действия", ""
        ])
        
        # Настройка таблицы
        self.moderation_table.horizontalHeader().setStretchLastSection(True)
        self.moderation_table.setAlternatingRowColors(True)
        self.moderation_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.moderation_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.moderation_table)
        
    def load_current_user(self):
        """Загрузка данных текущего пользователя"""
        self.current_user = self.api.get_current_user()
        
        if self.current_user and isinstance(self.current_user, dict):
            username = self.current_user.get('username', 'Гость')
            self.user_label.setText(f"👤 {username}")
            self.create_btn.setEnabled(True)
            
            # Проверяем права модератора
            if self.current_user.get('is_staff', False):
                self.tabs.setTabEnabled(2, True)
                self.load_moderation_list()
            else:
                self.tabs.setTabEnabled(2, False)
            
            # Загружаем алгоритмы
            self.load_algorithms()
            self.load_my_algorithms()
        else:
            self.user_label.setText("Гость")
            self.create_btn.setEnabled(False)
            self.tabs.setTabEnabled(2, False)
    
    def show_login_dialog(self):
        """Показать диалог входа"""
        dialog = LoginDialog(self.api, self)
        dialog.login_success.connect(self.on_login_success)
        
        if dialog.exec_() == QDialog.Accepted:
            self.load_current_user()
        else:
            QTimer.singleShot(100, self.close)
    
    def on_login_success(self):
        """Обработка успешного входа"""
        self.load_current_user()
    
    def load_algorithms(self):
        """Загрузка всех алгоритмов"""
        search_text = self.search_input.text().strip()
        algorithms = self.api.get_algorithms(search_text)
        self.update_all_algorithms_table(algorithms)
        self.status_label.setText(f"Загружено алгоритмов: {len(algorithms)}")
    
    def load_my_algorithms(self):
        """Загрузка моих алгоритмов"""
        if self.current_user:
            username = self.current_user.get('username')
            algorithms = self.api.get_user_algorithms(username)
            self.update_my_algorithms_table(algorithms)
    
    def load_moderation_list(self):
        """Загрузка списка на модерацию"""
        if self.current_user and self.current_user.get('is_staff'):
            algorithms = self.api.get_moderation_list()
            self.update_moderation_table(algorithms)
    
    def update_all_algorithms_table(self, algorithms):
        """Обновление таблицы всех алгоритмов"""
        # Проверяем, что algorithms - это список
        if not isinstance(algorithms, list):
            print(f"Ошибка: ожидался список, получен {type(algorithms)}")
            algorithms = []
        
        self.all_algorithms_table.setRowCount(len(algorithms))
        
        for row, algo in enumerate(algorithms):
            # Проверяем, что algo - это словарь
            if not isinstance(algo, dict):
                print(f"Пропускаем элемент {row}: не словарь")
                continue
                
            # ID
            self.all_algorithms_table.setItem(row, 0, QTableWidgetItem(str(algo.get('id', ''))))
            
            # Название
            name_item = QTableWidgetItem(algo.get('name', ''))
            name_item.setToolTip(algo.get('name', ''))
            self.all_algorithms_table.setItem(row, 1, name_item)
            
            # Автор
            self.all_algorithms_table.setItem(row, 2, QTableWidgetItem(algo.get('author_name', '')))
            
            # Теги
            tags_list = algo.get('tags_list', [])
            if isinstance(tags_list, list):
                tags = ", ".join(tags_list)
            else:
                tags = str(tags_list)
            tags_item = QTableWidgetItem(tags)
            tags_item.setToolTip(tags)
            self.all_algorithms_table.setItem(row, 3, tags_item)
            
            # Статус
            status = algo.get('status_display', '')
            if not status:
                status = algo.get('status', '')
            status_item = QTableWidgetItem(status)
            
            # Раскрашиваем статус
            status_val = algo.get('status', '')
            if status_val == 'approved':
                status_item.setBackground(QColor(config.COLOR_APPROVED))
            elif status_val == 'rejected':
                status_item.setBackground(QColor(config.COLOR_REJECTED))
            else:
                status_item.setBackground(QColor(config.COLOR_PENDING))
            
            self.all_algorithms_table.setItem(row, 4, status_item)
            
            # Дата создания
            created = algo.get('created_at', '')
            if created and len(created) >= 10:
                created = created[:10]  # Берем только дату
            self.all_algorithms_table.setItem(row, 5, QTableWidgetItem(created))
            
            # Действия
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(3)
            
            # Кнопка просмотра
            view_btn = QPushButton("👁")
            view_btn.setFixedSize(30, 25)
            view_btn.setToolTip("Просмотреть")
            view_btn.clicked.connect(lambda checked, a=algo: self.view_algorithm(a))
            actions_layout.addWidget(view_btn)
            
            # Если это мой алгоритм или я модератор - добавляем кнопки редактирования/удаления
            if self.current_user:
                can_edit = algo.get('can_edit', False)
                can_moderate = algo.get('can_moderate', False)
                
                if can_edit or can_moderate:
                    # Кнопка редактирования
                    edit_btn = QPushButton("✏️")
                    edit_btn.setFixedSize(30, 25)
                    edit_btn.setToolTip("Редактировать")
                    edit_btn.clicked.connect(lambda checked, a=algo: self.edit_algorithm(a))
                    actions_layout.addWidget(edit_btn)
                    
                    # Кнопка удаления
                    delete_btn = QPushButton("🗑")
                    delete_btn.setFixedSize(30, 25)
                    delete_btn.setToolTip("Удалить")
                    delete_btn.clicked.connect(lambda checked, a=algo: self.delete_algorithm(a))
                    actions_layout.addWidget(delete_btn)
            
            self.all_algorithms_table.setCellWidget(row, 6, actions_widget)
        self.all_algorithms_table.resizeRowsToContents()
    
    def update_my_algorithms_table(self, algorithms):
        """Обновление таблицы моих алгоритмов"""
        self.my_algorithms_table.setRowCount(len(algorithms))
        
        for row, algo in enumerate(algorithms):
            # ID
            self.my_algorithms_table.setItem(row, 0, QTableWidgetItem(str(algo.get('id', ''))))
            
            # Название
            name_item = QTableWidgetItem(algo.get('name', ''))
            self.my_algorithms_table.setItem(row, 1, name_item)
            
            # Статус
            status = algo.get('status_display', '')
            status_item = QTableWidgetItem(status)
            
            if algo.get('status') == 'approved':
                status_item.setBackground(QColor(config.COLOR_APPROVED))
            elif algo.get('status') == 'rejected':
                status_item.setBackground(QColor(config.COLOR_REJECTED))
            else:
                status_item.setBackground(QColor(config.COLOR_PENDING))
            
            self.my_algorithms_table.setItem(row, 2, status_item)
            
            # Модератор
            moderator = algo.get('moderated_by', {})
            moderator_name = moderator.get('username', '') if isinstance(moderator, dict) else str(moderator)
            self.my_algorithms_table.setItem(row, 3, QTableWidgetItem(moderator_name))
            
            # Дата создания
            created = algo.get('created_at', '')[:19]  # Берем дату и время
            self.my_algorithms_table.setItem(row, 4, QTableWidgetItem(created))
            
            # Дата обновления
            updated = algo.get('updated_at', '')[:19]
            self.my_algorithms_table.setItem(row, 5, QTableWidgetItem(updated))
            
            # Действия
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            view_btn = QPushButton("👁")
            view_btn.setFixedSize(30, 25)
            view_btn.clicked.connect(lambda checked, a=algo: self.view_algorithm(a))
            actions_layout.addWidget(view_btn)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 25)
            edit_btn.clicked.connect(lambda checked, a=algo: self.edit_algorithm(a))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("🗑")
            delete_btn.setFixedSize(30, 25)
            delete_btn.clicked.connect(lambda checked, a=algo: self.delete_algorithm(a))
            actions_layout.addWidget(delete_btn)
            
            self.my_algorithms_table.setCellWidget(row, 6, actions_widget)
        
        self.my_algorithms_table.resizeRowsToContents()
    
    def update_moderation_table(self, algorithms):
        """Обновление таблицы модерации"""
        self.moderation_table.setRowCount(len(algorithms))
        
        for row, algo in enumerate(algorithms):
            # ID
            self.moderation_table.setItem(row, 0, QTableWidgetItem(str(algo.get('id', ''))))
            
            # Название
            self.moderation_table.setItem(row, 1, QTableWidgetItem(algo.get('name', '')))
            
            # Автор
            self.moderation_table.setItem(row, 2, QTableWidgetItem(algo.get('author_name', '')))
            
            # Теги
            tags = ", ".join(algo.get('tags_list', []))
            self.moderation_table.setItem(row, 3, QTableWidgetItem(tags))
            
            # Дата создания
            created = algo.get('created_at', '')[:19]
            self.moderation_table.setItem(row, 4, QTableWidgetItem(created))
            
            # Статус
            status = algo.get('status_display', '')
            status_item = QTableWidgetItem(status)
            status_item.setBackground(QColor(config.COLOR_PENDING))
            self.moderation_table.setItem(row, 5, status_item)
            
            # Действия модерации
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            view_btn = QPushButton("👁")
            view_btn.setFixedSize(30, 25)
            view_btn.clicked.connect(lambda checked, a=algo: self.view_algorithm(a))
            actions_layout.addWidget(view_btn)
            
            approve_btn = QPushButton("✅")
            approve_btn.setFixedSize(30, 25)
            approve_btn.setToolTip("Одобрить")
            approve_btn.clicked.connect(lambda checked, a=algo: self.moderate_algorithm(a, 'approved'))
            actions_layout.addWidget(approve_btn)
            
            reject_btn = QPushButton("❌")
            reject_btn.setFixedSize(30, 25)
            reject_btn.setToolTip("Отклонить")
            reject_btn.clicked.connect(lambda checked, a=algo: self.show_reject_dialog(a))
            actions_layout.addWidget(reject_btn)
            
            self.moderation_table.setCellWidget(row, 6, actions_widget)
        
        self.moderation_table.resizeRowsToContents()
    
    def on_search_changed(self, text):
        """Обработка изменения текста поиска"""
        # Используем таймер для отложенного поиска
        if hasattr(self, 'search_timer'):
            self.search_timer.stop()
        
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.search_algorithms)
        self.search_timer.start(500)  # 500ms задержка
    
    def search_algorithms(self):
        """Выполнение поиска"""
        self.load_algorithms()
    
    def create_algorithm(self):
        """Создание нового алгоритма"""
        if not self.current_user:
            self.show_error("Сначала войдите в систему")
            return
        
        dialog = AlgorithmForm(self.api, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_algorithms()
            self.load_my_algorithms()
    
    def edit_algorithm(self, algorithm):
        """Редактирование алгоритма"""
        if not self.current_user:
            self.show_error("Сначала войдите в систему")
            return
        
        # Загружаем полные данные алгоритма
        full_algo = self.api.get_algorithm(algorithm.get('id'))
        if not full_algo:
            self.show_error("Не удалось загрузить данные алгоритма")
            return
        
        dialog = AlgorithmForm(self.api, algorithm=full_algo, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_algorithms()
            self.load_my_algorithms()
    
    def view_algorithm(self, algorithm):
        """Просмотр алгоритма"""
        # Загружаем полные данные
        full_algo = self.api.get_algorithm(algorithm.get('id'))
        if not full_algo:
            self.show_error("Не удалось загрузить данные алгоритма")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Просмотр: {full_algo.get('name')}")
        dialog.resize(900, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Создаем табы для разных разделов
        tabs = QTabWidget()
        
        # Вкладка "Общая информация"
        info_tab = QWidget()
        info_layout = QFormLayout(info_tab)
        info_layout.setLabelAlignment(Qt.AlignRight)
        
        # Основная информация
        info_layout.addRow("Название:", QLabel(full_algo.get('name', '')))
        info_layout.addRow("Автор:", QLabel(full_algo.get('author_name', '')))
        
        status_label = QLabel(full_algo.get('status_display', ''))
        if full_algo.get('status') == 'approved':
            status_label.setStyleSheet(f"color: #388e3c; font-weight: bold; background-color: {config.COLOR_APPROVED}; padding: 5px;")
        elif full_algo.get('status') == 'rejected':
            status_label.setStyleSheet(f"color: #d32f2f; font-weight: bold; background-color: {config.COLOR_REJECTED}; padding: 5px;")
        else:
            status_label.setStyleSheet(f"color: #f57c00; font-weight: bold; background-color: {config.COLOR_PENDING}; padding: 5px;")
        info_layout.addRow("Статус:", status_label)
        
        if full_algo.get('rejection_reason'):
            reason_text = QTextEdit(full_algo.get('rejection_reason'))
            reason_text.setReadOnly(True)
            reason_text.setMaximumHeight(80)
            info_layout.addRow("Причина отклонения:", reason_text)
        
        info_layout.addRow("Дата создания:", QLabel(full_algo.get('created_at', '')))
        info_layout.addRow("Дата обновления:", QLabel(full_algo.get('updated_at', '')))
        
        if full_algo.get('moderated_by'):
            moderator = full_algo.get('moderated_by', {})
            moderator_name = moderator.get('username', '') if isinstance(moderator, dict) else str(moderator)
            info_layout.addRow("Модератор:", QLabel(moderator_name))
            info_layout.addRow("Дата модерации:", QLabel(full_algo.get('moderated_at', '')))
        
        # Теги
        tags_label = QLabel(", ".join(full_algo.get('tags_list', [])))
        tags_label.setWordWrap(True)
        info_layout.addRow("Теги:", tags_label)
        
        tabs.addTab(info_tab, "Общая информация")
        
        # Вкладка "Описание"
        desc_tab = QWidget()
        desc_layout = QVBoxLayout(desc_tab)
        
        desc_text = QTextEdit(full_algo.get('description', ''))
        desc_text.setReadOnly(True)
        desc_layout.addWidget(desc_text)
        
        tabs.addTab(desc_tab, "Описание")
        
        # Вкладка "Код"
        code_tab = QWidget()
        code_layout = QVBoxLayout(code_tab)
        
        code_text = QTextEdit(full_algo.get('code', ''))
        code_text.setReadOnly(True)
        
        # Устанавливаем моноширинный шрифт для кода
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.Monospace)
        code_text.setFont(font)
        
        # Добавляем подсветку синтаксиса (простая версия)
        from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
        class PythonHighlighter(QSyntaxHighlighter):
            def __init__(self, parent):
                super().__init__(parent)
                self.highlighting_rules = []
                
                # Ключевые слова Python
                keyword_format = QTextCharFormat()
                keyword_format.setForeground(QColor("#0000FF"))
                keyword_format.setFontWeight(QFont.Bold)
                keywords = [
                    "def", "class", "return", "if", "elif", "else", "for", "while",
                    "try", "except", "import", "from", "as", "with", "pass", "break",
                    "continue", "True", "False", "None", "and", "or", "not", "in", "is"
                ]
                for word in keywords:
                    pattern = r'\b' + word + r'\b'
                    self.highlighting_rules.append((QRegExp(pattern), keyword_format))
                
                # Комментарии
                comment_format = QTextCharFormat()
                comment_format.setForeground(QColor("#008000"))
                self.highlighting_rules.append((QRegExp(r'#.*'), comment_format))
                
                # Строки
                string_format = QTextCharFormat()
                string_format.setForeground(QColor("#800000"))
                self.highlighting_rules.append((QRegExp(r'\".*\"'), string_format))
                self.highlighting_rules.append((QRegExp(r'\'.*\''), string_format))
        
        # Применяем подсветку
        highlighter = PythonHighlighter(code_text.document())
        
        code_layout.addWidget(code_text)
        tabs.addTab(code_tab, "Код")
        
        layout.addWidget(tabs)
        
        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.exec_()
    
    def delete_algorithm(self, algorithm):
        """Удаление алгоритма"""
        if not self.current_user:
            self.show_error("Сначала войдите в систему")
            return
        
        reply = QMessageBox.question(
            self, 'Подтверждение удаления',
            f'Вы уверены, что хотите удалить алгоритм "{algorithm.get("name")}"?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.api.delete_algorithm(algorithm.get('id')):
                self.show_success("Алгоритм успешно удален")
                self.load_algorithms()
                self.load_my_algorithms()
            else:
                self.show_error("Не удалось удалить алгоритм")
    
    def moderate_algorithm(self, algorithm, status):
        """Модерация алгоритма"""
        if not self.current_user or not self.current_user.get('is_staff'):
            self.show_error("У вас нет прав модератора")
            return
        
        if status == 'approved':
            reply = QMessageBox.question(
                self, 'Подтверждение',
                f'Одобрить алгоритм "{algorithm.get("name")}"?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.api.moderate_algorithm(algorithm.get('id'), 'approved'):
                    self.show_success("Алгоритм одобрен")
                    self.load_moderation_list()
                    self.load_algorithms()
                    self.load_my_algorithms()
                else:
                    self.show_error("Не удалось одобрить алгоритм")
    
    def show_reject_dialog(self, algorithm):
        """Диалог отклонения алгоритма"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Отклонение алгоритма")
        dialog.setFixedSize(500, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Информация об алгоритме
        info_label = QLabel(f"Алгоритм: <b>{algorithm.get('name')}</b><br>Автор: {algorithm.get('author_name')}")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addWidget(QLabel("Причина отклонения*:"))
        
        self.reject_reason_input = QTextEdit()
        self.reject_reason_input.setPlaceholderText("Укажите причину отклонения алгоритма...")
        self.reject_reason_input.setMaximumHeight(150)
        layout.addWidget(self.reject_reason_input)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(dialog.reject)
        
        reject_btn = QPushButton("Отклонить")
        reject_btn.clicked.connect(lambda: self.process_rejection(dialog, algorithm))
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(reject_btn)
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def process_rejection(self, dialog, algorithm):
        """Обработка отклонения"""
        reason = self.reject_reason_input.toPlainText().strip()
        
        if not reason:
            self.show_error("Укажите причину отклонения")
            return
        
        if self.api.moderate_algorithm(algorithm.get('id'), 'rejected', reason):
            self.show_success("Алгоритм отклонен")
            dialog.accept()
            self.load_moderation_list()
            self.load_algorithms()
            self.load_my_algorithms()
        else:
            self.show_error("Не удалось отклонить алгоритм")
    
    def logout(self):
        """Выход из системы"""
        self.api.clear_token()
        self.current_user = None
        self.user_label.setText("Гость")
        self.create_btn.setEnabled(False)
        self.tabs.setTabEnabled(2, False)
        
        # Очищаем таблицы
        self.all_algorithms_table.setRowCount(0)
        self.my_algorithms_table.setRowCount(0)
        self.moderation_table.setRowCount(0)
        
        # Показываем диалог входа
        self.show_login_dialog()
    
    def auto_refresh(self):
        """Автообновление данных"""
        if self.current_user:
            current_tab = self.tabs.currentIndex()
            if current_tab == 0:  # Все алгоритмы
                self.load_algorithms()
            elif current_tab == 1:  # Мои алгоритмы
                self.load_my_algorithms()
            elif current_tab == 2:  # Модерация
                self.load_moderation_list()
    
    def show_error(self, message: str):
        """Показать сообщение об ошибке"""
        QMessageBox.critical(self, "Ошибка", message)
    
    def show_success(self, message: str):
        """Показать сообщение об успехе"""
        QMessageBox.information(self, "Успех", message)
    
    def closeEvent(self, event):
        """Обработка закрытия окна"""
        self.timer.stop()
        event.accept()