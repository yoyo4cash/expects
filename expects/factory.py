# -*- coding: utf-8 -*

from . import errors


class ExpectFactory(object):
    def __init__(self, named_plugins, type_plugins):
        self._named_plugins = named_plugins
        self._type_plugins = type_plugins

    def __call__(self, *args, **kwargs):
        plugin_name, actual = self.__parse_args(args, kwargs)

        if plugin_name == 'default':
            type_plugin = self._type_plugins.get(self.__type_name(actual))

            if type_plugin is not None:
                return type_plugin(actual, *self.__message(plugin_name, actual))

        try:
            return self._named_plugins[plugin_name](
                actual, *self.__message(plugin_name, actual))
        except KeyError:
            raise errors.PluginError(
                'Plugin {!r} not found'.format(plugin_name))

    def __parse_args(self, args, kwargs):
        total_args = len(args)
        total_kwargs = len(kwargs)

        if total_kwargs > 1 or (total_kwargs == 1 and total_args > 0):
            raise TypeError('expect() got an unexpected keyword argument '
                            '{!r}'.format(kwargs.popitem()[0]))

        if total_args > 1:
            raise TypeError('expect() takes 1 positional argument but '
                            '{} were given'.format(total_args))

        if total_args < 1 and total_kwargs < 1:
            raise TypeError('expect() takes 1 required positional argument')

        try:
            actual = args[0]
        except IndexError:
            plugin_name, actual = kwargs.popitem()
        else:
            plugin_name = 'default'

        return plugin_name, actual

    def __message(self, plugin_name, actual):
        message = ['Expected']

        if plugin_name != 'default':
            message.append(plugin_name)

        message.append(repr(actual))

        return message

    def __type_name(self, obj):
        obj_type = type(obj)
        return obj_type.__module__ + '.' + obj_type.__name__
