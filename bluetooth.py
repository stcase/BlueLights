from datetime import datetime, timedelta
import logging
from typing import Callable

from bluepy.btle import DefaultDelegate, ScanEntry, Scanner


logging.basicConfig(level=logging.DEBUG)


class LightController:
    def __init__(self) -> None:
        self.expiriers = OrderedDict

    def add_event(self, strength: int, expiry: datetime, data: object) -> None:
        pass

    def _prune_and_get_highest_value(self) -> None:
        pass

    def _get_max_level(self) -> int:


class BluetoothTracker(DefaultDelegate):
    def __init__(self, callback: Callable[[int, datetime, object], None], min_rssi: int, max_rssi: int, expiry: timedelta) -> None:
        self.min_rssi = min_rssi
        self.max_rssi = max_rssi
        self.expiry = expiry
        self.callback = callback
        self.devices: Dict[str, str] = {}

    def _interpolate(self, val: int) -> int:
        """
        Interpolates val between minVal and maxVal and gives it a corresponding value between 0 and 100
        """
        testVal = int((val - self.min_rssi)/(self.max_rssi - self.min_rssi) * 100)
        return max(0, min(100, testVal))

    def handleDiscovery(self, dev: ScanEntry, isNewDev: bool, isNewData: bool):
        self.devices[dev.addr] = dev.rssi
        logging.debug(f"Seen device {dev.addr}, strength: {dev.rssi}")
        self.callback(self._interpolate(int(dev.rssi)), datetime.now() + self.expiry, {"addr": dev.addr, "rssi": dev.rssi})


def main():
    scanner = Scanner()
    test_callback = lambda a, b, c: None
    tracker = BluetoothTracker(test_callback, -80, -50, timedelta(seconds=3))
    scanner.withDelegate(tracker)
    devices = scanner.scan(60, passive=True)
    for dev in devices:
        print(f"Device {dev.addr} @ strength {dev.rssi}")

    
if __name__ == "__main__":
    main()
