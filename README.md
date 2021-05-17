![Workflow Status](https://github.com/stcase/BlueLights/actions/workflows/run-tests.yml/badge.svg)

# BlueLights
Automatic lights controlled by Bluetooth proximity detection.

These are lights using the Tuya platform that will change colors or turn on/off based on the presence of a Bluetooth
device, like your phone or smartwatch. When you walk into a room with them, watch them automatically turn on, and
automatically turn off when you leave. No need to pair devices, it will react to any Bluetooth broadcast. All signalling
is done over the Wi-Fi network.

This is primarily designed with [LED strips](https://www.action.com/nl-nl/p/lsc-smart-connect-ledstrip/) in mind, but
works with any Tuya "bulb" device.

## Installation

### Hardware Requirements
1. A [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) or similar board with Wi-Fi and Bluetooth.
2. A microSD card compatible with the Pi Zero.
3. A micro-USB cable and power supply compatible with the Pi Zero.
4. A Tuya bulb device, such as the [LSC Smart Connect ledstrip](https://www.action.com/nl-nl/p/lsc-smart-connect-ledstrip/).
5. A Wi-Fi network, and a second computer to use for installation.

### Setting up the Raspberry Pi

This is assuming we're using a Raspberry Pi Zero W with Raspberry Pi OS version 10 (buster).

We'll be setting up the Pi with a headless installation of Raspberry Pi OS.
It should save memory and drive space or something, but it's mostly because I don't have a spare keyboard and monitor.
1. Install Raspberry Pi OS on the microSD card using the [Raspberry Pi Imager](https://www.raspberrypi.org/software/).
2. Mount the microSD card on your computer.
3. [Configure it to automatically connect to your Wi-Fi network](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md).
4. [Enable SSH on a headless Raspberry Pi (item 3)](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md).
5. Unmount the microSD card, put it in the Pi, plug the pi into micro-USB, and wait for a few minutes to power up.
6. Find the IP address of the Pi on your router.
7. Connect to it from a command line with `ssh pi@<IP here>`. Password: `raspberry`.
8. Change the password with `passwd`
9. Update the OS: `sudo apt-get update` and `sudo apt-get upgrade`.
10. Set the timezone and other settings with `sudo raspi-config`.
11. Install git for source code management: `sudo apt-get install git`.
12. Install other necessary packages: `sudo apt-get install python3-distutils libglib2.0-dev`.
12. Install [poetry](https://python-poetry.org/docs/#installation) for Python package management. You will probably need
to log out and back in after this command.

### Setting up the Tuya device

The following will require setting up a Tuya development account, and may require that you submit a ticket for your
account. To set up the Tuya device, follow the instructions for linking your devices either
[without the smartphone app](https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md) or
[with the smartphone app](https://github.com/jasonacox/tinytuya). After these instructions you should have the device
IP Address, Local Key, Version, and Device ID to be used in `config.py` below.



### Setting up the BlueLights software

1. If you aren't already connect to the Pi: `ssh pi@<IP here>`.
2. Pick a directory to install the code, like `cd ~`.
3. Get the source code with `git clone https://github.com/stcase/BlueLights.git`.
4. `cd BlueLights`
5. Install the necessary Python packages with `poetry install --no-dev`.
6. Create the file config.py with `nano config.py` and populate it with the Tuya device data like below.

config.py:
```
local_key = '<Local Key>'
bulb = {"id": '<Tuya Device ID>', "ip": '<IP address of Tuya device>', "version": <device version 3.1 or 3.3>}

```
7. Run the program with `sudo /home/pi/BlueLights/.venv/bin/python main.py`
