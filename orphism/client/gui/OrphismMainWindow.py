from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QStackedWidget, 
    QHBoxLayout, 
    QFrame, 
    QLabel, 
    QFileDialog, 
    QMessageBox, 
    QScrollArea, 
    QVBoxLayout
)
from PySide6.QtCore import Qt, QTranslator
import os



class OrphismMainWindow(QMainWindow):
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
        self.menuBar = OrphismMenuBar(self)
        self.setMenuBar(self.menuBar)
        
        self.statusBar = OrphismStatusBar(self)
        self.setStatusBar(self.statusBar)
        
        # Create main tab bar
        self.main_tab_bar = OrphismTabBar(self)
        
        # Create main content area
        self.main_content = QStackedWidget()
        
        # Setup the split interface for the first tab (Library)
        self.library_widget = QWidget()
        self.setupSplitInterface(self.library_widget)
        
        # Add placeholder widgets for other tabs
        self.playlists_widget = QWidget()
        self.playlists_widget.setLayout(QVBoxLayout())
        self.playlists_widget.layout().addWidget(QLabel("Playlists - Coming Soon"))
        
        self.favorites_widget = QWidget()
        self.favorites_widget.setLayout(QVBoxLayout())
        self.favorites_widget.layout().addWidget(QLabel("Favorites - Coming Soon"))
        
        self.recent_widget = QWidget()
        self.recent_widget.setLayout(QVBoxLayout())
        self.recent_widget.layout().addWidget(QLabel("Recent - Coming Soon"))
        
        # Add all widgets to the stacked widget
        self.main_content.addWidget(self.library_widget)
        self.main_content.addWidget(self.playlists_widget)
        self.main_content.addWidget(self.favorites_widget)
        self.main_content.addWidget(self.recent_widget)
        
        # Connect tab bar to stacked widget
        self.main_tab_bar.currentChanged.connect(self.main_content.setCurrentIndex)
        
        # Create central layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(0)
        
        # Add tab bar and content to layout
        main_layout.addWidget(self.main_tab_bar)
        main_layout.addWidget(self.main_content)

    def setupWindowSize(self):
        """Set default window size based on screen dimensions"""
        screen = QApplication.primaryScreen().availableGeometry()
        window_width = int(screen.width() * 0.8)
        window_height = int(screen.height() * 0.8)
        x_position = int((screen.width() - window_width) / 2)
        y_position = int((screen.height() - window_height) / 2)
        self.setGeometry(x_position, y_position, window_width, window_height)

    def setupSplitInterface(self, parent_widget):
        """Setup the main split interface with left panel and content area"""
        layout = QHBoxLayout(parent_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.left_panel = OrphismToolsetPanel(self.LEFT_PANEL_MIN_WIDTH, self)
        
        # Create media display panel
        media_display = OrphismMediaDisplayPanel(self)
        
        # Wrap media display panel in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(media_display)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Create and configure splitter
        splitter = OrphismSplitter(Qt.Horizontal, self.LEFT_PANEL_MIN_WIDTH)
        splitter.addWidget(self.left_panel)
        splitter.addWidget(scroll_area)
        splitter.setSizes([int(parent_widget.width() * 0.3), int(parent_widget.width() * 0.7)])
        
        layout.addWidget(splitter)
        
        # Store reference to media display panel for later use
        self.media_display_panel = media_display

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
        
        # Update main tab bar
        tab_texts = [self.tr("Library"), self.tr("Playlists"), 
                     self.tr("Favorites"), self.tr("Recent")]
        for i, text in enumerate(tab_texts):
            if i < self.main_tab_bar.count():
                self.main_tab_bar.setTabText(i, text)
        
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