# wifi_scan.py
import network
from time import localtime


def scan_networks():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        sta_if.active(True)
    nets = sta_if.scan()
    return nets

def detect_anomalies(networks, threshold):
    anomalies = []
    if len(networks) > 50:
        anomalies.append({
            'type': 'Possible MAC Flood',
            'details': 'Detected %d networks in range.' % len(networks)
        })
    for net in networks:
        ssid = net[0].decode()
        rssi = net[3]
        if rssi < threshold:
            anomalies.append({
                'type': 'Weak Signal Detected',
                'details': 'SSID: %s, RSSI: %d dBm' % (ssid, rssi)
            })
    return anomalies
