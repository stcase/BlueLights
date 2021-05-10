from datetime import datetime, timedelta
import logging
from platform import system
from queue import Queue
from threading import Thread
from time import sleep
from typing import Callable

if system() == "Linux":
    from bluepy.btle import DefaultDelegate, ScanEntry, Scanner
else:
    from bluelights.windows_mock import DefaultDelegate, ScanEntry, Scanner

from bluelights.domain import Color, LightSwitch


logging.basicConfig(level=logging.DEBUG)


class BluetoothProximity(Thread):
    def __init__(self,
                 switch_queue: "Queue[LightSwitch]",
                 threshold_rssi: int,
                 detection_duration: timedelta,
                 priority: int,
                 color: Color,
                 **kwargs):
        self._switch_queue = switch_queue
        self._threshold_rssi = threshold_rssi
        self._detection_duration = detection_duration
        self._priority = priority
        self._color = color

        super().__init__(**kwargs)

    def run(self) -> None:
        scanner = Scanner()
        handler = BluetoothProximityHandler(self.flick_light_switch, self._threshold_rssi)
        scanner.withDelegate(handler)
        continue_loop = True
        while continue_loop:
            sleep(1)
            scanner.scan(60, passive=True)

    def flick_light_switch(self, address: str, rssi: int) -> None:
        logging.info(f"Device {address} in range ({rssi})")
        expiry = (datetime.now() + self._detection_duration).timestamp()
        flick = LightSwitch(expiry, self._priority, self._color)
        logging.debug("Sending message {switch}")
        self._switch_queue.put(flick)


class BluetoothProximityHandler(DefaultDelegate):
    def __init__(self, callback: Callable[[str, int], None], threshold_rssi: int) -> None:
        self._threshold_rssi = threshold_rssi
        self._callback = callback

    def handleDiscovery(self, dev: ScanEntry, isNewDev: bool, isNewData: bool) -> None:
        logging.debug(f"Seen device {dev.addr}, strength: {dev.rssi}")
        if int(dev.rssi) >= self._threshold_rssi:
            self._callback(dev.addr, dev.rssi)
