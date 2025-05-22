# utils.py
import network
import ujson
import urequests

CONFIG_FILE = 'config.json'


def load_config():
    with open(CONFIG_FILE) as f:
        return ujson.load(f)

def connect_to_wifi():
    import time
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.connect('YOUR_WIFI_SSID', 'YOUR_WIFI_PASSWORD')
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())

def send_slack_alert(webhook_url, node, anomaly):
    try:
        message = {
            'text': '*RootSignal Alert:* `%s` from `%s`\n> %s' % (anomaly['type'], node, anomaly['details'])
        }
        urequests.post(webhook_url, json=message)
    except Exception as e:
        print('Slack error:', e)
