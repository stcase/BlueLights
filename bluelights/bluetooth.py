from datetime import datetime, timedelta
import logging
from platform import system
from queue import Queue
from threading import Thread
from time import sleep
from typing import Callable, Dict, List

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
    def __init__(self, callback: Callable[[str, int], None], threshold_rssi: int, threshold_timer: float = 2) -> None:
        """
        Args:
            callback: Function to be called when a device is seen
            threshold_rssi: The threshold rssi for a seen device to trigger the light
            threshold_timer: The duration a light must be above threshold for to trigger the light
        """
        self._threshold_rssi = threshold_rssi
        self._threshold_timer = threshold_timer
        self._callback = callback
        self._seen_devices: Dict[str, List[float]] = {}  # _seen_devices[addr] = [last seen, most recent]

    def _passes_threshold(self, dev: ScanEntry) -> bool:
        """
        Determines whether a device should trigger the light or not by seeing how long the device has been above the
        threshold. Also maintains the `_seen_devices` dictionary.

        Returns:
            True if the light should be triggered by this device
        """
        triggered = False
        now = datetime.now().timestamp()
        if int(dev.rssi) >= self._threshold_rssi:
            timediff = now - self._seen_devices.setdefault(dev.addr, [now, now])[0]
            self._seen_devices[dev.addr][1] = now
            triggered = triggered or timediff >= self._threshold_timer
        elif dev.addr in self._seen_devices:
            del self._seen_devices[dev.addr]

        for addr, times in list(self._seen_devices.items()):
            if now - times[1] > 2 * self._threshold_timer:
                del self._seen_devices[addr]

        return triggered

    def handleDiscovery(self, dev: ScanEntry, isNewDev: bool, isNewData: bool) -> None:
        logging.debug(f"Seen device {dev.addr}, strength: {dev.rssi}")
        if self._passes_threshold(dev):
            self._callback(dev.addr, dev.rssi)
