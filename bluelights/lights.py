import logging
from queue import Empty, Queue
from time import sleep
from threading import Thread
from typing import Iterable, List, Optional

from tinytuya import BulbDevice

from bluelights.domain import Color, LightSwitch


logging.basicConfig(level=logging.DEBUG)


class LightController(Thread):
    def __init__(self, switch_queue: Queue[LightSwitch], lights: Iterable[BulbDevice], default_color: Color, **kwargs):
        self._switch_queue = switch_queue
        self._switches: List[LightSwitch] = []
        self._lights = lights
        self._default_color = default_color
        self._last_update: Optional[Color] = None

        super().__init__(**kwargs)

    def run(self) -> None:
        continue_loop = True
        while continue_loop:
            sleep(1)
            self.receive_switches()
            self.remove_expired()
            highest_prio = self.get_highest_priority()
            if highest_prio is None:
                self.update_lights(self._default_color)
            else:
                self.update_lights(highest_prio.color)

    def receive_switches(self) -> None:
        while not self._switch_queue.empty():
            try:
                switch = self._switch_queue.get(block=False)
                self._switches.append(switch)
                logging.debug(f"Received switch message {switch}")
            except Empty:
                logging.info("Receiving message from switch_queue failed: empty")
                break

    def remove_expired(self) -> None:
        self._switches = [switch for switch in self._switches if not switch.expired()]

    def get_highest_priority(self) -> Optional[LightSwitch]:
        """
        Returns:
            The LightSwitch with the highest priority. If there are ones with equal priority, it returns the oldest/
            earliest in the list. If the list is empty, returns None.
        """
        highest_prio: Optional[LightSwitch] = None
        for switch in self._switches:
            if highest_prio is None or highest_prio.priority < switch.priority:
                highest_prio = switch
        return highest_prio

    def update_lights(self, color: Color) -> None:
        if color == self._last_update:
            return
        self._last_update = color
        logging.info(f"Updating Lights: {color}")
        for light in self._lights:
            light.set_colour(color.r, color.g, color.b)
