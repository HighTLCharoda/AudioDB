from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QMenuBar, QWidget, QListWidget, QStackedWidget, QTableWidgetItem,
    QListWidgetItem, QTableWidget, QHBoxLayout, QSplitter, QTabBar, QFrame, QLabel,
    QGridLayout, QStatusBar, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QTranslator, QLocale, QSize
from PySide6.QtGui import QAction
import sys
import os
from sqlite_manager import *


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


class AudioDBMenuBar(QMenuBar):
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


class AudioDBStatusBar(QStatusBar):
    """Encapsulates the status bar functionality"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupStatusBar()
    
    def setupStatusBar(self):
        """Setup the application status bar"""
        self.showMessage(self.tr("Ready"))
        
        version_label = QLabel("AudioDB v0.0.3")
        self.addPermanentWidget(version_label)


class LeftPanel(QWidget):
    """Encapsulates the left navigation panel"""
    def __init__(self, min_width, parent=None):
        super().__init__(parent)
        self.min_width = min_width
        self.parent = parent
        self.setupPanel()
    
    def setupPanel(self):
        """Setup the left panel UI"""
        self.setMinimumWidth(self.min_width)
        left_layout = QHBoxLayout(self)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        left_background = QFrame()
        left_background.setStyleSheet("background-color: #e0e0e0; border: 1px solid #cccccc;")
        left_background.setFrameShape(QFrame.StyledPanel)
        left_layout.addWidget(left_background)


class MediaDisplayPanel(QWidget):
    """Encapsulates the media display panel functionality"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.db = parent.db if hasattr(parent, 'db') else None
        self.setupPanel()
    
    def setupPanel(self):
        """Setup the media display panel UI"""
        media_display_layout = QGridLayout(self)
        media_display_layout.setContentsMargins(0, 0, 0, 0)
        
        self.view_mode_bar = self.createViewModeBar()
        media_display_layout.addWidget(self.view_mode_bar, 0, 0)
        
        self.content_stack = self.createContentStack()
        media_display_layout.addWidget(self.content_stack, 1, 0)
        
        # Connect tab bar switching
        self.view_mode_bar.currentChanged.connect(self.content_stack.setCurrentIndex)
    
    def createViewModeBar(self):
        """Create the view mode selector tab bar"""
        view_mode_bar = QTabBar()
        view_mode_bar.addTab(self.tr("Tiles"))
        view_mode_bar.addTab(self.tr("Table"))
        view_mode_bar.setExpanding(False)
        return view_mode_bar

    def createContentStack(self):
        """Create the stacked widget containing different view modes"""
        content_stack = QStackedWidget()
        
        self.tile_view = self.createTileView()
        self.table_view = self.createTableView()
        
        content_stack.addWidget(self.tile_view)
        content_stack.addWidget(self.table_view)
        
        return content_stack

    def createTileView(self):
        """Create the tile view for displaying media items as tiles"""
        tile_view = QListWidget()
        
        # Populate with dummy data for now
        for i in range(12):
            item = QListWidgetItem(f"Audio File {i+1}\nDuration: 3:45\nSize: 4.2MB")
            item.setSizeHint(QSize(150, 100))
            tile_view.addItem(item)

        tile_view.setViewMode(QListWidget.IconMode)
        tile_view.setGridSize(QSize(160, 110))
        tile_view.setResizeMode(QListWidget.Adjust)
        tile_view.setWrapping(True)
        return tile_view

    def createTableView(self):
        """Create the table view for displaying media items as a table"""
        table_view = QTableWidget()
        table_view.setColumnCount(4)
        table_view.setHorizontalHeaderLabels(["Name", "Duration", "Size", "Format"])
        
        # Populate with dummy data for now
        table_view.setRowCount(12)
        for row in range(12):
            table_view.setItem(row, 0, QTableWidgetItem(f"Audio File {row+1}"))
            table_view.setItem(row, 1, QTableWidgetItem("3:45"))
            table_view.setItem(row, 2, QTableWidgetItem("4.2MB"))
            table_view.setItem(row, 3, QTableWidgetItem("MP3"))
        return table_view
    
    def refreshData(self):
        """Refresh the display with data from the database"""
        if not self.db:
            return
            
        # Clear existing data
        self.tile_view.clear()
        self.table_view.setRowCount(0)
        
        # Get audio files from database
        audio_files = self.db.get_all_audio_files()
        
        # Update tile view
        for audio in audio_files:
            duration_str = f"{int(audio['duration'] // 60)}:{int(audio['duration'] % 60):02d}" if audio['duration'] else "Unknown"
            size_str = f"{audio['size'] / (1024*1024):.2f}MB" if audio['size'] else "Unknown"
            
            item = QListWidgetItem(f"{audio['filename']}\nDuration: {duration_str}\nSize: {size_str}")
            item.setSizeHint(QSize(150, 100))
            item.setData(Qt.UserRole, audio['id'])  # Store ID for later reference
            self.tile_view.addItem(item)
        
        # Update table view
        self.table_view.setRowCount(len(audio_files))
        for row, audio in enumerate(audio_files):
            duration_str = f"{int(audio['duration'] // 60)}:{int(audio['duration'] % 60):02d}" if audio['duration'] else "Unknown"
            size_str = f"{audio['size'] / (1024*1024):.2f}MB" if audio['size'] else "Unknown"
            
            self.table_view.setItem(row, 0, QTableWidgetItem(audio['filename']))
            self.table_view.setItem(row, 1, QTableWidgetItem(duration_str))
            self.table_view.setItem(row, 2, QTableWidgetItem(size_str))
            self.table_view.setItem(row, 3, QTableWidgetItem(audio['format'] or "Unknown"))
            
            # Store ID in the first column for reference
            self.table_view.item(row, 0).setData(Qt.UserRole, audio['id'])


