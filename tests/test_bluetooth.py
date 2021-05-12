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


@freeze_time("2020-01-01 12:00:02")
class TestBluetoothProximityHandler:
    class MockScanEntry:
        rssi = -30
        addr = "fa:ke:ad:dr"

    def test_callback_called(self) -> None:
        mock = Mock()
        handler = BluetoothProximityHandler(mock.callback, -50)
        handler._seen_devices[self.MockScanEntry.addr] = [0, 0]
        handler.handleDiscovery(self.MockScanEntry(), False, False)
        mock.callback.assert_called_once_with("fa:ke:ad:dr", -30)

    def test_callback_not_called(self) -> None:
        mock = Mock()
        handler = BluetoothProximityHandler(mock.callback, -25)
        time = datetime.now().timestamp()
        handler._seen_devices[self.MockScanEntry.addr] = [time, time]
        handler.handleDiscovery(self.MockScanEntry(), False, False)
        mock.callback.assert_not_called()

    def test_passes_threshold_addr_added(self) -> None:
        mock = Mock()
        handler = BluetoothProximityHandler(mock.callback, -40)
        now = datetime.now().timestamp()
        assert not handler._passes_threshold(self.MockScanEntry())
        assert handler._seen_devices == {self.MockScanEntry.addr: [now, now]}

    def test_passes_threshold_removes_old(self) -> None:
        old_addr = "ol:dd:ad:dr"
        new_addr = "ne:ww:ad:dr"
        mock = Mock()
        handler = BluetoothProximityHandler(mock.callback, -25)
        now = datetime.now().timestamp()
        handler._seen_devices = {old_addr: [0, 0], new_addr: [now, now]}
        handler._passes_threshold(self.MockScanEntry())
        assert new_addr in handler._seen_devices
        assert old_addr not in handler._seen_devices
