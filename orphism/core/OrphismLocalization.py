from PySide6.QtCore import QTranslator, QLocale
import os

class OrphismLocalizationManager:
    """
    Class responsible for managing application localization.
    Handles loading and applying translations based on system locale.
    """
    
    def __init__(self, app):
        """
        Initialize the localization manager.
        
        Args:
            app: QApplication instance to apply translations to
        """
        self.app = app
        self.translator = QTranslator()
        self.app.translator = self.translator
    
    def setup_localization(self):
        """
        Set up application localization based on system locale.
        Currently supports Russian language.
        """
        locale = QLocale.system().name()
        
        if locale.startswith('ru'):
            self._load_russian_translation()
    
    def _load_russian_translation(self):
        """
        Load Russian translation if available.
        """
        translation_file = os.path.join('translations', 'audiodb_ru.qm')
        if os.path.exists(translation_file):
            self.translator.load(translation_file)
            self.app.installTranslator(self.translator)
    
    def change_language(self, language_code):
        """
        Change application language manually.
        
        Args:
            language_code: String code of the language (e.g., 'ru', 'en')
        
        Returns:
            bool: True if language was changed successfully, False otherwise
        """
        if language_code == 'ru':
            return self._load_russian_translation()
        elif language_code == 'en':
            # Remove translator to use default English
            self.app.removeTranslator(self.translator)
            return True
        
        return False