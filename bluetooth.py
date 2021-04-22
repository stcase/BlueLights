from bluepy.btle import DefaultDelegate, Scanner


class ScanDelegate(DefaultDelegate):
    def handleDiscovery(self, dev, isNewDev, isNewData):
        print(f"Discovered device {dev.addr}, strength: {dev.rssi}")


def main():
    scanner = Scanner()
    scanner.withDelegate(ScanDelegate())
    devices = scanner.scan(10, passive=False)
    for dev in devices:
        print(f"Device {dev.addr} @ strength {dev.rssi}")

    
if __name__ == "__main__":
    main()
