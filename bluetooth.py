from bluepy.btle import DefaultDelegate, Scanner


class ScanDelegate(DefaultDelegate):
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print(f"Discovered device {dev.addr}")
        elif isNewData:
            print(f"Received new data from {dev.addr}")


def main():
    scanner = Scanner()
    scanner.withDelegate(ScanDelegate())
    scanner.scan(30)

    
if __name__ == "__main__":
    main()
