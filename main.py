from datetime import timedelta
from queue import Queue

from tinytuya import BulbDevice

from bluelights.bluetooth import BluetoothProximity
from bluelights.domain import Color, LightSwitch
from bluelights.lights import LightController
import config  # type: ignore


def main() -> None:
    d = BulbDevice(config.bulb["id"], config.bulb["ip"], config.local_key)
    d.set_version(config.bulb["version"])
    d.status()

    switch_queue: Queue[LightSwitch] = Queue()
    ble = BluetoothProximity(switch_queue, -50, timedelta(seconds=5), 50, Color(0, 255, 0))
    lc = LightController(switch_queue, [d], Color(255, 0, 0))
    ble.start()
    lc.start()
    ble.join()
    lc.join()


if __name__ == "__main__":
    main()
