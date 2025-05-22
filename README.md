# RootSignal-ESP32

A MicroPython-based WiFi security monitoring system for ESP32 that detects RF jamming, deauthentication attacks, and MAC flooding attempts.

## Features

- Real-time WiFi network scanning and analysis
- Detection of multiple security threats:
  - RF jamming (signal interference)
  - Deauthentication attacks
  - MAC flooding attempts
- Slack integration for instant alerts
- Configurable thresholds and scan intervals
- Local logging for debugging and analysis
- Memory-efficient implementation for ESP32

## Quickstart

1. **Hardware Requirements**
   - ESP32 development board
   - Micro USB cable
   - Power supply (if not using USB power)

2. **Software Requirements**
   - MicroPython firmware for ESP32
   - `ampy` or `rshell` for file transfer
   - Python 3.6+ for testing

3. **Installation**
   ```bash
   # Flash MicroPython to ESP32
   esptool.py --port /dev/ttyUSB0 erase_flash
   esptool.py --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-firmware.bin

   # Upload project files
   ampy --port /dev/ttyUSB0 put main.py
   ampy --port /dev/ttyUSB0 put utils.py
   ampy --port /dev/ttyUSB0 put wifi_scan.py
   ampy --port /dev/ttyUSB0 put config.json
   ```

4. **Configuration**
   Edit `config.json` with your settings:
   ```json
   {
       "slack_webhook": "https://hooks.slack.com/services/your/webhook/url",
       "system_name": "rootsignal-esp32",
       "signal_threshold": -80,
       "wifi_ssid": "YOUR_WIFI_SSID",
       "wifi_password": "YOUR_WIFI_PASSWORD",
       "scan_interval": 30,
       "mac_flood_threshold": 50,
       "deauth_threshold": 5,
       "signal_drop_threshold": 20,
       "log_level": "INFO"
   }
   ```

5. **Running**
   - The system will automatically start on boot
   - Monitor the serial console for status messages
   - Check Slack for security alerts

## Example Slack Alert

```
*RootSignal Alert:* `Possible Deauth Attack` from `rootsignal-esp32`
> SSID: Office-Network showing repeated signal drops
```

## Dependencies

- MicroPython 1.18+
- Required MicroPython modules:
  - `network`
  - `ujson`
  - `urequests`
  - `machine`
  - `time`

## Testing

Run the test suite:
```bash
python test_rootsignal.py
```

## Troubleshooting

### Common Issues

1. **ESP32 Not Detected**
   - Check USB connection
   - Install proper USB drivers
   - Try different USB cable

2. **WiFi Connection Issues**
   - Verify SSID and password in config.json
   - Check WiFi signal strength
   - Ensure 2.4GHz network (ESP32 doesn't support 5GHz)

3. **Memory Errors**
   - Reduce scan interval
   - Lower MAC flood threshold
   - Enable garbage collection

4. **Slack Integration Not Working**
   - Verify webhook URL
   - Check internet connectivity
   - Monitor log.txt for errors

### Debugging

1. **Serial Console**
   ```bash
   # Connect to serial console
   screen /dev/ttyUSB0 115200
   ```

2. **Log File**
   - Check `log.txt` for detailed error messages
   - Log level can be adjusted in config.json

3. **Memory Usage**
   ```python
   import gc
   gc.collect()
   print(gc.mem_free())
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- MicroPython community
- ESP32 community
- Slack API team 