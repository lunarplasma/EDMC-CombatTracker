from typing import Dict, Any
import tkinter as tk
from common import plugin_name, plugin_version

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
    controller.add_new_event(entry)


def plugin_stop() -> None:
    """
    EDMC is closing
    """
    controller.stop()
