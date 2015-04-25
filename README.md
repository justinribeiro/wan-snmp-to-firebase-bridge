# SNMP to Firebase

This script reads SNMP data from a network interface and pushes that data to a Firebase endpoint.

## Why?

Little something something to wire up to my [bandwidth-gauge Polymer element](https://github.com/justinribeiro/bandwidth-gauge) for [GDG Oakdale's Firebase Code Day](http://www.meetup.com/GDG-Oakdale/events/220949519/).

## Dependencies

1. [Snimpy](https://snimpy.readthedocs.org/en/latest/)
2. [firebase-python](https://pypi.python.org/pypi/python-firebase/1.2)

## Setup

This will vary based on your platform, but I'll outline the steps that worked for me on Ubuntu 14.04 LTS:

1. Install libffi-dev
```
sudo apt-get libffi-dev
```
2. Install libsmi-dev
```
sudo apt-get install libsmi2-dev
```
3. You'll need at least the base mibs for snmp, so we need to install the downloader tool, snmp-mibs-downloader:
```
sudo apt-get install snmp-mibs-downloader
```
4. Download the mibs by running:
```
sudo download-mibs
```
5. Install snimpy:
```
pip install snimpy
```
6. Install firebase-python:
```
pip install firebase-python
```
7. Edit the `wan-snmp-to-firebase.py` paths in the file:
```
# Our Firebase application
_FIREBASE_ENDPOINT = "https://[YOUR_APP_HERE].firebaseio.com/"

# Our WAN SNMP settings
_WAN_HOST = "[SOME_IP_ADDRESS_OR_ADDRESS]"
_WAN_COMMUNITY = "public"
_WAN_SNMP_VERSION = 2

# We only want to watch one adapter, so we set the target
# You can find this by parsing ifDescr:
# snmpwalk -v 2 -c public target ifDescr
_WAN_ADAPTER = 5
```
8. Run via `python wan-snmp-to-firebase.py`
9. Check Firebase to verify the data (you can append `.json` to an endpoint record to get JSON):
```
{
    "calc": {
        "calc_bits_ifInOctets": {
            "speed": "407.01",
            "unit": "Kbps"
        },
        "calc_bits_ifOutOctets": {
            "speed": "73.8",
            "unit": "Kbps"
        },
        "calc_bytes_ifInOctets": {
            "speed": "49.68",
            "unit": "KB/s"
        },
        "calc_bytes_ifOutOctets": {
            "speed": "9.01",
            "unit": "KB/s"
        }
    },
    "raw": {
        "ifInOctets": 2048839370,
        "ifOutOctets": 148367494,
        "timestamp": 1429980758.285195
    }
}
```