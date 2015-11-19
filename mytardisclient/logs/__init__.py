"""
Custom logging for MyTardis Client allows logging to ~/.mytardisclient.log
"""

# pylint: disable=missing-docstring
# pylint: disable=bare-except


import threading
import logging
import os
import sys
import inspect
import pkgutil
import traceback


class Logger(object):
    """
    Allows logger.debug(...), logger.info(...) etc. to write to
    ~/.mytardisclient.log with custom formats.
    """
    def __init__(self, name):
        self.name = name
        self.logger_object = None
        self.logger_file_handler = None
        self.level = logging.DEBUG
        self.configure_logger()
        self.app_root_dir = \
            os.path.dirname(pkgutil.get_loader("mytardisclient.client").filename)

    def configure_logger(self):
        self.logger_object = logging.getLogger(self.name)
        self.logger_object.setLevel(self.level)

        self.log_format_string = \
            "%(asctime)s - %(moduleName)s - %(lineNumber)d - " \
            "%(functionName)s - %(currentThreadName)s - %(levelname)s - " \
            "%(message)s"

        # Send all log messages to a log file.
        self.logger_file_handler = \
            logging.FileHandler(os.path.join(os.path.expanduser("~"),
                                             ".MyData_debug_log.txt"))
        self.logger_file_handler.setLevel(self.level)
        self.logger_file_handler\
            .setFormatter(logging.Formatter(self.log_format_string))
        self.logger_object.addHandler(self.logger_file_handler)

    def set_log_filename(self, log_filename):
        self.logger_object.removeHandler(self.logger_file_handler)
        self.logger_file_handler = \
            logging.FileHandler(os.path.join(os.path.expanduser("~"),
                                             log_filename))
        self.logger_file_handler.setLevel(self.level)
        self.logger_file_handler\
            .setFormatter(logging.Formatter(self.log_format_string))
        self.logger_object.addHandler(self.logger_file_handler)

    def set_level(self, level):
        self.level = level
        self.logger_object.setLevel(self.level)
        for handler in self.logger_object.handlers:
            handler.setLevel(self.level)

    def debug(self, message):
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)[1]
        if hasattr(sys, "frozen"):
            try:
                module_name = os.path.basename(outer_frames[1])
            except:
                module_name = outer_frames[1]
        else:
            module_name = os.path.relpath(outer_frames[1], self.app_root_dir)
        extra = {'moduleName':  module_name,
                 'lineNumber': outer_frames[2],
                 'functionName': outer_frames[3],
                 'currentThreadName': threading.current_thread().name}
        self.logger_object.debug(message, extra=extra)

    def error(self, message):
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)[1]
        if hasattr(sys, "frozen"):
            try:
                module_name = os.path.basename(outer_frames[1])
            except:
                module_name = outer_frames[1]
        else:
            module_name = os.path.relpath(outer_frames[1], self.app_root_dir)
        extra = {'moduleName':  module_name,
                 'lineNumber': outer_frames[2],
                 'functionName': outer_frames[3],
                 'currentThreadName': threading.current_thread().name}
        self.logger_object.error(message, extra=extra)

    def warning(self, message):
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)[1]
        if hasattr(sys, "frozen"):
            try:
                module_name = os.path.basename(outer_frames[1])
            except:
                module_name = outer_frames[1]
        else:
            module_name = os.path.relpath(outer_frames[1], self.app_root_dir)
        extra = {'moduleName':  module_name,
                 'lineNumber': outer_frames[2],
                 'functionName': outer_frames[3],
                 'currentThreadName': threading.current_thread().name}
        self.logger_object.warning(message, extra=extra)

    def info(self, message):
        frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(frame)[1]
        if hasattr(sys, "frozen"):
            try:
                module_name = os.path.basename(outer_frames[1])
            except:
                module_name = outer_frames[1]
        else:
            module_name = os.path.relpath(outer_frames[1], self.app_root_dir)
        extra = {'moduleName':  module_name,
                 'lineNumber': outer_frames[2],
                 'functionName': outer_frames[3],
                 'currentThreadName': threading.current_thread().name}
        self.logger_object.info(message, extra=extra)


logger = Logger("MyTardis Client")  # pylint: disable=invalid-name
