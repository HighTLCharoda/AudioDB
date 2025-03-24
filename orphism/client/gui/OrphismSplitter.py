from PySide6.QtWidgets import QSplitter

class OrphismSplitter(QSplitter):
    def __init__(self, orientation, min_width, parent=None):
        super().__init__(orientation, parent)
        self.snap_threshold = OrphismMainWindow.SNAP_THRESHOLD
        self.min_width = min_width
        self.left_width = min_width  # Store the absolute width in pixels