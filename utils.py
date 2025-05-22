# utils.py
import network
import ujson
import urequests
import gc
import time
from machine import Pin

CONFIG_FILE = 'config.json'
LOG_FILE = 'log.txt'

def log_error(error_msg):
    try:
        with open(LOG_FILE, 'a') as f:
            timestamp = time.localtime()
            f.write(f"[{timestamp[0]}-{timestamp[1]}-{timestamp[2]} {timestamp[3]}:{timestamp[4]}:{timestamp[5]}] {error_msg}\n")
    except:
        print(f"Failed to write to log: {error_msg}")

def load_config():
    try:
        with open(CONFIG_FILE) as f:
            config = ujson.load(f)
            gc.collect()  # Clean up after file operations
            return config
    except Exception as e:
        error_msg = f"Config load error: {str(e)}"
        log_error(error_msg)
        raise

def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to network...')
        try:
            config = load_config()
            sta_if.connect(config['wifi_ssid'], config['wifi_password'])
            timeout = 0
            while not sta_if.isconnected() and timeout < 20:
                time.sleep(1)
                timeout += 1
            if not sta_if.isconnected():
                raise Exception("WiFi connection timeout")
            print('Network config:', sta_if.ifconfig())
        except Exception as e:
            error_msg = f"WiFi connection error: {str(e)}"
            log_error(error_msg)
            raise

def send_slack_alert(webhook_url, node, anomaly):
    try:
        message = {
            'text': '*RootSignal Alert:* `%s` from `%s`\n> %s' % (anomaly['type'], node, anomaly['details'])
        }
        response = urequests.post(webhook_url, json=message)
        if response.status_code != 200:
            raise Exception(f"Slack API error: {response.status_code}")
        response.close()
        gc.collect()  # Clean up after network request
    except Exception as e:
        error_msg = f"Slack alert error: {str(e)}"
        log_error(error_msg)
        raise
