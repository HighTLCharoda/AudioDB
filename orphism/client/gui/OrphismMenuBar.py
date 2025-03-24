from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QWidget, QListWidget, QStackedWidget, QTableWidgetItem,
    QListWidgetItem, QTableWidget, QHBoxLayout, QSplitter, QTabBar, QFrame, QLabel,
    QGridLayout, QStatusBar, QFileDialog, QMessageBox, QScrollArea, QVBoxLayout
)
from PySide6.QtCore import Qt, QTranslator, QSize
from PySide6.QtGui import QAction
import os

class OrphismMenuBar(QMenuBar):
    """Encapsulates the menu bar functionality"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setupMenus()
    
    def setupMenus(self):
        """Setup all menus in the menu bar"""
        self.createFileMenu()
        self.createEditMenu()
        self.createViewMenu()
        self.createLanguageMenu()
        self.createHelpMenu()
    
    def createFileMenu(self):
        """Create the File menu"""
        file_menu = self.addMenu(self.tr('File'))
        
        open_action = QAction(self.tr('Open'), self)
        open_action.setStatusTip(self.tr('Open file'))
        open_action.triggered.connect(self.parent.openFile)
        file_menu.addAction(open_action)
        
        save_action = QAction(self.tr('Save'), self)
        save_action.setStatusTip(self.tr('Save file'))
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(self.tr('Exit'), self)
        exit_action.setStatusTip(self.tr('Exit application'))
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)

    def createEditMenu(self):
        """Create the Edit menu"""
        edit_menu = self.addMenu(self.tr('Edit'))
        
        undo_action = QAction(self.tr('Undo'), self)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction(self.tr('Redo'), self)
        edit_menu.addAction(redo_action)

    def createViewMenu(self):
        """Create the View menu"""
        view_menu = self.addMenu(self.tr('View'))
        
        fullscreen_action = QAction(self.tr('Fullscreen'), self)
        view_menu.addAction(fullscreen_action)

    def createLanguageMenu(self):
        """Create the Language menu"""
        language_menu = self.addMenu(self.tr('Language'))
        
        english_action = QAction('English', self)
        english_action.triggered.connect(lambda: self.parent.changeLanguage('en'))
        language_menu.addAction(english_action)
        
        russian_action = QAction('Русский', self)
        russian_action.triggered.connect(lambda: self.parent.changeLanguage('ru'))
        language_menu.addAction(russian_action)

    def createHelpMenu(self):
        """Create the Help menu"""
        help_menu = self.addMenu(self.tr('Help'))
        
        about_action = QAction(self.tr('About'), self)
        about_action.triggered.connect(self.parent.showAboutDialog)
        help_menu.addAction(about_action)