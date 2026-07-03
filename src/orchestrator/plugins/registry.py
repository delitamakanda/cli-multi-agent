class PluginRegistry:
    def __init__(self):
        self._plugins = {}
    
    def register_plugin(self, plugin_name: str, plugin_class):
        self._plugins[plugin_name] = plugin_class

    def get_plugin(self, plugin_name: str):
        return self._plugins.get(plugin_name)