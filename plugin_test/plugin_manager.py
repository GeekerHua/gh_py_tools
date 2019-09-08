import os
import sys
import inspect


class PluginManager(object):
    PLUGINS = {}

    def after_setup(self, plugins=(), *args, **kwargs):
        return self._run_func(plugins, *args, **kwargs)

    def after_init(self, plugins=(), *args, **kwargs):
        return self._run_func(plugins, *args, **kwargs)

    def _run_func(self, plugins, *args, **kwargs):
        # curframe = inspect.currentframe()
        # calframe = inspect.getouterframes(curframe, 2)
        # print('caller name:', calframe[1][3])
        # # 获取被调用函数所在模块文件名
        # print(sys._getframe(1).f_code.co_filename)
        # 获取被调用函数名称
        # print(sys._getframe(1).f_code.co_name)
        # # 获取被调用函数在被调用时所处代码行数
        # print(sys._getframe(1).f_lineno)
        for plugin_name in plugins or self.PLUGINS.keys():
            plugin = self.PLUGINS[plugin_name]()
            func_name = sys._getframe(1).f_code.co_name
            if hasattr(plugin, func_name):
                getattr(plugin, func_name)(*args, **kwargs)
        return True

    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name: plugin})
            return plugin
        return wrapper
