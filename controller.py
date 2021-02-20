from typing import Dict, List

from monitor import (
    monitor,
)  # imports from the EDMarketConnector. Is used to obtain the logs folder.

from Data import MissionInterface, Massacres
from Display.massacreFrame import MassacreFrame
import logging
import time
import json
import os
from datetime import timedelta, datetime
import re
import tkinter as tk


# Logging set-up as per EDMC directive
from common import logger_name

logger = logging.getLogger(logger_name)


class Controller:
    """
    This class is meant to control the database access, hold all the trackers,
    and handle event assignment to the different event trackers
    """

    _event_watchers: Dict[str, List[MissionInterface]]

    @staticmethod
    def get_journal_folder():
        """Returns the journal folder"""
        return monitor.currentdir

    @staticmethod
    def filter_logs_by_date(
        logs: List[str], start_date: datetime, end_date: datetime = datetime.now()
    ) -> List[str]:
        """
        Parses log filenames and returns those whose parsed date are
        within the specified dates (inclusive).
        :param logs: List of log filenames to search through.
        :param start_date: Oldest file date to search for.
        :param end_date: Newest file date to search for.
        :return: list of logs
        """
        assert start_date < end_date, "start_date must come before end_date"
        wanted_logs = []
        matcher = re.compile(
            r"^Journal\."
            r"(?P<YY>\d\d)"
            r"(?P<MM>\d\d)"
            r"(?P<DD>\d\d)"
            r"(?P<hh>\d\d)"
            r"(?P<mm>\d\d)"
            r"(?P<ss>\d\d)"
        )
        for log in logs:
            match = matcher.search(log)
            if match:
                # Note - these are all 2 digits, including the year
                log_date = datetime(
                    year=int(match.group("YY")) + 2000,
                    month=int(match.group("MM")),
                    day=int(match.group("DD")),
                )

                if start_date <= log_date <= end_date:
                    wanted_logs.append(log)

        return wanted_logs

    def rebuild_from_logs(self):
        """
        This will attempt to read the past seven days from the log files.
        """
        journal_folder = self.get_journal_folder()
        logger.info(f"Starting to read previous journal files: {journal_folder}")

        logs = [f for f in os.listdir(journal_folder) if ".log" in f]  # get logs only
        a_week_ago = datetime.now() - timedelta(days=7)
        wanted_logs = self.filter_logs_by_date(logs, start_date=a_week_ago)

        files_with_issues = []
        for log in wanted_logs:
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
        self._logs_scanned = True

    def __init__(self):
        """
        Initialise the Controller class.
        """
        # launch a thread that will wait for `monitor` to be ready,
        # then launch use the reader to get the latest relevant lines of mission data.

        self.massacre_frame = None  # initialise with register_frame
        self._event_watchers = {}  # key: event name, value: List(DataInterface)
        self._massacre_tracker = Massacres()

        self._logs_scanned = False  # flag to indicate that the logs have been scanned

        logger.debug("Combat controller initialised")

    @property
    def logs_scanned(self):
        """Flag indicating whether the initial startup scan has been done yet or not."""
        return self._logs_scanned

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
        massacre_data = self._massacre_tracker.grouped_by_faction()
        if massacre_data:
            while not self.massacre_frame:
                pass
            self.massacre_frame.update_data(massacre_data)

    def stop(self):
        """Shutdown the controller"""
        pass


# Here, we can set this up to use an environment variable
# to replace the journal folder location. We'll update the Controller
# to use all the files from that directory.
test_folder = os.getenv("PLUGIN_TEST_FOLDER")
if test_folder:
    target_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), test_folder)

    def return_files(obj, files, *args, **kwargs):
        return files

    Controller.filter_logs_by_date = return_files
    Controller.get_journal_folder = lambda *args: target_path
