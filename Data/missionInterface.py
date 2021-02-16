from datetime import datetime
from typing import Dict, List, Any


class MissionInterface:
    """All mission types should implement these"""
    def add_event(self, new_event: dict):
        raise NotImplementedError(self.__name__ + " does not implement add_event")

    def grouped_by_faction(self) -> Dict[str, List[Dict]]:
        raise NotImplementedError(
            self.__name__ + " does not implement grouped_by_faction"
        )
