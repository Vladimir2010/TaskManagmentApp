from PyQt6.QtWidgets import QMessageBox

class HelloWorldPlugin:
    def __init__(self, main_window):
        self.main_window = main_window
        # Example: Add a simple menu action or modify UI
        # For safety/demo, we'll just log or hook a signal if exposed
        # Here we just print on init
        print("Hello World Plugin Initialized!")

    def run(self):
        pass

def register_plugin(app_context):
    # app_context is expected to be the MainView instance
    return HelloWorldPlugin(app_context)
