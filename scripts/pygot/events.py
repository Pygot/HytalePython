# type: ignore

from java.util.function import Consumer


class _PyConsumer(Consumer):
    def __init__(self, fn):
        self._fn = fn

    def accept(self, event):
        self._fn(event)


def register_global(plugin, event, method):
    plugin.getEventRegistry().registerGlobal(event, _PyConsumer(method))
    return True