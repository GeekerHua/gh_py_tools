from plugin_manager import PluginManager
@PluginManager.plugin_register('plugin1')
class CleanMarkdownBolds(object):
    def after_setup(self, text):
        print(text.replace('**', ''), 1)
