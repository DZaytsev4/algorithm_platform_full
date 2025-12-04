from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import config

class AlgorithmForm(QDialog):
    def __init__(self, api_client, algorithm=None, parent=None):
        super().__init__(parent)
        self.api = api_client
        self.algorithm = algorithm
        self.is_edit_mode = algorithm is not None
        self.init_ui()
        
    def init_ui(self):
        if self.is_edit_mode:
            self.setWindowTitle(f"Редактирование: {self.algorithm.get('name', '')}")
        else:
            self.setWindowTitle("Создание алгоритма")
            
        self.resize(800, 600)
        
        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        # Создаем скроллируемую область для формы
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Контейнер для формы
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)
        
        # Поле названия
        name_group = QGroupBox("Основная информация")
        name_layout = QFormLayout(name_group)
        
        self.name_input = QLineEdit()
        if self.algorithm:
            self.name_input.setText(self.algorithm.get('name', ''))
        self.name_input.setPlaceholderText("Введите название алгоритма")
        
        self.tags_input = QLineEdit()
        if self.algorithm:
            self.tags_input.setText(self.algorithm.get('tegs', ''))
        self.tags_input.setPlaceholderText("тег1, тег2, тег3 (через запятую)")
        
        name_layout.addRow("Название*:", self.name_input)
        name_layout.addRow("Теги:", self.tags_input)
        
        form_layout.addWidget(name_group)
        
        # Поле описания
        desc_group = QGroupBox("Описание алгоритма")
        desc_layout = QVBoxLayout(desc_group)
        
        self.desc_input = QTextEdit()
        if self.algorithm:
            self.desc_input.setText(self.algorithm.get('description', ''))
        self.desc_input.setPlaceholderText("Опишите алгоритм, его назначение и особенности...")
        self.desc_input.setMaximumHeight(150)
        
        desc_layout.addWidget(self.desc_input)
        form_layout.addWidget(desc_group)
        
        # Поле кода
        code_group = QGroupBox("Код алгоритма")
        code_layout = QVBoxLayout(code_group)
        
        # Панель инструментов для кода
        code_toolbar = QHBoxLayout()
        
        lang_label = QLabel("Язык программирования:")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Python", "JavaScript", "Java", "C++", "C#", "Other"])
        code_toolbar.addWidget(lang_label)
        code_toolbar.addWidget(self.lang_combo)
        code_toolbar.addStretch()
        
        code_layout.addLayout(code_toolbar)
        
        # Редактор кода
        self.code_input = QTextEdit()
        if self.algorithm:
            self.code_input.setText(self.algorithm.get('code', ''))
        else:
            self.code_input.setPlaceholderText("# Введите код алгоритма здесь\n# Например:\ndef sort_array(arr):\n    return sorted(arr)")
        
        # Устанавливаем моноширинный шрифт для кода
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.Monospace)
        self.code_input.setFont(font)
        self.code_input.setMaximumHeight(250)
        
        code_layout.addWidget(self.code_input)
        form_layout.addWidget(code_group)
        
        # Статус (только для редактирования)
        if self.is_edit_mode:
            status_group = QGroupBox("Статус алгоритма")
            status_layout = QFormLayout(status_group)
            
            status_label = QLabel(self.algorithm.get('status_display', ''))
            if self.algorithm.get('status') == 'approved':
                status_label.setStyleSheet(f"color: #388e3c; font-weight: bold; background-color: {config.COLOR_APPROVED}; padding: 5px;")
            elif self.algorithm.get('status') == 'rejected':
                status_label.setStyleSheet(f"color: #d32f2f; font-weight: bold; background-color: {config.COLOR_REJECTED}; padding: 5px;")
            else:
                status_label.setStyleSheet(f"color: #f57c00; font-weight: bold; background-color: {config.COLOR_PENDING}; padding: 5px;")
            
            status_layout.addRow("Текущий статус:", status_label)
            
            if self.algorithm.get('rejection_reason'):
                reason_label = QLabel(self.algorithm.get('rejection_reason', ''))
                reason_label.setWordWrap(True)
                reason_label.setStyleSheet("color: #666; font-style: italic; background-color: #fff3cd; padding: 5px;")
                status_layout.addRow("Причина отклонения:", reason_label)
            
            form_layout.addWidget(status_group)
        
        # Информация о модерации (если есть)
        if self.is_edit_mode and self.algorithm.get('moderated_by'):
            mod_group = QGroupBox("Информация о модерации")
            mod_layout = QFormLayout(mod_group)
            
            moderator = self.algorithm.get('moderated_by', {})
            moderator_name = moderator.get('username', 'Неизвестно') if isinstance(moderator, dict) else str(moderator)
            
            mod_layout.addRow("Модератор:", QLabel(moderator_name))
            mod_layout.addRow("Дата модерации:", QLabel(self.algorithm.get('moderated_at', 'Не указана')))
            
            form_layout.addWidget(mod_group)
        
        # Подсказка
        hint_label = QLabel("<i>* Обязательные поля</i>")
        hint_label.setStyleSheet("color: #666;")
        form_layout.addWidget(hint_label)
        
        # Устанавливаем контейнер в скроллируемую область
        scroll_area.setWidget(form_container)
        main_layout.addWidget(scroll_area)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        self.preview_btn = QPushButton("👁 Предпросмотр")
        self.preview_btn.clicked.connect(self.show_preview)
        self.preview_btn.setToolTip("Предварительный просмотр алгоритма")
        
        button_layout.addWidget(self.preview_btn)
        button_layout.addStretch()
        
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("💾 Сохранить")
        self.save_btn.clicked.connect(self.save_algorithm)
        self.save_btn.setDefault(True)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(button_layout)
        
        # Статус сохранения
        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        main_layout.addWidget(self.status_label)
        
        # Стилизация
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
        """)
    
    def get_form_data(self) -> dict:
        """Получение данных из формы"""
        return {
            'name': self.name_input.text().strip(),
            'tegs': self.tags_input.text().strip(),
            'description': self.desc_input.toPlainText().strip(),
            'code': self.code_input.toPlainText().strip()
        }
    
    def validate_form(self) -> tuple[bool, str]:
        """Валидация формы"""
        data = self.get_form_data()
        
        if not data['name']:
            return False, "Название алгоритма обязательно для заполнения"
        
        if not data['description']:
            return False, "Описание алгоритма обязательно для заполнения"
        
        if not data['code']:
            return False, "Код алгоритма обязателен для заполнения"
        
        if len(data['name']) > 200:
            return False, "Название не должно превышать 200 символов"
        
        if len(data['description']) > 5000:
            return False, "Описание не должно превышать 5000 символов"
        
        if len(data['code']) > 10000:
            return False, "Код не должен превышать 10000 символов"
        
        return True, ""
    
    def save_algorithm(self):
        """Сохранение алгоритма"""
        is_valid, error_message = self.validate_form()
        if not is_valid:
            self.show_error(error_message)
            return
        
        data = self.get_form_data()
        
        # Блокируем кнопки на время сохранения
        self.save_btn.setEnabled(False)
        self.save_btn.setText("Сохранение...")
        QApplication.processEvents()
        
        try:
            if self.is_edit_mode:
                success = self.api.update_algorithm(self.algorithm['id'], data)
                message = "обновлен"
            else:
                result = self.api.create_algorithm(data)
                success = result is not None
                message = "создан"
            
            if success:
                self.show_success(f"Алгоритм успешно {message}!")
                QTimer.singleShot(500, self.accept)
            else:
                self.show_error("Не удалось сохранить алгоритм. Проверьте подключение.")
                self.save_btn.setEnabled(True)
                self.save_btn.setText("💾 Сохранить")
                
        except Exception as e:
            self.show_error(f"Ошибка при сохранении: {str(e)}")
            self.save_btn.setEnabled(True)
            self.save_btn.setText("💾 Сохранить")
    
    def show_preview(self):
        """Показать предпросмотр"""
        data = self.get_form_data()
        
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("Предпросмотр алгоритма")
        preview_dialog.resize(700, 500)
        
        layout = QVBoxLayout(preview_dialog)
        
        # Поля предпросмотра
        preview_fields = [
            ("Название:", data['name'] or "<не указано>"),
            ("Теги:", data['tegs'] or "<не указаны>"),
            ("Описание:", data['description'] or "<не указано>"),
            ("Код:", data['code'] or "<не указан>")
        ]
        
        for label, value in preview_fields:
            group = QGroupBox(label)
            group_layout = QVBoxLayout(group)
            
            text_edit = QTextEdit(value)
            text_edit.setReadOnly(True)
            
            if label == "Код:":
                font = QFont("Consolas", 10)
                font.setStyleHint(QFont.Monospace)
                text_edit.setFont(font)
                text_edit.setMaximumHeight(200)
            elif label == "Описание:":
                text_edit.setMaximumHeight(100)
            else:
                text_edit.setMaximumHeight(50)
            
            group_layout.addWidget(text_edit)
            layout.addWidget(group)
        
        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(preview_dialog.accept)
        layout.addWidget(close_btn)
        
        preview_dialog.exec_()
    
    def show_error(self, message: str):
        """Показать ошибку"""
        self.status_label.setText(f"❌ {message}")
        self.status_label.setStyleSheet("color: #d32f2f; font-weight: bold;")
    
    def show_success(self, message: str):
        """Показать успех"""
        self.status_label.setText(f"✅ {message}")
        self.status_label.setStyleSheet("color: #388e3c; font-weight: bold;")