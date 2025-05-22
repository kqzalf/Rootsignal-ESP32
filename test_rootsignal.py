# test_rootsignal.py
import unittest
from unittest.mock import patch, MagicMock
import ujson
import utils
import wifi_scan

class TestRootSignal(unittest.TestCase):
    def setUp(self):
        # Mock config data
        self.mock_config = {
            'slack_webhook': 'https://hooks.slack.com/test',
            'system_name': 'test-node',
            'signal_threshold': -80,
            'wifi_ssid': 'test-ssid',
            'wifi_password': 'test-password'
        }
        
        # Mock network scan data
        self.mock_networks = [
            (b'TestSSID1', b'\x00\x11\x22\x33\x44\x55', 1, -50, 0, 0),
            (b'TestSSID2', b'\x66\x77\x88\x99\xaa\xbb', 6, -90, 0, 0)
        ]

    @patch('builtins.open')
    def test_load_config(self, mock_open):
        mock_open.return_value.__enter__.return_value.read.return_value = ujson.dumps(self.mock_config)
        config = utils.load_config()
        self.assertEqual(config, self.mock_config)

    @patch('urequests.post')
    def test_send_slack_alert(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        anomaly = {
            'type': 'Test Alert',
            'details': 'Test details'
        }
        
        utils.send_slack_alert(self.mock_config['slack_webhook'], 
                             self.mock_config['system_name'], 
                             anomaly)
        
        mock_post.assert_called_once()

    def test_detect_anomalies(self):
        # Test weak signal detection
        anomalies = wifi_scan.detect_anomalies(self.mock_networks, -80)
        self.assertTrue(any(a['type'] == 'Weak Signal Detected' for a in anomalies))
        
        # Test MAC flood detection
        many_networks = self.mock_networks * 30  # Create 60 networks
        anomalies = wifi_scan.detect_anomalies(many_networks, -80)
        self.assertTrue(any(a['type'] == 'Possible MAC Flood' for a in anomalies))

    @patch('network.WLAN')
    def test_scan_networks(self, mock_wlan):
        mock_wlan.return_value.scan.return_value = self.mock_networks
        networks = wifi_scan.scan_networks()
        self.assertEqual(len(networks), 2)
        self.assertEqual(networks[0][0], b'TestSSID1')

if __name__ == '__main__':
    unittest.main() 