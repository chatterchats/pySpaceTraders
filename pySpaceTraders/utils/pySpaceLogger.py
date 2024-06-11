"""
:Date: 8 JUN 2024
:version: 1.0
:Authors: ChatterChats
"""

import logging


class PySpaceLogger:

    def __init__(self, name: str = "pySpaceTrader", debug: bool = False):
        """
        Initializes the PySpaceLogger instance with the provided name.

        :param str name: Name of the logger
        :param bool debug: Where the logger is debug or not
        """
        self.LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.name: str = name
        self.logger: logging.Logger = logging.getLogger(f"{name}")
        self.formatter: logging.Formatter = logging.Formatter(self.LOG_FORMAT)
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)

        if not self.logger.hasHandlers():
            sh = logging.StreamHandler()
            sh.setLevel(logging.INFO)
            sh.setFormatter(self.formatter)
            sh.setLevel(logging.DEBUG if debug else logging.INFO)
            self.logger.addHandler(sh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def fatal(self, msg):
        self.logger.fatal(msg)
