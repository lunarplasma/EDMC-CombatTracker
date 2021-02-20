import tkinter as tk
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from theme import theme

# Logging set-up as per EDMC directive
from common import logger_name

logger = logging.getLogger(logger_name)


class MassacreFrame(tk.Frame):
    def __init__(self, parent, version, **kw):
        """Create this frame"""
        super().__init__(parent, **kw)

        # Initialise the frame
        title = tk.Label(
            self,
            text=f"Massacre Tracker {version}",
            justify=tk.LEFT,
            font=("helvetica", 12, "underline"),
        )
        title.grid(row=0, column=0, sticky=tk.W)

        self._content = tk.Frame(self, **kw)
        self._content.grid(row=2, column=0, sticky=tk.W)
        self._content.grid_columnconfigure(0, minsize=15)
        self._row_data = {}  # key by mission_id
        self._factions = []

    @staticmethod
    def str_delta(delta: timedelta):
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        result = ""
        if days > 0:
            result = f"{days} days,"
        result += f"{hours} hours, {minutes} minutes"
        return result

    def faction_label(self, faction: str, row_no):
        label = tk.Label(
            self._content, text=faction, font=("Helvetica", "10", "italic")
        )
        label.grid(row=row_no, column=0, sticky=tk.W, columnspan=5)
        return label

    def data_label(self, text, row, column, sticky=tk.W):
        label = tk.Label(self._content, text=text)
        label.grid(row=row, column=column, sticky=sticky)
        return label

    def data_row(
        self,
        row,
        location: str,
        reward: str,
        killcount: str,
        expiry: str,
    ):

        labels = []
        items = [location, reward, killcount, expiry]
        column = 0

        for item in items:
            # for each one, add a spacer, then the data
            labels.append(self.data_label(text=" ", row=row, column=column))
            column += 1
            labels.append(self.data_label(text=f"{item}", row=row, column=column))
            column += 1

        row_data = {
            "location": labels[0],
            "reward": labels[1],
            "killcount": labels[2],
            "expiry": labels[3],
        }

        return row_data

    def clear_content(self):
        for widget in self._content.winfo_children():
            widget.destroy()

    def legends(self, row):
        # Legend
        self.data_row(
            row=row,
            location="Location",
            reward="Reward",
            killcount="Kill Count",
            expiry="Expiry",
        )

    def update_data(self, data: Dict[str, Dict[str, Any]]):
        factions = data.keys()

        # if self._factions != factions:
        #     self._factions = factions
        self.clear_content()
        self.legends(0)

        row_no = 1
        for faction, events in data.items():
            title_rowno = row_no
            faction_label = self.faction_label(faction, row_no=row_no)
            row_no += 1
            total_killcount = 0
            for event in events:
                event: Dict[str, Any]
                obj_done = False

                # location
                if event["event"] == "MissionRedirected":
                    obj_done = True
                    location = f'->{event["NewDestinationStation"]} ({event["NewDestinationSystem"]})'
                else:
                    location = f'{event["DestinationSystem"]}'

                # reward
                reward = f'{event["Reward"]:,d} cr'

                # kills
                killcount = event["KillCount"]
                if obj_done is False:
                    total_killcount += int(killcount)
                else:
                    killcount = ""

                # expiry
                time_left = "<Objective Complete>"
                expiry = "<Objective Complete>"
                if obj_done is False:
                    expiry = datetime.strptime(event["Expiry"], "%Y-%m-%dT%H:%M:%SZ")
                    expiry = expiry.replace(second=0)
                    time_left_delta = expiry - datetime.now().replace(
                        microsecond=0, second=0
                    )
                    time_left = self.str_delta(time_left_delta)

                row_data = self.data_row(
                    row=row_no,
                    location=location,
                    reward=reward,
                    killcount=killcount,
                    expiry=expiry,
                )

                row_no += 1

            # Add the killcount label
            if total_killcount > 0:
                kill_text = f"{total_killcount}"
                tk.Label(
                    self._content,
                    justify=tk.RIGHT,
                    text=kill_text,
                    font=(
                        "Helvetica",
                        "10",
                        "italic",
                    ),
                ).grid(row=title_rowno, column=5, sticky=tk.W, columnspan=3)

        theme.update(self._content)
