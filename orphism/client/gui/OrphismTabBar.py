from PySide6.QtWidgets import (
    QTabBar
)
from PySide6.QtCore import Qt

class OrphismTabBar(QTabBar):
    """Custom tab bar for the main application"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setExpanding(False)
        self.setDrawBase(True)
        self.setDocumentMode(True)
        self.setElideMode(Qt.ElideRight)
        self.setMovable(True)
        
        # Add default tabs
        self.addTab(self.tr("Library"))
        self.addTab(self.tr("Playlists"))
        self.addTab(self.tr("Favorites"))
        self.addTab(self.tr("Recent"))