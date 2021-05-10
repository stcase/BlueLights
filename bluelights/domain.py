from datetime import datetime
from typing import Any


class Color:
    """
    A color that the lights can be set to. Not all tuya lights support all color profiles (for example a white warmth
    vs RGB control).
    See https://github.com/jasonacox/tinytuya for more details.

    Args:
        r, g, b: RGB values: 0-255.
    """
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Color):
            return self.r == other.r and self.g == other.g and self.b == other.b
        return False


class LightSwitch:
    """
    Messages to control the lights by communicating what activity they should perform and for how long.

    Args:
        expiry: A POSIX timestamp representing when the message is no longer valid.
        priority: Priority relative to related methods. The high the number, the higher the priority.
        color: color this message is asking the lights to perform
    """
    def __init__(self, expiry: float, priority: int, color: Color):
        self.expiry = expiry
        self.priority = priority
        self.color = color

    def expired(self) -> bool:
        """
        Returns:
            Whether the expiry time has passed for the Light Switch
        """
        return self.expiry < datetime.now().timestamp()

    def __str__(self) -> str:
        return f"{self.color} @ P{self.priority} until {self.expiry}"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, LightSwitch):
            return self.expiry == other.expiry and self.priority == other.priority and self.color == other.color
        return False
