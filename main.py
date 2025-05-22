# main.py
import time
import wifi_scan
import utils

config = utils.load_config()

utils.connect_to_wifi()

while True:
    nets = wifi_scan.scan_networks()
    anomalies = wifi_scan.detect_anomalies(nets, config['signal_threshold'])
    for anomaly in anomalies:
        utils.send_slack_alert(config['slack_webhook'], config['system_name'], anomaly)
    time.sleep(30)
