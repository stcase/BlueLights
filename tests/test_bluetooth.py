from datetime import datetime, timedelta
from queue import Queue
from unittest.mock import Mock

from freezegun import freeze_time

from bluelights.bluetooth import BluetoothProximity, BluetoothProximityHandler
from bluelights.domain import Color, LightSwitch


class TestBluetoothProximity:
    @freeze_time("2020-01-01 12:00:02")
    def test_send_message(self) -> None:
        queue: Queue[LightSwitch] = Queue()
        blp = BluetoothProximity(queue, -50, timedelta(seconds=3), 50, Color(1, 2, 3))
        blp.flick_light_switch("fa:ke:ad:dr", -42)

        assert queue.qsize() == 1
        actual = queue.get()
        assert actual == LightSwitch(datetime(2020, 1, 1, 12, 0, 5).timestamp(), 50, Color(1, 2, 3))


class TestBluetoothProximityHandler:
    class MockScanEntry:
        rssi = -30
        addr = "fa:ke:ad:dr"

    def test_in_range(self) -> None:
        mock = Mock()
        handler = BluetoothProximityHandler(mock.callback, -50)
        handler.handleDiscovery(self.MockScanEntry(), False, False)
        mock.callback.assert_called_once_with("fa:ke:ad:dr", -30)

    def test_not_in_range(self) -> None:
        mock = Mock()
        handler = BluetoothProximityHandler(mock.callback, -25)
        handler.handleDiscovery(self.MockScanEntry(), False, False)
        mock.callback.assert_not_called()