class AudioDBMainWindow(QMainWindow):
    LEFT_PANEL_MIN_WIDTH = 200
    SNAP_THRESHOLD = 50

    def __init__(self):
        super().__init__()
        # Initialize database connection
        self.db = AudioDBSqlite()
        if not self.db.connect():
            QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
        
        # Initialize database tables
        self.db.initialize_database()
        
        self.initializeUI()

    def initializeUI(self):
        """Initialize all UI components"""
        self.setWindowTitle("AudioDB")
        self.setupWindowSize()
        
        # Setup components
        self.menuBar = AudioDBMenuBar(self)
        self.setMenuBar(self.menuBar)
        
        self.statusBar = AudioDBStatusBar(self)
        self.setStatusBar(self.statusBar)
        
        self.setupSplitInterface()

    def setupWindowSize(self):
        """Set default window size based on screen dimensions"""
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = int(screen.width() * 0.8)
        window_height = int(screen.height() * 0.8)
        x_position = int((screen.width() - window_width) / 2)
        y_position = int((screen.height() - window_height) / 2)
        self.setGeometry(x_position, y_position, window_width, window_height)

    def setupSplitInterface(self):
        """Setup the main split interface with left panel and content area"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)
        
        self.left_panel = LeftPanel(self.LEFT_PANEL_MIN_WIDTH, self)
        self.media_display_panel = MediaDisplayPanel(self)
        
        splitter = CustomSplitter(Qt.Horizontal, self.LEFT_PANEL_MIN_WIDTH)
        splitter.addWidget(self.left_panel)
        splitter.addWidget(self.media_display_panel)
        splitter.setSizes([int(self.width() * 0.3), int(self.width() * 0.7)])
        
        main_layout.addWidget(splitter)

    def openFile(self):
        """Open audio file and add to database"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            self.tr("Open Audio File"), 
            "", 
            self.tr("Audio Files (*.mp3 *.wav *.ogg *.flac);;All Files (*)")
        )
        
        if file_path:
            # Extract basic file information
            file_info = {
                'filename': os.path.basename(file_path),
                'filepath': file_path,
                'size': os.path.getsize(file_path)
            }
            
            # TODO: Extract audio metadata using a library like mutagen
            # For now, just add with basic info
            file_id = self.db.add_audio_file(
                filename=file_info['filename'],
                filepath=file_info['filepath'],
                size=file_info['size']
            )
            
            if file_id:
                self.statusBar.showMessage(self.tr(f"Added file: {file_info['filename']}"))
                # Refresh the display
                self.media_display_panel.refreshData()
            else:
                QMessageBox.warning(self, self.tr("Error"), self.tr("Failed to add file to database"))

    def showAboutDialog(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            self.tr("About AudioDB"),
            self.tr("AudioDB v0.0.3\nA simple audio database manager.")
        )

    def changeLanguage(self, language):
        """Change the application language"""
        app = QApplication.instance()
        
        if hasattr(app, 'translator'):
            app.removeTranslator(app.translator)
        
        app.translator = QTranslator()
        
        if language == 'en':
            pass  # English is default
        elif language == 'ru':
            translation_file = os.path.join('translations', 'audiodb_ru.qm')
            if os.path.exists(translation_file):
                app.translator.load(translation_file)
                app.installTranslator(app.translator)
        
        self.updateTranslations()

    def updateTranslations(self):
        """Update all translatable strings in the interface"""
        self.setWindowTitle(self.tr("AudioDB"))
        self.statusBar.showMessage(self.tr("Ready"))
        
        # Clear and recreate menu
        self.menuBar.clear()
        self.menuBar.setupMenus()
        
        # Update view mode bar
        for i in range(self.media_display_panel.view_mode_bar.count()):
            if i == 0:
                self.media_display_panel.view_mode_bar.setTabText(i, self.tr("Tiles"))
            elif i == 1:
                self.media_display_panel.view_mode_bar.setTabText(i, self.tr("Table"))
        
        # Update table headers
        self.media_display_panel.table_view.setHorizontalHeaderLabels([
            self.tr("Name"), self.tr("Duration"), self.tr("Size"), self.tr("Format")
        ])
        
        # Refresh data display
        self.media_display_panel.refreshData()

    def closeEvent(self, event):
        """Handle window close event"""
        # Close database connection
        if hasattr(self, 'db') and self.db:
            self.db.disconnect()
        event.accept()


# Application entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Initialize translator
    app.translator = QTranslator()
    
    # Set language based on system locale
    locale = QLocale.system().name()
    if locale.startswith('ru'):
        translation_file = os.path.join('translations', 'audiodb_ru.qm')
        if os.path.exists(translation_file):
            app.translator.load(translation_file)
            app.installTranslator(app.translator)
    
    window = AudioDBMainWindow()
    window.show()
    sys.exit(app.exec())