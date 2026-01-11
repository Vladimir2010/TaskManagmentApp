import os
import importlib.util
from config import Config

class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self, app_context):
        if not os.path.exists(Config.PLUGINS_DIR):
            os.makedirs(Config.PLUGINS_DIR)

        for filename in os.listdir(Config.PLUGINS_DIR):
            if filename.endswith(".py") and filename != "__init__.py":
                self._load_plugin(os.path.join(Config.PLUGINS_DIR, filename), app_context)

    def _load_plugin(self, path, app_context):
        try:
            spec = importlib.util.spec_from_file_location("plugin_module", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "register_plugin"):
                plugin_instance = module.register_plugin(app_context)
                self.plugins.append(plugin_instance)
                print(f"Loaded plugin from {path}")
        except Exception as e:
            print(f"Failed to load plugin {path}: {e}")
