from datetime import datetime

from freezegun import freeze_time

from bluelights.domain import Color, LightSwitch


class TestLightSwitch:
    def test_equal(self) -> None:
        now = datetime.now().timestamp()
        assert LightSwitch(now, 50, Color(1, 2, 3)) == LightSwitch(now, 50, Color(1, 2, 3))

    def test_not_equal(self) -> None:
        now = datetime.now().timestamp()
        assert LightSwitch(now, 49, Color(1, 2, 3)) != LightSwitch(now, 50, Color(1, 2, 3))

    @freeze_time("2020-01-01 12:00:02")
    def test_expired(self) -> None:
        assert LightSwitch(datetime.now().timestamp() - 1, 42, Color(1, 2, 3)).expired()

    @freeze_time("2020-01-01 12:00:02")
    def test_not_expired(self) -> None:
        assert not LightSwitch(datetime.now().timestamp() + 1, 42, Color(1, 2, 3)).expired()


class TestColor:
    def test_equal(self) -> None:
        assert Color(1, 2, 3) == Color(1, 2, 3)

    def test_not_equal(self) -> None:
        assert Color(1, 2, 3) != Color(1, 2, 4)
