# wifi_scan.py
import network
import time
import gc
from collections import defaultdict

# Constants for anomaly detection
MAC_FLOOD_THRESHOLD = 50
DEAUTH_THRESHOLD = 5  # Number of deauth frames in a short time
SCAN_INTERVAL = 30  # seconds

# Store previous scan results for comparison
previous_networks = {}
deauth_counter = defaultdict(int)
last_scan_time = 0

def scan_networks():
    global last_scan_time
    current_time = time.time()
    
    # Ensure minimum scan interval
    if current_time - last_scan_time < 5:  # Minimum 5 seconds between scans
        time.sleep(5)
    
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        sta_if.active(True)
    
    try:
        nets = sta_if.scan()
        last_scan_time = current_time
        gc.collect()  # Clean up after scan
        return nets
    except Exception as e:
        print(f"Scan error: {e}")
        return []

def detect_anomalies(networks, threshold):
    global previous_networks, deauth_counter
    anomalies = []
    current_networks = {}
    
    # Check for MAC flooding
    if len(networks) > MAC_FLOOD_THRESHOLD:
        anomalies.append({
            'type': 'Possible MAC Flood',
            'details': f'Detected {len(networks)} networks in range (threshold: {MAC_FLOOD_THRESHOLD})'
        })
    
    # Analyze each network
    for net in networks:
        try:
            ssid = net[0].decode() if net[0] else "Hidden SSID"
            bssid = ':'.join(['%02x' % b for b in net[1]])
            rssi = net[3]
            
            current_networks[bssid] = {
                'ssid': ssid,
                'rssi': rssi,
                'channel': net[2]
            }
            
            # Check for weak signals
            if rssi < threshold:
                anomalies.append({
                    'type': 'Weak Signal Detected',
                    'details': f'SSID: {ssid}, RSSI: {rssi} dBm, Channel: {net[2]}'
                })
            
            # Check for sudden signal drops (possible deauth)
            if bssid in previous_networks:
                prev_rssi = previous_networks[bssid]['rssi']
                if rssi < prev_rssi - 20:  # 20dB drop
                    deauth_counter[bssid] += 1
                    if deauth_counter[bssid] >= DEAUTH_THRESHOLD:
                        anomalies.append({
                            'type': 'Possible Deauth Attack',
                            'details': f'SSID: {ssid} showing repeated signal drops'
                        })
                else:
                    deauth_counter[bssid] = max(0, deauth_counter[bssid] - 1)
        
        except Exception as e:
            print(f"Error processing network: {e}")
            continue
    
    # Update previous networks
    previous_networks = current_networks
    
    # Clean up old deauth counters
    current_bssids = set(current_networks.keys())
    deauth_counter = {k: v for k, v in deauth_counter.items() if k in current_bssids}
    
    gc.collect()  # Clean up after processing
    return anomalies
