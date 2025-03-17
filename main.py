# Импорт нужных компонентов
import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QMenuBar, QWidget, 
    QHBoxLayout, QSplitter, QTextEdit, QListWidget, QGridLayout,
    QFrame, QLabel, QGraphicsView, QGraphicsScene, QStatusBar
)
from PySide6.QtCore import QRect, QSize, QTranslator, QLocale, Qt
from PySide6.QtGui import QIcon, QScreen, QAction, QColor, QPalette
# Создаём главное окно
class AudioDBMainWindow(QMainWindow):
    # Class-level constants
    LEFT_PANEL_MIN_WIDTH = 200
    SNAP_THRESHOLD = 50

    def __init__(self):
        super().__init__()  # Инициализация окна
        
        # Настройки окна
        self.setWindowTitle("AudioDB")  # Заголовок
        
        # Установка размера окна с отступом 10% от краев экрана
        self.setDefaultWindowSize()
        
        # Создание меню бара
        self.createMenuBar()
        
        # Создание статусбара
        self.createStatusBar()
        
        # Создание разделенного интерфейса
        self.setupSplitInterface()

    def setupSplitInterface(self):
    
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
    
        # Создаем горизонтальный лейаут
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)  # Убираем отступы
    
        # Modify left widget settings
        left_widget = QWidget()
        left_widget.setMinimumWidth(self.LEFT_PANEL_MIN_WIDTH)
        left_layout = QHBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
    
        # Create splitter with custom behavior
        splitter = CustomSplitter(Qt.Horizontal, self.LEFT_PANEL_MIN_WIDTH)
    
        right_widget = QWidget()
        right_layout = QGridLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
    
        # Добавляем фоновые элементы в левую часть
    
        # Вариант 1: QFrame с установленным стилем
        left_background = QFrame()
        left_background.setStyleSheet("background-color: #e0e0e0; border: 1px solid #cccccc;")
        left_background.setFrameShape(QFrame.StyledPanel)
        left_layout.addWidget(left_background)
    
        # Добавляем фоновые элементы в правую часть (сетку)
    
        # Вариант 2: QLabel без текста
        right_background1 = QFrame()
        right_background1.setStyleSheet("background-color: #e0e0e0; border: 1px solid #cccccc;")
        right_background1.setMinimumHeight(100)
        right_layout.addWidget(right_background1, 0, 0)
    
        # Добавляем виджеты в сплиттер
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
    
        # Устанавливаем начальные размеры разделенных областей (в процентах)
        splitter.setSizes([int(self.width() * 0.3), int(self.width() * 0.7)])
    
        # Добавляем сплиттер в лейаут
        main_layout.addWidget(splitter)
        
    def createStatusBar(self):
        # Создаем статусбар
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Устанавливаем начальное сообщение
        self.statusBar.showMessage(self.tr("Ready"))
        
        # Добавляем постоянные элементы в статусбар (справа)
        version_label = QLabel("AudioDB v0.0.3")
        self.statusBar.addPermanentWidget(version_label)

    def setDefaultWindowSize(self):
        # Получаем размер доступного экрана
        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # Вычисляем размер окна (80% от размера экрана)
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Вычисляем позицию окна (отступ 10% от краев)
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        
        # Устанавливаем геометрию окна
        self.setGeometry(x_position, y_position, window_width, window_height)
    
    def createMenuBar(self):
        # Создаем меню бар
        menubar = self.menuBar()
        
        # Создаем меню "Файл"
        file_menu = menubar.addMenu(self.tr('File'))
        
        # Добавляем действия в меню "Файл"
        open_action = QAction(self.tr('Open'), self)
        open_action.setStatusTip(self.tr('Open file'))
        file_menu.addAction(open_action)
        
        save_action = QAction(self.tr('Save'), self)
        save_action.setStatusTip(self.tr('Save file'))
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(self.tr('Exit'), self)
        exit_action.setStatusTip(self.tr('Exit application'))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Создаем меню "Правка"
        edit_menu = menubar.addMenu(self.tr('Edit'))
        
        # Добавляем действия в меню "Правка"
        undo_action = QAction(self.tr('Undo'), self)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction(self.tr('Redo'), self)
        edit_menu.addAction(redo_action)
        
        # Создаем меню "Вид"
        view_menu = menubar.addMenu(self.tr('View'))
        
        # Добавляем действия в меню "Вид"
        fullscreen_action = QAction(self.tr('Fullscreen'), self)
        view_menu.addAction(fullscreen_action)
        
        # Создаем меню "Язык"
        language_menu = menubar.addMenu(self.tr('Language'))
        
        # Добавляем действия для выбора языка
        english_action = QAction('English', self)
        english_action.triggered.connect(lambda: self.changeLanguage('en'))
        language_menu.addAction(english_action)
        
        russian_action = QAction('Русский', self)
        russian_action.triggered.connect(lambda: self.changeLanguage('ru'))
        language_menu.addAction(russian_action)
        
        # Создаем меню "Справка"
        help_menu = menubar.addMenu(self.tr('Help'))
        
        # Добавляем действия в меню "Справка"
        about_action = QAction(self.tr('About'), self)
        help_menu.addAction(about_action)
    
    def changeLanguage(self, language):
        """Изменяет язык приложения"""
        # Получаем экземпляр приложения
        app = QApplication.instance()
        
        # Удаляем текущий переводчик, если он есть
        if hasattr(app, 'translator'):
            app.removeTranslator(app.translator)
        
        # Создаем новый переводчик
        app.translator = QTranslator()
        
        # Загружаем файл перевода
        if language == 'en':
            # Для английского языка (по умолчанию)
            pass
        elif language == 'ru':
            # Загружаем русский перевод
            translation_file = os.path.join('translations', 'audiodb_ru.qm')
            if os.path.exists(translation_file):
                app.translator.load(translation_file)
                app.installTranslator(app.translator)
        
        # Обновляем интерфейс
        self.retranslateUi()
    
    def retranslateUi(self):
        """Обновляет все переводимые строки в интерфейсе"""
        # Обновляем заголовок окна
        self.setWindowTitle(self.tr("AudioDB"))
        
        # Обновляем статусбар
        self.statusBar.showMessage(self.tr("Ready"))
        
        # Обновляем меню
        menubar = self.menuBar()
        menus = menubar.findChildren(QMenu)
        
        # Очищаем и пересоздаем меню
        menubar.clear()
        self.createMenuBar()

class CustomSplitter(QSplitter):
    def __init__(self, orientation, min_width, parent=None):
        super().__init__(orientation, parent)
        self.snap_threshold = AudioDBMainWindow.SNAP_THRESHOLD
        self.min_width = min_width
        
    def moveSplitter(self, pos, index):
        if pos < self.snap_threshold:
            # Snap to left edge
            super().moveSplitter(0, index)
        elif pos < 200 and pos >= self.snap_threshold:
            # Prevent resizing below 200px
            super().moveSplitter(200, index)
        else:
            # Normal splitter movement
            super().moveSplitter(pos, index)

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаём приложение
    
    # Создаем переводчик
    app.translator = QTranslator()
    
    # Определяем текущую локаль системы
    locale = QLocale.system().name()
    
    # По умолчанию используем английский язык
    # Если локаль русская, пытаемся загрузить русский перевод
    if locale.startswith('ru'):
        translation_file = os.path.join('translations', 'audiodb_ru.qm')
        if os.path.exists(translation_file):
            app.translator.load(translation_file)
            app.installTranslator(app.translator)
    
    window = AudioDBMainWindow()  # Создаём окно
    window.show()                 # Показываем окно с отступами
    sys.exit(app.exec())          # Запускаем цикл событий
