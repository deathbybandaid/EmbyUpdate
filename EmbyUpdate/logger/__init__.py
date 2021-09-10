import os
import logging
from logging.config import dictConfig


from EmbyUpdate.tools import isint, closest_int_from_list


def sorted_levels(method):
    """
    Sort Logging levels by Number, and output by number/name.
    """

    level_guide = {}
    sorted_levels = sorted(logging._nameToLevel, key=lambda i: (logging._nameToLevel[i]))

    if method == "name":
        for level in sorted_levels:
            level_guide[level] = logging._nameToLevel[level]

    elif method == "number":
        for level in sorted_levels:
            level_guide[logging._nameToLevel[level]] = level

    else:
        return logging._nameToLevel

    return level_guide


class Logger():
    """
    The logging System for EmbyUpdate.
    """

    LOG_LEVEL_CUSTOM_NOOB = 25
    LOG_LEVEL_CUSTOM_SSDP = 8

    def __init__(self, settings):

        self.config = settings

        logging_config = {
            'version': 1,
            'formatters': {
                'EmbyUpdate': {
                    'format': '[%(asctime)s] %(levelname)s - %(message)s',
                    },
            },
            'loggers': {
                # all purpose, EmbyUpdate root logger
                'EmbyUpdate': {
                    'level': self.levelname,
                    'handlers': ['console', 'logfile'],
                },
            },
            'handlers': {
                # output on stderr
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'EmbyUpdate',
                },
                # generic purpose log file
                'logfile': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'filename': os.path.join(
                        self.config.internal["paths"]["logs_dir"], '.EmbyUpdate.log'),
                    'when': 'midnight',
                    'formatter': 'EmbyUpdate',
                },
            },
        }

        dictConfig(logging_config)
        self.logger = logging.getLogger('EmbyUpdate')

    @property
    def levelno(self):
        """
        Convert a configuration level name/number to applicable number.
        """

        if isint(self.config.dict["logging"]["level"]):

            levels = sorted_levels("number")

            if self.config.dict["logging"]["level"] in list(levels.keys()):
                return int(self.config.dict["logging"]["level"])

            else:
                return closest_int_from_list(list(levels.keys()), int(self.config.dict["logging"]["level"]))
        else:

            levels = sorted_levels("name")
            level = self.config.dict["logging"]["level"].upper()

            if self.config.dict["logging"]["level"].upper() not in levels:
                level = self.config.conf_default["logging"]["level"]["value"]

            return logging.getLevelName(level)

    @property
    def levelname(self):
        """
        Convert a configuration level name/number to applicable name.
        """

        if isint(self.config.dict["logging"]["level"]):

            levels = sorted_levels("number")

            if self.config.dict["logging"]["level"] in list(levels.keys()):
                level = int(self.config.dict["logging"]["level"])

            else:
                level = closest_int_from_list(list(levels.keys()), int(self.config.dict["logging"]["level"]))

            return logging.getLevelName(level)
        else:

            levels = sorted_levels("name")
            level = self.config.dict["logging"]["level"].upper()

            if self.config.dict["logging"]["level"].upper() not in levels:
                level = self.config.conf_default["logging"]["level"]["value"]

            return level

    def __getattr__(self, name):
        """
        Quick and dirty shortcuts. Will only get called for undefined attributes.
        """

        if hasattr(self.logger, name):
            return eval("self.logger.%s" % name)

        elif hasattr(self.logger, name.lower()):
            return eval("self.logger.%s" % name.lower())
