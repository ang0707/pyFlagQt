import requests
import random
import sys
import sqlite3

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGridLayout, QPushButton, QDialog, QLineEdit, QDialogButtonBox, 
    QHeaderView, QTableWidget, QTableWidgetItem
)
from PyQt6.QtGui import QPixmap, QPainter


def get_quiz():
    """
    Генерирует список вопросов для викторины со странами и флагами.
    
    Returns:
        list: Список вопросов, каждый из которых содержит:
              - список из 4 вариантов ответов
              - правильный ответ
              - URL изображения флага
    """
    quiz = []

    # Данные о странах: название и код для получения флага
    COUNTRIES_DATA = [
        {"name": "Россия", "code": "ru"},
        {"name": "США", "code": "us"},
        {"name": "Китай", "code": "cn"},
        {"name": "Индия", "code": "in"},
        {"name": "Бразилия", "code": "br"},
        {"name": "Германия", "code": "de"},
        {"name": "Франция", "code": "fr"},
        {"name": "Великобритания", "code": "gb"},
        {"name": "Италия", "code": "it"},
        {"name": "Испания", "code": "es"},
        {"name": "Канада", "code": "ca"},
        {"name": "Австралия", "code": "au"},
        {"name": "Мексика", "code": "mx"},
        {"name": "Япония", "code": "jp"},
        {"name": "Южная Корея", "code": "kr"},
        {"name": "Украина", "code": "ua"},
        {"name": "Польша", "code": "pl"},
        {"name": "Турция", "code": "tr"},
        {"name": "Египет", "code": "eg"},
        {"name": "Аргентина", "code": "ar"},
        {"name": "Нигерия", "code": "ng"},
        {"name": "ЮАР", "code": "za"},
        {"name": "Пакистан", "code": "pk"},
        {"name": "Индонезия", "code": "id"},
        {"name": "Филиппины", "code": "ph"},
        {"name": "Вьетнам", "code": "vn"},
        {"name": "Таиланд", "code": "th"},
        {"name": "Малайзия", "code": "my"},
        {"name": "Сингапур", "code": "sg"},
        {"name": "Саудовская Аравия", "code": "sa"},
        {"name": "ОАЭ", "code": "ae"},
        {"name": "Израиль", "code": "il"},
        {"name": "Иран", "code": "ir"},
        {"name": "Ирак", "code": "iq"},
        {"name": "Афганистан", "code": "af"},
        {"name": "Казахстан", "code": "kz"},
        {"name": "Узбекистан", "code": "uz"},
        {"name": "Беларусь", "code": "by"},
        {"name": "Нидерланды", "code": "nl"},
        {"name": "Бельгия", "code": "be"},
        {"name": "Швеция", "code": "se"},
        {"name": "Норвегия", "code": "no"},
        {"name": "Финляндия", "code": "fi"},
        {"name": "Дания", "code": "dk"},
        {"name": "Португалия", "code": "pt"},
        {"name": "Греция", "code": "gr"},
        {"name": "Чехия", "code": "cz"},
        {"name": "Венгрия", "code": "hu"},
        {"name": "Румыния", "code": "ro"},
        {"name": "Болгария", "code": "bg"},
        {"name": "Сербия", "code": "rs"},
        {"name": "Хорватия", "code": "hr"},
        {"name": "Словакия", "code": "sk"},
        {"name": "Австрия", "code": "at"},
        {"name": "Швейцария", "code": "ch"},
        {"name": "Ирландия", "code": "ie"},
        {"name": "Новая Зеландия", "code": "nz"},
        {"name": "Чили", "code": "cl"},
        {"name": "Колумбия", "code": "co"},
        {"name": "Перу", "code": "pe"},
        {"name": "Венесуэла", "code": "ve"},
        {"name": "Куба", "code": "cu"},
        {"name": "Доминиканская Республика", "code": "do"},
        {"name": "Эквадор", "code": "ec"},
        {"name": "Боливия", "code": "bo"},
        {"name": "Парагвай", "code": "py"},
        {"name": "Уругвай", "code": "uy"},
        {"name": "Коста-Рика", "code": "cr"},
        {"name": "Панама", "code": "pa"},
        {"name": "Ямайка", "code": "jm"},
        {"name": "Гватемала", "code": "gt"},
        {"name": "Марокко", "code": "ma"},
        {"name": "Алжир", "code": "dz"},
        {"name": "Тунис", "code": "tn"},
        {"name": "Ливия", "code": "ly"},
        {"name": "Эфиопия", "code": "et"},
        {"name": "Кения", "code": "ke"},
        {"name": "Танзания", "code": "tz"},
        {"name": "Гана", "code": "gh"},
        {"name": "Ангола", "code": "ao"},
        {"name": "Мозамбик", "code": "mz"},
        {"name": "Мадагаскар", "code": "mg"},
        {"name": "Камерун", "code": "cm"},
        {"name": "Кот-д'Ивуар", "code": "ci"},
        {"name": "Сенегал", "code": "sn"},
        {"name": "Мали", "code": "ml"},
        {"name": "Буркина-Фасо", "code": "bf"},
        {"name": "Непал", "code": "np"},
        {"name": "Шри-Ланка", "code": "lk"},
        {"name": "Бангладеш", "code": "bd"},
        {"name": "Мьянма", "code": "mm"},
        {"name": "Камбоджа", "code": "kh"},
        {"name": "Лаос", "code": "la"},
        {"name": "Монголия", "code": "mn"},
        {"name": "Азербайджан", "code": "az"},
        {"name": "Грузия", "code": "ge"},
        {"name": "Армения", "code": "am"},
        {"name": "Литва", "code": "lt"},
        {"name": "Латвия", "code": "lv"},
        {"name": "Эстония", "code": "ee"},
        {"name": "Словения", "code": "si"},
        {"name": "Македония", "code": "mk"},
        {"name": "Албания", "code": "al"},
        {"name": "Черногория", "code": "me"},
        {"name": "Босния и Герцеговина", "code": "ba"}
    ]

    # Перемешиваем страны для случайного порядка вопросов
    random.shuffle(COUNTRIES_DATA)

    names = [country["name"] for country in COUNTRIES_DATA]
    codes = [country["code"] for country in COUNTRIES_DATA]

    def get_flag_url(country_code):
        """Генерирует URL для загрузки флага страны."""
        return f"https://flagcdn.com/w320/{country_code}.png"

    # Создаем вопросы для викторины
    for name, code in zip(names, codes):
        # Создаем список вариантов ответов (правильный + 3 случайных)
        answer_options = [name]
        while len(answer_options) < 4:
            random_country = random.choice(names)
            if random_country not in answer_options:
                answer_options.append(random_country)
        
        # Перемешиваем варианты ответов
        random.shuffle(answer_options)
        
        # Получаем URL флага
        flag_url = get_flag_url(code)
        
        # Добавляем вопрос в викторину
        quiz.append([answer_options, name, flag_url])

    return quiz


