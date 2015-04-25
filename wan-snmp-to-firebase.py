import time
import json
from snimpy.manager import Manager as M
from snimpy.manager import load
from firebase import firebase

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

def octetsToBytesSpeed(input):
    if input < 1048576:
            speed = str(round((input / 10.24) / 100, 2))
            unit = "KB/s"
            return {'speed': speed, 'unit': unit}
    if input < 1073741824:
            speed = str(round((input / 10485.76) / 100, 2))
            unit = "MB/s"
            return {'speed': speed, 'unit': unit}
    if input > 1073741824:
            speed = str(round((input / 10737418.24) / 100, 2))
            unit = "GB/s"
            return {'speed': speed, 'unit': unit}

def octetsToBitsSpeed(input):
    if input < 125000:
            speed = str(round(input / 125, 2))
            unit = "Kbps"
            return {'speed': speed, 'unit': unit}
    if input < 125000000:
            speed = str(round((input / 1250) / 100, 2))
            unit = "Mbps"
            return {'speed': speed, 'unit': unit}
    if input > 125000000:
            speed = str(round((speed / 1250000) / 100, 2))
            unit = "Gbps"
            return {'speed': speed, 'unit': unit}

# Wire Firebase
firebaseConnection = firebase.FirebaseApplication(_FIREBASE_ENDPOINT, None)

# Load SNMP MIB
load("IF-MIB")

# SNMP Manager (our client)
m = M(_WAN_HOST, _WAN_COMMUNITY, _WAN_SNMP_VERSION)

last_ifOutOctets = 0
last_ifInOctets = 0
last_timestamp = time.time()

while True:
    # The first time the script runs, we have no change to send
    if last_ifOutOctets == 0:
        last_ifOutOctets = m.ifOutOctets[_WAN_ADAPTER]
        last_ifInOctets = m.ifInOctets[_WAN_ADAPTER]
        last_timestamp = time.time()
    else:
        holder_timestamp = time.time()

        diff_timestamp  = holder_timestamp - last_timestamp;
        diff_ifInOctets  = m.ifInOctets[_WAN_ADAPTER] - last_ifInOctets;
        diff_ifOutOctets = m.ifOutOctets[_WAN_ADAPTER] - last_ifOutOctets;
    
        split_ifOutOctets = diff_ifOutOctets / diff_timestamp
        split_ifInOctets = diff_ifInOctets / diff_timestamp

        calc_bytes_ifOutOctets = octetsToBytesSpeed(split_ifOutOctets)
        calc_bits_ifOutOctets = octetsToBitsSpeed(split_ifOutOctets)

        calc_bytes_ifInOctets = octetsToBytesSpeed(split_ifInOctets)
        calc_bits_ifInOctets = octetsToBitsSpeed(split_ifInOctets)

        last_ifOutOctets = m.ifOutOctets[_WAN_ADAPTER]
        last_ifInOctets = m.ifInOctets[_WAN_ADAPTER]
        last_timestamp = holder_timestamp
    
        result = {
            'raw': {
                'ifOutOctets': m.ifOutOctets[_WAN_ADAPTER],
                'ifInOctets': m.ifInOctets[_WAN_ADAPTER],
                'timestamp': holder_timestamp
            },
            'calc': {
                'calc_bytes_ifOutOctets': calc_bytes_ifOutOctets,
                'calc_bits_ifOutOctets': calc_bits_ifOutOctets,
                'calc_bytes_ifInOctets': calc_bytes_ifInOctets,
                'calc_bits_ifInOctets': calc_bits_ifInOctets
            }
        }

        result = firebaseConnection.post('/em4', result)
        print result

    time.sleep(1)