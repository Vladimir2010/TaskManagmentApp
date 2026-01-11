import os

class Config:
    APP_NAME = "Task Manager Pro"
    VERSION = "1.0.0"
    DB_NAME = "task_manager.db"
    CLOUD_API_URL = "http://127.0.0.1:5000/api"
    
    # Assets
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
    ICONS_DIR = os.path.join(ASSETS_DIR, 'icons')
    PLUGINS_DIR = os.path.join(BASE_DIR, 'plugins')
    
    # Appearance
    DEFAULT_THEME = "Dark"
    ACCENT_COLOR = "#0078D4"
    
    # Sync
    SYNC_INTERVAL_SECONDS = 60
    
    # Security (For real production, use env vars)
    SECRET_KEY = "super-secret-key-for-hashing"
    
    # OAuth (Mock IDs for now)
    GOOGLE_CLIENT_ID = "mock-google-client-id"
    MICROSOFT_CLIENT_ID = "mock-microsoft-client-id"
