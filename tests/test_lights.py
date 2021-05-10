from datetime import datetime
from queue import Queue

from freezegun import freeze_time

from bluelights.domain import Color, LightSwitch
from bluelights.lights import LightController


class TestLightController:
    def test_receive_switches(self) -> None:
        q: Queue[LightSwitch] = Queue()
        lc = LightController(q, [])
        c = Color(1, 2, 3)
        exp = 0
        q.put(LightSwitch(exp, 40, c))
        q.put(LightSwitch(exp, 41, c))
        q.put(LightSwitch(exp, 42, c))
        lc.receive_switches()
        assert len(lc._switches) == 3

    def test_receive_switches_empty(self) -> None:
        lc = LightController(Queue(), [])
        lc.receive_switches()
        assert len(lc._switches) == 0

    @freeze_time("2020-01-01 12:00:02")
    def remove_expired(self) -> None:
        lc = LightController(Queue(), [])
        c = Color(1, 2, 3)
        exp = datetime.now().timestamp()
        lc._switches = [LightSwitch(exp, 40, c), LightSwitch(exp - 1, 50, c), LightSwitch(exp - 2, 40, c),
                        LightSwitch(exp + 3, 40, c), LightSwitch(exp - 10000, 40, c)]
        assert len(lc._switches) == 2

    def get_highest_priority(self) -> None:
        lc = LightController(Queue(), [])
        c = Color(1, 2, 3)
        exp = 0
        lc._switches = [LightSwitch(exp, 40, c), LightSwitch(exp + 1, 50, c), LightSwitch(exp + 2, 40, c), LightSwitch(exp + 3, 40, c)]
        assert lc.get_highest_priority() == LightSwitch(exp + 1, 50, c)

    def get_highest_priority_none(self) -> None:
        lc = LightController(Queue(), [])
        assert lc.get_highest_priority() is None
