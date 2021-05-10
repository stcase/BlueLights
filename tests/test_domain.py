from datetime import datetime

from bluelights.domain import Color, LightSwitch

class TestLightSwitch:
    def test_equal(self) -> None:
        now = datetime.now().timestamp()
        assert LightSwitch(now, 50, Color(1, 2, 3)) == LightSwitch(now, 50, Color(1, 2, 3))

    def test_not_equal(self) -> None:
        now = datetime.now().timestamp()
        assert LightSwitch(now, 49, Color(1, 2, 3)) != LightSwitch(now, 50, Color(1, 2, 3))

class TestColor:
    def test_equal(self) -> None:
        assert Color(1, 2, 3) == Color(1, 2, 3)

    def test_not_equal(self) -> None:
        assert Color(1, 2, 3) != Color(1, 2, 4)
