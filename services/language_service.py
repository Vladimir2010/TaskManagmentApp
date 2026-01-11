import json
import os
from config import Config

class LanguageService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LanguageService, cls).__new__(cls)
            cls._instance.languages = {}
            cls._instance.current_lang = "en"
            cls._instance.load_languages()
        return cls._instance

    def load_languages(self):
        lang_dir = os.path.join(Config.ASSETS_DIR, 'languages')
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
            return

        for filename in os.listdir(lang_dir):
            if filename.endswith(".json"):
                lang_code = filename.split(".")[0]
                with open(os.path.join(lang_dir, filename), 'r', encoding='utf-8') as f:
                    self.languages[lang_code] = json.load(f)

    def set_language(self, lang_code):
        if lang_code in self.languages:
            self.current_lang = lang_code
            return True
        return False

    def get(self, key, **kwargs):
        lang_data = self.languages.get(self.current_lang, {})
        text = lang_data.get(key, key) # Default to key if not found
        try:
            return text.format(**kwargs)
        except:
            return text
            
    def get_current_code(self):
        return self.current_lang

# Global Instance
lang_service = LanguageService()
