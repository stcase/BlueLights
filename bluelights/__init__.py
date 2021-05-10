def main():
    scanner = Scanner()
    test_callback = lambda a, b, c: None
    tracker = BluetoothTracker(test_callback, -80, -50, timedelta(seconds=3))
    scanner.withDelegate(tracker)
    devices = scanner.scan(60, passive=True)
    for dev in devices:
        print(f"Device {dev.addr} @ strength {dev.rssi}")


if __name__ == "__main__":
    main()