import sys
import time
from app import TaskManagerApp
from views.splash_screen import SplashScreen
from views.login_view import LoginView
from views.main_view import MainView
from services.plugin_manager import PluginManager
from config import Config

def main():
    # 1. Initialize App
    task_manager = TaskManagerApp(sys.argv)
    
    # 2. Show Splash
    splash = SplashScreen(Config.APP_NAME, Config.VERSION)
    splash.show()
    
    for i in range(1, 101):
        splash.show_progress(i)
        task_manager.app.processEvents()
    
    # 3. Show Login
    login_window = LoginView()
    
    # 4. Handle Login Success
    def on_login_success(user):
        try:
            # Create Main Window
            main_window = MainView(user)
            
            # Load Plugins
            plugin_manager = PluginManager()
            plugin_manager.load_plugins(main_window)
            
            main_window.show()
            # Keep reference to avoid garbage collection
            global win 
            win = main_window
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            import traceback
            error_msg = f"Error starting applications:\n{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            QMessageBox.critical(None, "Startup Error", error_msg)

    login_window.login_success.connect(on_login_success)
    
    splash.finish(login_window)
    login_window.show()
    
    sys.exit(task_manager.exec())

if __name__ == "__main__":
    main()