class AnimatedImageLabel(QLabel):
    """
    Виджет анимированного изображения, которое плавно увеличивается и уменьшается.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scale_factor = 1.0

        # Загружаем изображение или создаем тестовое при ошибке
        try:
            self._original_pixmap = QPixmap("Zambia-scaled.png")
            if self._original_pixmap.isNull():
                self.create_test_image()
        except Exception:
            self.create_test_image()

        self.setFixedSize(400, 200)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_pixmap()

        # Настройка анимации увеличения
        self.animation_forward = QPropertyAnimation(self, b"scale_factor")
        self.animation_forward.setDuration(1000)
        self.animation_forward.setStartValue(1.0)
        self.animation_forward.setEndValue(1.05)
        self.animation_forward.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # Настройка анимации уменьшения
        self.animation_backward = QPropertyAnimation(self, b"scale_factor")
        self.animation_backward.setDuration(1000)
        self.animation_backward.setStartValue(1.05)
        self.animation_backward.setEndValue(1.0)
        self.animation_backward.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Связываем анимации для непрерывного цикла
        self.animation_forward.finished.connect(self.animation_backward.start)
        self.animation_backward.finished.connect(self.animation_forward.start)
        
    def create_test_image(self):
        """Создает тестовое изображение если основное не загружено."""
        self._original_pixmap = QPixmap(400, 250)
        self._original_pixmap.fill(Qt.GlobalColor.darkCyan)
    
    def update_pixmap(self):
        """Обновляет изображение с учетом текущего масштаба."""
        if self._original_pixmap:
            new_width = int(400 * self._scale_factor)
            new_height = 250
            
            # Масштабируем исходное изображение
            scaled_pixmap = self._original_pixmap.scaled(
                new_width,
                new_height,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            # Создаем прозрачный pixmap для центрирования
            final_pixmap = QPixmap(new_width, new_height)
            final_pixmap.fill(Qt.GlobalColor.transparent)

            # Отрисовываем масштабированное изображение по центру
            painter = QPainter(final_pixmap)
            x_offset = (new_width - scaled_pixmap.width()) // 2
            y_offset = (new_height - scaled_pixmap.height()) // 2
            painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
            painter.end()
            
            self.setPixmap(final_pixmap)
    
    def get_scale_factor(self):
        """Возвращает текущий коэффициент масштабирования."""
        return self._scale_factor
    
    def set_scale_factor(self, factor):
        """Устанавливает коэффициент масштабирования и обновляет изображение."""
        self._scale_factor = factor
        self.update_pixmap()
    
    # Свойство для анимации
    scale_factor = pyqtProperty(float, get_scale_factor, set_scale_factor)
    
    def start_animation(self):
        """Запускает анимацию."""
        self.animation_forward.start()


class MyWidget(QWidget):
    """
    Главный виджет приложения, содержащий всю логику викторины.
    """
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Инициализирует пользовательский интерфейс."""
        # Инициализация переменных игры
        self.right_answers = 0
        self.wrong_answers = 0
        self.total_questions = 0
        self.score = 100.0

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("PyFlagQT")
        self.setFixedSize(650, 500)

        # Заголовок приложения
        self.title = QLabel("PyFlagQT")
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.title)

        # Виджет для отображения точности ответов
        self.score_label = QLabel("Правильность: 100%")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.score_label.hide()
        layout.addWidget(self.score_label)

        # Кнопка начала игры
        self.play_button = QPushButton("ИГРАТЬ")
        self.play_button.clicked.connect(self.start_game)
        layout.addWidget(self.play_button)
        
        # Кнопка таблицы лидеров
        self.leaderboard_button = QPushButton("ТАБЛИЦА ЛИДЕРОВ")
        self.leaderboard_button.clicked.connect(self.show_leaderboard)
        layout.addWidget(self.leaderboard_button)

        # Виджет для отображения флагов
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.image_label.hide()
        layout.addWidget(self.image_label)

        # Сетка для кнопок ответов
        answers_layout = QGridLayout()
        answers_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.answer1 = QPushButton()
        self.answer2 = QPushButton()
        self.answer3 = QPushButton()
        self.answer4 = QPushButton()

        # Скрываем кнопки ответов до начала игры
        self.answer1.hide()
        self.answer2.hide()
        self.answer3.hide()
        self.answer4.hide()

        # Добавляем кнопки в сетку
        answers_layout.addWidget(self.answer1, 0, 0)
        answers_layout.addWidget(self.answer2, 0, 1)
        answers_layout.addWidget(self.answer3, 1, 0)
        answers_layout.addWidget(self.answer4, 1, 1)

        layout.addLayout(answers_layout)

        # Анимированное изображение
        self.animated_image = AnimatedImageLabel()
        layout.addWidget(self.animated_image, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.animated_image.start_animation()

        # Применяем темную тему
        self.setStyleSheet(self.create_dark_theme())
    
    def calculate_score(self):
        """
        Вычисляет текущую точность ответов в процентах.
        
        Returns:
            float: Точность ответов в процентах
        """
        if self.total_questions == 0:
            return 100.0

        accuracy = (self.right_answers / self.total_questions) * 100
        return round(accuracy, 1)

    def update_score_display(self):
        """Обновляет отображение точности ответов."""
        self.score = self.calculate_score()
        self.score_label.setText(f"Правильность: {self.score}%")

    def load_image_from_url(self, url):
        """
        Загружает изображение по URL и отображает его.
        
        Args:
            url (str): URL изображения для загрузки
        """
        try:
            response = requests.get(url)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            # Масштабируем изображение
            scaled_pixmap = pixmap.scaled(
                400, 300, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )

            self.image_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.image_label.setText(f"Ошибка загрузки: {str(e)}")

    def create_dark_theme(self):
        """
        Создает CSS стили для темной темы приложения.
        
        Returns:
            str: CSS стили
        """
        return """
        QMainWindow {
            background-color: #293133; 
        }
        
        QWidget {
            background: #293133;
        }

        QLabel {
            font-size: 30px;
            font-weight: bold;
            font-family: "Comic Sans MS";
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #585b70, stop:1 #45475a);
            border: 1px solid #585b70;
            border-radius: 8px;
            padding: 8px 16px;
            color: #cdd6f4;
            font-size: 24px;
            font-family: "Comic Sans MS";
            font-weight: bold;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #74c7ec, stop:1 #89b4fa);
            border: 1px solid #74c7ec;
            color: #1e1e2e;
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #cba6f7, stop:1 #f5c2e7);
        }
        
        QLineEdit, QTextEdit {
            background: rgba(30, 30, 46, 0.8);
            border: 2px solid #45475a;
            border-radius: 6px;
            padding: 6px;
            color: #cdd6f4;
            selection-background-color: #cba6f7;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #74c7ec;
            background: rgba(30, 30, 46, 0.9);
        }
        
        QProgressBar {
            border: 2px solid #45475a;
            border-radius: 5px;
            text-align: center;
            color: #cdd6f4;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                    stop:0 #f38ba8, stop:0.5 #cba6f7, stop:1 #89b4fa);
            border-radius: 3px;
        }
        """
    
    def start_game(self):
        """Начинает новую игру, сбрасывая статистику и показывая игровые элементы."""
        # Сброс статистики
        self.right_answers = 0
        self.wrong_answers = 0
        self.total_questions = 0
        self.score = 100.0
        
        # Стиль кнопок по умолчанию
        self.original_button_style = '''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #585b70, stop:1 #45475a);
                border: 1px solid #585b70;
                border-radius: 8px;
                padding: 8px 16px;
                color: #cdd6f4;
                font-size: 24px;
                font-family: "Comic Sans MS";
                font-weight: bold;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #74c7ec, stop:1 #89b4fa);
                border: 1px solid #74c7ec;
                color: #1e1e2e;
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #cba6f7, stop:1 #f5c2e7);
            }
        '''
        
        # Показываем игровые элементы, скрываем меню
        self.play_button.hide()
        self.leaderboard_button.hide()
        self.animated_image.hide()

        self.image_label.show()
        self.score_label.show()
        
        self.answer1.show()
        self.answer2.show()
        self.answer3.show()
        self.answer4.show()

        # Загружаем вопросы и начинаем с первого
        self.quiz_data = list(get_quiz())
        self.current_question = 0
        self.setup_question()

    def setup_question(self):
        """Настраивает отображение текущего вопроса."""
        if self.current_question >= len(self.quiz_data):
            self.end_game()
            return
        
        # Получаем данные текущего вопроса
        answers, correct_answer, image_url = self.quiz_data[self.current_question]
        buttons = [self.answer1, self.answer2, self.answer3, self.answer4]

        # Загружаем изображение флага
        self.load_image_from_url(image_url)

        # Сбрасываем стиль и состояние кнопок
        for button in buttons:
            button.setStyleSheet(self.original_button_style)
            # Отключаем предыдущие соединения
            try:
                button.clicked.disconnect()
            except TypeError:
                pass  # Если соединений не было
            button.setEnabled(True)

        # Назначаем текст и обработчики для кнопок
        for answer, button in zip(answers, buttons):
            button.setText(answer)
            button.clicked.connect(
                lambda checked, btn=button, correct=correct_answer: 
                self.check_answer(btn, correct)
            )

    def check_answer(self, button, correct_answer):
        """
        Проверяет выбранный ответ и обновляет статистику.
        
        Args:
            button: Нажатая кнопка ответа
            correct_answer (str): Правильный ответ
        """
        self.total_questions += 1
        
        if button.text() == correct_answer:
            # Правильный ответ
            self.right_answers += 1
            button.setStyleSheet("background-color: green; color: white;")
            
            # Блокируем кнопки после ответа
            for btn in [self.answer1, self.answer2, self.answer3, self.answer4]:
                btn.setEnabled(False)
            
            # Показываем диалог продолжения каждые 10 правильных ответов
            if self.right_answers % 10 == 0:
                QTimer.singleShot(1000, self.show_continue_dialog)
            else:
                QTimer.singleShot(1000, self.next_question)
        else:
            # Неправильный ответ
            self.wrong_answers += 1
            button.setStyleSheet("background-color: red; color: white;")
            # Возвращаем обычный стиль через секунду
            QTimer.singleShot(1000, lambda: button.setStyleSheet(self.original_button_style))
        
        # Обновляем отображение статистики
        self.update_score_display()

    def show_continue_dialog(self):
        """
        Показывает диалоговое окно с предложением продолжить или сохранить результат.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Продолжить игру?")
        dialog.setFixedSize(500, 500)
        dialog.setModal(True)
        
        layout = QVBoxLayout()

        # Статистика игры
        stats_label = QLabel(
            f"Ваша текущая статистика:\n"
            f"Правильных ответов: {self.right_answers}\n"
            f"Неправильных ответов: {self.wrong_answers}\n"
            f"Правильность: {self.score}%"
        )
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(stats_label)
        
        question_label = QLabel(
            "Хотите выйти из игры и сохранить результаты или продолжить игру?"
        )
        question_label.setWordWrap(True)
        question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(question_label)
        
        # Кнопки выбора
        button_layout = QHBoxLayout()
        
        continue_btn = QPushButton("Продолжить")
        continue_btn.clicked.connect(lambda: self.on_continue_clicked(dialog))
        
        exit_btn = QPushButton("Выйти и сохранить")
        exit_btn.clicked.connect(lambda: self.exit_and_save(dialog))
        
        button_layout.addWidget(continue_btn)
        button_layout.addWidget(exit_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)

        dialog.exec()

    def on_continue_clicked(self, dialog):
        """
        Обрабатывает нажатие кнопки продолжения игры.
        
        Args:
            dialog: Диалоговое окно
        """
        dialog.accept()
        self.next_question()

    def exit_and_save(self, dialog):
        """
        Обрабатывает выход из игры с сохранением результатов.
        
        Args:
            dialog: Диалоговое окно
        """
        dialog.accept()
        self.end_game()

    def next_question(self):
        """Переходит к следующему вопросу."""
        self.current_question += 1
        self.setup_question()

    def end_game(self):
        """Завершает игру и показывает диалог с результатами."""
        self.show_score_dialog()
        
        # Скрываем игровые элементы, показываем меню
        for btn in [self.answer1, self.answer2, self.answer3, self.answer4]:
            btn.hide()
        
        self.image_label.hide()
        self.score_label.hide()
        
        self.play_button.show()
        self.leaderboard_button.show()
        self.animated_image.show()

    def show_score_dialog(self):
        """Показывает диалоговое окно с результатами игры и запросом имени."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Результат игры")
        dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout()

        score_label = QLabel(f"Ваш счет: {self.score}")
        score_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        layout.addWidget(score_label)

        name_label = QLabel("Введите ваше имя:")
        layout.addWidget(name_label)
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Ваше имя")
        layout.addWidget(name_input)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(lambda: self.save_score(name_input.text(), dialog))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec()

    def save_score(self, name, dialog):
        """
        Сохраняет результат игры в базу данных.
        
        Args:
            name (str): Имя игрока
            dialog: Диалоговое окно
        """
        if not name.strip():
            name = "Аноним"

        dialog.accept()

        # Сохранение в базу данных
        connection = sqlite3.connect("leaderboard.sqlite")
        cursor = connection.cursor()

        # Создаем таблицу если не существует
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                score FLOAT
            )
        """)

        # Вставляем результат
        cursor.execute("INSERT INTO users (name, score) VALUES (?, ?)", (name, self.score))

        connection.commit()
        connection.close()

    def show_leaderboard(self):
        """Показывает таблицу лидеров с лучшими результатами."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Таблица лидеров")
        dialog.setFixedSize(400, 500)
        dialog.setModal(True)
        
        layout = QVBoxLayout()

        title = QLabel("Лучшие игроки")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2E7D32;
            margin: 15px;
        """)
        layout.addWidget(title)

        # Загружаем данные лидерборда
        leaderboard_data = self.load_leaderboard()[:10]  # Берем первые 10
        
        # Создаем таблицу
        table = QTableWidget(len(leaderboard_data), 3)
        table.setHorizontalHeaderLabels(["Место", "Имя", "Очки"])

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        # Заполняем таблицу данными
        for row, (name, score) in enumerate(leaderboard_data):
            place_item = QTableWidgetItem(f"{row + 1}")
            place_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            name_item = QTableWidgetItem(name)

            score_item = QTableWidgetItem(str(score))
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            table.setItem(row, 0, place_item)
            table.setItem(row, 1, name_item)
            table.setItem(row, 2, score_item)
        
        layout.addWidget(table)

        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(dialog.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        dialog.setLayout(layout)
        dialog.exec()

    def load_leaderboard(self):
        """
        Загружает данные таблицы лидеров из базы данных.
        
        Returns:
            list: Список кортежей (имя, счет) отсортированный по убыванию счета
        """
        try:
            connection = sqlite3.connect("leaderboard.sqlite")
            cursor = connection.cursor()

            # Создаем таблицу если не существует
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    score FLOAT
                )
            """)

            # Получаем данные, отсортированные по убыванию счета
            cursor.execute("SELECT name, score FROM users ORDER BY score DESC")
            scores = cursor.fetchmany(10)

            connection.close()

            return scores
        except Exception as e:
            # Возвращаем заглушку при ошибке
            return [("Пока нет результатов", 0)]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
