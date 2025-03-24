from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QFrame
)

class OrphismToolsetPanel(QWidget):
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