from plugin_manager import PluginManager
from plugins import *

def test():
    plugin_manager = PluginManager()
    # print(plugin_manager.PLUGINS)
    # processed = plugin_manager.after_setup(text="**foo bar**", plugins=('plugin1', ))
    # print('--------')
    plugin_manager.after_setup(text="--foo bar--")


if __name__ == "__main__":
    test()
