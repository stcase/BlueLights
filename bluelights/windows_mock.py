"""
Because bluepy only works on Linux/raspberry pi, this provides stubs to allow for testing and development on windows
"""


class Scanner:
    def __init__(self) -> None:
        pass

    def withDelegate(self) -> None:
        pass

    def scan(self, *args, **kwargs) -> None:
        pass


class DefaultDelegate:
    pass


class ScanEntry:
    def __init__(self, addr: str, rssi: str):
        self.addr = addr
        self.rssi = rssi
