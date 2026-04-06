# type: ignore

from java.util.logging import Level

from defaults import prefix


class Log:
    def __init__(self, hytale_logger, is_debug):
        self.hytale_logger = hytale_logger
        self.is_debug = is_debug

    def info(self, message):
        self.hytale_logger.at(Level.INFO).log(prefix + message)
        return True

    def error(self, message):
        self.hytale_logger.at(Level.SEVERE).log(prefix + message)
        return True

    def debug(self, message):
        if self.is_debug:
            self.hytale_logger.at(Level.INFO).log("[DEBUG] " + prefix + message)
        return self.is_debug