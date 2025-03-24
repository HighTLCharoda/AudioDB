from PySide6.QtWidgets import (
    QWidget, 
    QListWidget, 
    QStackedWidget, 
    QTableWidgetItem,
    QListWidgetItem, 
    QTableWidget, 
    QTabBar,
    QGridLayout
)
from PySide6.QtCore import Qt, QSize

class OrphismMediaDisplayPanel(QWidget):

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
        # Уменьшаем размер сетки, чтобы элементы были ближе друг к другу
        tile_view.setGridSize(QSize(152, 102))
        tile_view.setResizeMode(QListWidget.Adjust)
        tile_view.setWrapping(True)
        
        # Отключаем возможность перетаскивания элементов
        tile_view.setDragEnabled(False)
        
        # Используем отрицательное значение для spacing, чтобы уменьшить промежутки
        
        # Фиксируем элементы на сетке
        tile_view.setMovement(QListWidget.Static)
        
        # Настраиваем стили для уменьшения отступов и границ
        tile_view.setStyleSheet("""
            QListWidget {
                background-color: #f5f5f5;
                padding: 0px;
                margin: 0px;
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin: 0px;
                padding: 2px;
            }
            QListWidget::item:selected {
                background-color: #e0e0ff;
                border: 1px solid #9090ff;
            }
        """)
        
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