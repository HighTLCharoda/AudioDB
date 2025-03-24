from PySide6.QtWidgets import (
    QLabel,
    QStatusBar
)

class OrphismStatusBar(QStatusBar):
    """Encapsulates the status bar functionality"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupStatusBar()
    
    def setupStatusBar(self):
        """Setup the application status bar"""
        self.showMessage(self.tr("Ready"))
        
        version_label = QLabel("AudioDB v0.0.3")
        self.addPermanentWidget(version_label)