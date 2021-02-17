from typing import Dict, List

from monitor import (
    monitor,
)  # imports from the EDMarketConnector. Is used to obtain the logs folder.
import threading
from Data import MissionInterface, Massacres
from Display.massacreFrame import MassacreFrame
import logging
import time
import json
import os
import tkinter as tk

# Logging set-up as per EDMC directive
from config import appname

plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f"{appname}.{plugin_name}")


class Controller:
    """
    This class is meant to control the database access, hold all the trackers,
    and handle event assignment to the different event trackers
    """

    _event_watchers: Dict[str, List[MissionInterface]]

    def rebuild_from_logs(self):
        """
        This will attempt to read the past seven days from the log files.
        """
        while monitor.currentdir is None:
            time.sleep(1.0)
        journal_folder = monitor.currentdir
        # journal_folder = os.path.join(os.path.dirname(__file__), "Test\\Data") # for rudimentary testing
        logger.info(f"Starting to read previous journal files: {journal_folder}")

        logs = [f for f in os.listdir(journal_folder) if ".log" in f]  # get logs only
        logs.sort(reverse=True)
        logs = logs[0:7]  # Get the last 7 days
        logs.sort()
        files_with_issues = []
        for log in logs:
            log_file = os.path.join(journal_folder, log)
            logger.info(f"Reading {log_file}")
            with open(log_file, "r", encoding="UTF-8") as file:
                line_no = 1
                line = file.readline()
                while line:
                    try:
                        event = json.loads(line)
                        self.add_new_event(event, update_gui=False)
                        line = file.readline()
                        line_no = line_no + 1
                    except:
                        if log_file not in files_with_issues:
                            logger.exception(
                                f"Error parsing {log_file}, {line_no}: {line}"
                            )
                            files_with_issues.append(log_file)
                        break
        logger.info("Finished reading journals.")
        self.update_massacre_display()

    def __init__(self):
        """
        Initialise the Controller class.
        """
        # launch a thread that will wait for `monitor` to be ready,
        # then launch use the reader to get the latest relevant lines of mission data.
        threading.Thread(target=self.rebuild_from_logs).start()
        self.massacre_frame = None  # initialise with register_frame
        self._event_watchers = {}  # key: event name, value: List(DataInterface)
        self._massacre_tracker = Massacres()
        self._lock = threading.Lock()

        self.alive = True
        self.updater = threading.Thread(target=self.refresh_massacre_thread)
        self.updater.start()

    def stop(self):
        self.alive = False

    def refresh_massacre_thread(self):
        sleep_time = 0.5
        wait_time = 60
        wait_count = wait_time / sleep_time
        incrementer = 0
        while self.alive is True:
            incrementer += 1
            if incrementer > wait_count:
                logger.info("Refreshing display")
                self.update_massacre_display()
                incrementer = 0
            else:
                time.sleep(sleep_time)

    def register_frame(self, version, parent=tk.Frame):
        """Registers the parent frame and initialises the tracker panels"""
        self.massacre_frame = MassacreFrame(parent, version=version)
        return self.massacre_frame

    def add_new_event(self, new_event: dict, update_gui: bool = True) -> None:
        """
        Records the occurrence of a new event.
        :param new_event: The event to record.
        :param update_gui: If true, the GUI frame is also updated
        """
        event_name = new_event["event"]

        if "Mission" in event_name and "Name" in new_event:
            if "Massacre" in new_event["Name"]:
                self._massacre_tracker.add_event(event=new_event)
                if update_gui:
                    self.update_massacre_display()

    def update_massacre_display(self):
        """Updates the massacre display frame"""
        with self._lock:
            massacre_data = self._massacre_tracker.grouped_by_faction()
            self.massacre_frame.update_data(massacre_data)
