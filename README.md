# USB Temperature And Humidity Data Logger

This is a simple python script to read data from a USB Temperature And Humidity Data Logger.

After connecting the device we see:
```
$ lsusb
...
Bus 003 Device 029: ID 1941:8021 Dream Link WH1080 Weather Station / USB Missile Launcher
...
```

## Installation

The requirements are:

- Python 3
- pyusb (`pip install pyusb`)

If you get permissions error, you can add a `udev` rule to allow access to the device:

```bash
sudo nano /etc/udev/rules.d/99-weather-station.rules
```

Add the Rule:

```
SUBSYSTEM=="usb", ATTR{idVendor}=="1941", ATTR{idProduct}=="8021", MODE="0666", GROUP="plugdev", SYMLINK+="weather_station"
```

Make sure that your user is in the `plugdev` group. (`gpasswd -a $USER plugdev`)

Reload `udev` Rules:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Usage

```bash
$ python3 weather.py
```

## Device information

### Device names

The device is sold under different names:
- Datalogger DS100 USB
- Kongin USB Temperature And Humidity Data Logger
- KG100 Data Logger
- FreeTec USB Data Logger v1
- OTGENKG100BLK-0004728
- T113

### Specifications

- Memory: Max 16,320 temperature and relative humidity readings
- Logging Interval: 60 seconds to 4 hours
- Measure Temperature Range: -40 °Celsius to 60 °Celsius
- Temperature accuracy: /-1.0 °Celsius under 0-50 °Celsius
- Measure humidity range: 10%-99%RH
- Humidity accuracy: /-4% under 20%-80%

## Acknowledgements

The script is based on the following repository:

https://github.com/shaneHowearth/Dream-Link-WH1080-Weather-Station