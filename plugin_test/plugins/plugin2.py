from plugin_manager import PluginManager

@PluginManager.plugin_register('plugin2')
class CleanMarkdownItalic(object):
    def after_setup(self, text):
        print(text.replace('--', ''), 2)
