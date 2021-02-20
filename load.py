from typing import Dict, Any
import tkinter as tk
import logging
from common import plugin_name, plugin_version, logger_name

from controller import Controller

# Logging set-up as per EDMC directive
from common import logger_name

logger = logging.getLogger(logger_name)

# The global controller singleton
controller = None


def plugin_start3(plugin_dir: str = None) -> str:
    """
    Load this plugin into EDMC
    """
    logger.info("Plugin start.")

    global controller
    controller = Controller()

    return plugin_name


def plugin_app(parent: tk.Frame) -> tk.Frame:
    """
    EDMC Hook: creates the GUI elements.
    :param parent:
    :return:
    """
    logger.info("Plugin app.")
    return controller.register_frame(version=plugin_version, parent=parent)


def journal_entry(
    cmdr: str,
    is_beta: bool,
    system: str,
    station: str,
    entry: Dict[str, Any],
    state: Dict[str, Any],
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
    if controller.logs_scanned is False:
        controller.rebuild_from_logs()

    controller.add_new_event(entry)


def plugin_stop() -> None:
    """
    EDMC is closing
    """
    controller.stop()
