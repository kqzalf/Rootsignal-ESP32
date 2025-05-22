"""Utility functions for RootSignal-ESP32.

This module provides core functionality for configuration management,
WiFi connectivity, and Slack alert integration.
"""
import gc
import time
import network
import ujson
import urequests
from machine import Pin  # noqa: F401

CONFIG_FILE = 'config.json'
LOG_FILE = 'log.txt'

def log_error(error_msg: str) -> None:
    """Log an error message to the log file with timestamp.
    
    Args:
        error_msg: The error message to log
    """
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            timestamp = time.localtime()
            f.write(f"[{timestamp[0]}-{timestamp[1]}-{timestamp[2]} "
                   f"{timestamp[3]}:{timestamp[4]}:{timestamp[5]}] {error_msg}\n")
    except Exception as e:
        print(f"Failed to write to log: {error_msg} - {str(e)}")

def load_config() -> dict:
    """Load configuration from config.json file.
    
    Returns:
        dict: Configuration dictionary
        
    Raises:
        Exception: If config file cannot be loaded or parsed
    """
    try:
        with open(CONFIG_FILE, encoding='utf-8') as f:
            config = ujson.load(f)
            gc.collect()  # Clean up after file operations
            return config
    except Exception as e:
        error_msg = f"Config load error: {str(e)}"
        log_error(error_msg)
        raise

def connect_to_wifi() -> None:
    """Connect to WiFi network using credentials from config.
    
    Raises:
        Exception: If WiFi connection fails or times out
    """
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
                raise ConnectionError("WiFi connection timeout")
            print('Network config:', sta_if.ifconfig())
        except Exception as e:
            error_msg = f"WiFi connection error: {str(e)}"
            log_error(error_msg)
            raise

def send_slack_alert(webhook_url: str, node: str, anomaly: dict) -> None:
    """Send an alert to Slack about a detected anomaly.
    
    Args:
        webhook_url: Slack webhook URL
        node: Name of the monitoring node
        anomaly: Dictionary containing anomaly details
        
    Raises:
        Exception: If Slack API request fails
    """
    try:
        message = {
            'text': f'*RootSignal Alert:* `{anomaly["type"]}` from `{node}`\n> {anomaly["details"]}'
        }
        response = urequests.post(webhook_url, json=message)
        if response.status_code != 200:
            raise ConnectionError(f"Slack API error: {response.status_code}")
        response.close()
        gc.collect()  # Clean up after network request
    except Exception as e:
        error_msg = f"Slack alert error: {str(e)}"
        log_error(error_msg)
        raise
