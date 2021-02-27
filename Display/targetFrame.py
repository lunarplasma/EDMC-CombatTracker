import tkinter as tk
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from prefs import AutoInc

from theme import theme

# Logging set-up as per EDMC directive
from common import logger_name, Fonts

logger = logging.getLogger(logger_name)


class TargetFrame(tk.Frame):
    def _label(self, text, row, column, sticky, **kw):
        label = tk.Label(self._target_frame, text=text, font=Fonts.Targets, **kw)
        label.grid(row=row, column=column, sticky=sticky)
        return label

    def __init__(self, parent, **kw):
        """Create this frame"""
        super().__init__(parent, **kw)

        title = tk.Label(
            self,
            text=f"Target Ship",
            justify=tk.LEFT,
            font=Fonts.Title,
        )
        title.grid(row=0, column=0, sticky=tk.W)

        # Initialise the Target frame
        self._target_frame = tk.Frame(self)
        self._target_frame.grid(row=2, column=0, sticky=tk.W)

        self._label(text="  ", row=0, column=0, sticky=tk.E)
        self._label(text="Target:", row=0, column=1, sticky=tk.E)
        self._target = self._label(
            text="<target>",
            row=0,
            column=2,
            sticky=tk.W,
        )

        self._label(text="Status:", row=1, column=1, sticky=tk.E)
        self._wanted = self._label(
            text="<Wanted>", row=1, column=2, sticky=tk.W, fg="red"
        )

        self._label(text="Bounty:", row=2, column=1, sticky=tk.W)
        self._bounty = self._label(
            text="<bounty>",
            row=2,
            column=2,
            sticky=tk.W,
        )

        self._label(text="Faction:", row=3, column=1, sticky=tk.E)
        self._faction = self._label(text="", row=3, column=2, sticky=tk.W)
        self.reset_contact()
        self._target.configure(text="No ship targeted")

    def reset_contact(self):
        self._target.config(text="")
        self._wanted.config(text="")
        self._bounty.config(text="")
        self._faction.config(text="")

    def _update_wanted(self, new_state):
        self._wanted.config(text=new_state)
        if new_state == "Wanted":
            self._wanted.config(fg="red")
        else:
            self._wanted.config(fg="green")

    def update_data(self, data):
        assert data["event"] == "ShipTargeted", "This only accepts ShipTargeted"
        self.reset_contact()
        if data["TargetLocked"]:
            logger.info(f"Updating target info: {data['Ship']}")
            scan_stage = data["ScanStage"]
            if scan_stage == 0:
                self._target.config(text="Scanning...")
            else:
                target = f"{data['PilotName_Localised']} [{data['PilotRank']}]"
                self._target.config(text=target)

            if scan_stage > 1:
                pass
            if scan_stage > 2:
                self._faction.config(text=data["Faction"])
                self._update_wanted(data["LegalStatus"])
                if "Bounty" in data:
                    bounty = f"{data['Bounty']:,d} cr"
                    self._bounty.config(text=bounty)
            else:
                self._wanted.config(text="Scanning...")
                # copy the config colour of something else
                self._wanted.config(fg=self._target.cget("fg"))
                self._bounty.config(text="Scanning...")
                self._faction.config(text="Scanning...")
        else:
            self._target.config(text="No ship targeted")
