# main.py
"""Main entry point for RootSignal-ESP32.

This module initializes the WiFi security monitoring system and runs the main
monitoring loop that scans for networks and detects anomalies.
"""
import time
import gc
import machine
import wifi_scan
import utils

def main() -> None:
    """Run the main monitoring loop.
    
    This function:
    1. Loads configuration
    2. Connects to WiFi
    3. Continuously scans for networks and anomalies
    4. Sends alerts when anomalies are detected
    """
    try:
        # Load configuration
        config = utils.load_config()
        
        # Connect to WiFi
        utils.connect_to_wifi()
        
        # Main monitoring loop
        while True:
            try:
                # Scan for networks
                nets = wifi_scan.scan_networks()
                if not nets:
                    print("No networks found in scan")
                    time.sleep(5)
                    continue
                
                # Detect anomalies
                anomalies = wifi_scan.detect_anomalies(nets, config['signal_threshold'])
                
                # Send alerts for any anomalies
                for anomaly in anomalies:
                    try:
                        utils.send_slack_alert(
                            config['slack_webhook'],
                            config['system_name'],
                            anomaly
                        )
                    except ConnectionError as e:
                        print(f"Failed to send alert: {e}")
                
                # Memory cleanup
                gc.collect()
                
                # Sleep until next scan
                time.sleep(config.get('scan_interval', 30))
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(5)  # Wait before retrying
                
    except Exception as e:
        print(f"Fatal error: {e}")
        # If we hit a fatal error, wait a bit and reset
        time.sleep(10)
        machine.reset()

if __name__ == '__main__':
    main()
