import os, logging
from typing import Dict, Any, Set, List
from collections import OrderedDict
from .missionInterface import MissionInterface

# Logging set-up as per EDMC directive
from common import logger_name
logger = logging.getLogger(logger_name)


class Massacres(MissionInterface):
    """Handles Massacre missions"""

    def add_event(self, event: dict):
        """Adds a new event to the missions list"""
        assert "Massacre" in event["Name"], "Expecting a Massacre mission!"
        mission_id = int(event["MissionID"])
        mission_event = event["event"]
        massacre = self._store_new_massacre(mission_id, event)

        if "Accepted" in mission_event:
            self._add_to_factions(faction=event["Faction"], mission_id=mission_id)
        elif "Completed" in mission_event or "Abandoned" in mission_event:
            # move the mission to the completed pile
            self._completed[mission_id] = massacre
            del self._massacres[mission_id]
            if "Faction" in massacre:
                self._remove_from_factions(
                    faction=massacre["Faction"], mission_id=mission_id
                )

    def _store_new_massacre(self, mission_id, new_massacre: dict) -> dict:
        # Get the massacre based on the ID, or store it.

        if mission_id not in self._massacres:
            self._massacres[mission_id] = new_massacre
        else:
            self._massacres[mission_id]["event"] = new_massacre["event"]
            self._massacres[mission_id].update(new_massacre)
        return self._massacres[mission_id]

    def _add_to_factions(self, faction, mission_id):
        """Adds this mission id to the factions list"""
        by_faction = self._by_faction.setdefault(faction, [])
        by_faction.append(mission_id)

    def _remove_from_factions(self, faction, mission_id):
        """
        Removes the mission id from the factions list
        Also clears the faction from the list if it's empty.
        """
        if faction in self._by_faction:
            ids: List[int]
            ids = self._by_faction[faction]
            if mission_id in ids:
                ids.remove(mission_id)
                # Get rid of the faction if it's empty
                if len(self._by_faction[faction]) == 0:
                    del self._by_faction[faction]

    def __init__(self):
        """
        Initialise the missions handler
        """
        # massacres, arranged by mission_id
        _massacres: Dict[int, Dict]
        self._massacres = OrderedDict()

        # completed missions go here
        _completed: Dict[int, Dict]
        self._completed = OrderedDict()

        _by_faction: Dict[str, Set[int]]  # mission_id grouped by faction
        self._by_faction = OrderedDict()

        logger.debug("Massacre mission tracker initialised")

    def grouped_by_faction(self) -> Dict[str, List[Dict]]:
        """
        Get a dictionary of lists of missions per faction.
        :return:
        """
        by_faction: Dict[str, List[Dict]]  # faction is the str key
        by_faction = {
            faction: [self._massacres[mission_id] for mission_id in mission_ids]
            for faction, mission_ids in self._by_faction.items()
        }
        return by_faction
