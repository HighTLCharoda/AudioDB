# Импорт нужных компонентов
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QMenuBar
from PyQt5.QtCore import QRect, QSize

# Создаём главное окно
class AudioDBMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Инициализация окна
        
        # Настройки окна
        self.setWindowTitle("AudioDB")  # Заголовок
        
        # Установка размера окна с отступом 10% от краев экрана
        self.setDefaultWindowSize()
        
        # Создание меню бара
        self.createMenuBar()
        
    def setDefaultWindowSize(self):
        # Получаем размер доступного экрана
        screen_rect = QApplication.desktop().availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()
        
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
        file_menu = menubar.addMenu('Файл')
        
        # Добавляем действия в меню "Файл"
        open_action = QAction('Открыть', self)
        open_action.setStatusTip('Открыть файл')
        file_menu.addAction(open_action)
        
        save_action = QAction('Сохранить', self)
        save_action.setStatusTip('Сохранить файл')
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Выход', self)
        exit_action.setStatusTip('Выйти из приложения')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Создаем меню "Правка"
        edit_menu = menubar.addMenu('Правка')
        
        # Добавляем действия в меню "Правка"
        undo_action = QAction('Отменить', self)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction('Повторить', self)
        edit_menu.addAction(redo_action)
        
        # Создаем меню "Вид"
        view_menu = menubar.addMenu('Вид')
        
        # Добавляем действия в меню "Вид"
        fullscreen_action = QAction('Полный экран', self)
        view_menu.addAction(fullscreen_action)
        
        # Создаем меню "Справка"
        help_menu = menubar.addMenu('Справка')
        
        # Добавляем действия в меню "Справка"
        about_action = QAction('О программе', self)
        help_menu.addAction(about_action)

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаём приложение
    window = AudioDBMainWindow()        # Создаём окно
    window.show()                 # Показываем окно с отступами
    sys.exit(app.exec_())         # Запускаем цикл событий
