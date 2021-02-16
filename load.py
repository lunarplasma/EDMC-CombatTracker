from typing import Dict, Any
import tkinter as tk
import logging
import os

from config import appname

plugin_version = "0.1.0"

# This could also be returned from plugin_start3()
plugin_name = os.path.basename(os.path.dirname(__file__))

# A Logger is used per 'found' plugin to make it easy to include the plugin's
# folder name in the logging output format.
# NB: plugin_name here *must* be the plugin's folder name as per the preceding
#     code, else the logger won't be properly set up.
logger = logging.getLogger(f'{appname}.{plugin_name}.{plugin_version}')

# If the Logger has handlers then it was already set up by the core code, else
# it needs setting up here.
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(
        f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

from controller import Controller

controller = Controller()  # singleton


def plugin_start3(plugin_dir: str) -> str:
    """
    Load this plugin into EDMC
    """
    return plugin_name


def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    EDMC Hook: creates the GUI elements.
    :param parent:
    :return:
    """
    return controller.register_frame(version=plugin_version, parent=parent)


def journal_entry(cmdr: str
                  , is_beta: bool
                  , system: str
                  , station: str
                  , entry: Dict[str, Any]
                  , state: Dict[str, Any]
                  ) -> None:
    """
    EDMC hook which occurs when a new event is detected.
    :param cmdr:
    :param is_beta:
    :param system:
    :param station:
    :param entry:
    :param state:
    :return:
    """
    controller.add_new_event(entry)


def plugin_stop() -> None:
    """
    EDMC is closing
    """
    controller.stop()
