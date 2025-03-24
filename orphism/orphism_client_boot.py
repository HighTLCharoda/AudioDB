from PySide6.QtWidgets import (QApplication)
import sys
from orphism.core.OrphismDB import *
from orphism.core.OrphismWindowLayout import *
from orphism.core.OrphismLocalization import OrphismLocalizationManager

app = QApplication(sys.argv)

# Initialize localization
localization_manager = OrphismLocalizationManager(app)
localization_manager.setup_localization()

window = OrphismMainWindow()
window.show()

sys.exit(app.exec())