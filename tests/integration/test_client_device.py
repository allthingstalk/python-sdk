import pytest
from unittest.mock import Mock, patch
import responses
import json
from allthingstalk import Client, Device, IntegerAsset, StringAsset


class TestClientDeviceIntegration:
    """Integration tests for Client-Device interactions"""

    @responses.activate
    def test_device_creation_and_connection_flow(self, mock_token, mock_device_id):
        """Test complete device creation and connection workflow"""
        # Mock HTTP responses
        responses.add(
            responses.GET,
            f"https://api.allthingstalk.io/device/{mock_device_id}/assets",
            json=[],
            status=200
        )

        responses.add(
            responses.POST,
            f"https://api.allthingstalk.io/device/{mock_device_id}/assets",
            json={
                'id': 'asset_123',
                'name': 'temperature',
                'title': 'Temperature',
                'description': '',
                'is': 'sensor',
                'profile': {'type': 'integer'},
                'deviceId': mock_device_id
            },
            status=200
        )

        with patch('paho.mqtt.client.Client') as mock_mqtt:
            mock_mqtt_instance = Mock()
            mock_mqtt.return_value = mock_mqtt_instance

            # Create device class
            class TemperatureDevice(Device):
                temperature = IntegerAsset()

            # Create client and device
            client = Client(mock_token)
            device = TemperatureDevice(client=client, id=mock_device_id)

            # Verify connection
            assert device._connected is True
            assert device.id == mock_device_id
            assert device.client == client

            # Verify MQTT subscription
            mock_mqtt_instance.subscribe.assert_called()

            # Verify asset creation
            assert len(responses.calls) == 2  # GET assets + POST create asset
            assert device.assets['temperature'].id == 'asset_123'

    @responses.activate
    def test_asset_state_publishing_and_retrieval(self, mock_token, mock_device_id):
        """Test asset state publishing and retrieval integration"""
        # Mock asset retrieval
        responses.add(
            responses.GET,
            f"https://api.allthingstalk.io/device/{mock_device_id}/assets",
            json=[{
                'id': 'temp_asset',
                'name': 'temperature',
                'title': 'Temperature',
                'description': '',
                'is': 'sensor',
                'profile': {'type': 'integer'},
                'deviceId': mock_device_id
            }],
            status=200
        )

        # Mock state retrieval
        responses.add(
            responses.GET,
            f"https://api.allthingstalk.io/device/{mock_device_id}/asset/temperature/state",
            json={'state': {'value': 23, 'at': '2023-09-19T12:00:00Z'}},
            status=200
        )

        # Mock state publishing
        responses.add(
            responses.PUT,
            f"https://api.allthingstalk.io/device/{mock_device_id}/asset/temperature/state",
            json={'success': True},
            status=200
        )

        with patch('paho.mqtt.client.Client'):
            class TemperatureDevice(Device):
                temperature = IntegerAsset()

            client = Client(mock_token)
            device = TemperatureDevice(client=client, id=mock_device_id)

            # Test state publishing
            device.temperature = 25

            # Test state retrieval
            state = device.temperature
            assert state.value == 23

            # Verify HTTP calls
            put_call = next(call for call in responses.calls if call.request.method == 'PUT')
            request_data = json.loads(put_call.request.body)
            assert request_data['value'] == 25

    def test_multiple_devices_same_client(self, mock_token):
        """Test multiple devices using the same client"""
        with patch('paho.mqtt.client.Client'):
            with patch('requests.get') as mock_get:
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.return_value = []

                with patch('requests.post') as mock_post:
                    mock_post.return_value.json.return_value = {
                        'id': 'asset_123',
                        'name': 'sensor',
                        'title': 'Sensor',
                        'description': '',
                        'is': 'sensor',
                        'profile': {'type': 'integer'},
                        'deviceId': 'device_a'
                    }

                    class DeviceA(Device):
                        sensor_a = IntegerAsset()

                    class DeviceB(Device):
                        sensor_b = IntegerAsset()

                    client = Client(mock_token)
                    device_a = DeviceA(client=client, id="device_a")
                    device_b = DeviceB(client=client, id="device_b")

                    # Both devices should be registered with client
                    assert "device_a" in client._devices
                    assert "device_b" in client._devices
                    assert client._devices["device_a"] == device_a
                    assert client._devices["device_b"] == device_b

    def test_device_message_handling_integration(self, mock_token, mock_device_id):
        """Test MQTT message handling integration"""
        with patch('paho.mqtt.client.Client') as mock_mqtt:
            mock_mqtt_instance = Mock()
            mock_mqtt.return_value = mock_mqtt_instance

            with patch('requests.get') as mock_get:
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.return_value = []

                with patch('requests.post') as mock_post:
                    mock_post.return_value.json.return_value = {
                        'id': 'counter_asset',
                        'name': 'counter',
                        'title': 'Counter',
                        'description': '',
                        'is': 'actuator',
                        'profile': {'type': 'integer'},
                        'deviceId': mock_device_id
                    }

                    # Track handler calls
                    handler_calls = []

                    class CounterDevice(Device):
                        counter = IntegerAsset()

                    client = Client(mock_token)
                    device = CounterDevice(client=client, id=mock_device_id)

                    # Define handler outside the class
                    @CounterDevice.command.counter
                    def handle_counter_command(device, value, at):
                        handler_calls.append((value, at))

                    # Simulate MQTT message reception
                    mock_message_payload = json.dumps({'value': 42}).encode('utf-8')
                    device._on_message('command', 'counter', mock_message_payload)

                    # Verify handler was called
                    assert len(handler_calls) == 1
                    assert handler_calls[0][0] == 42  # value

    @responses.activate
    def test_error_handling_integration(self, mock_token, mock_device_id):
        """Test error handling in integrated scenarios"""
        # Mock 403 forbidden response
        responses.add(
            responses.GET,
            f"https://api.allthingstalk.io/device/{mock_device_id}/assets",
            json={'error': 'Forbidden'},
            status=403
        )

        with patch('paho.mqtt.client.Client'):
            from allthingstalk.exceptions import AccessForbiddenException

            class TestDevice(Device):
                temperature = IntegerAsset()

            client = Client(mock_token)

            with pytest.raises(AccessForbiddenException):
                device = TestDevice(client=client, id=mock_device_id)


class TestDeviceLifecycle:
    """Test complete device lifecycle scenarios"""

    @responses.activate
    def test_complete_device_lifecycle(self, mock_token, mock_device_id):
        """Test a complete device lifecycle from creation to operation"""
        # Setup HTTP mocks for the complete lifecycle
        responses.add(
            responses.GET,
            f"https://api.allthingstalk.io/device/{mock_device_id}/assets",
            json=[],
            status=200
        )

        responses.add(
            responses.POST,
            f"https://api.allthingstalk.io/device/{mock_device_id}/assets",
            json={
                'id': 'temp_asset',
                'name': 'temperature',
                'title': 'Temperature',
                'description': 'Temperature sensor',
                'is': 'sensor',
                'profile': {'type': 'number'},
                'deviceId': mock_device_id
            },
            status=200
        )

        responses.add(
            responses.POST,
            f"https://api.allthingstalk.io/device/{mock_device_id}/assets",
            json={
                'id': 'status_asset',
                'name': 'status',
                'title': 'Status',
                'description': 'Device status',
                'is': 'sensor',
                'profile': {'type': 'string'},
                'deviceId': mock_device_id
            },
            status=200
        )

        responses.add(
            responses.PUT,
            f"https://api.allthingstalk.io/device/{mock_device_id}/asset/temperature/state",
            json={'success': True},
            status=200
        )

        responses.add(
            responses.PUT,
            f"https://api.allthingstalk.io/device/{mock_device_id}/asset/status/state",
            json={'success': True},
            status=200
        )

        with patch('paho.mqtt.client.Client'):
            class SensorDevice(Device):
                temperature = IntegerAsset(description="Temperature sensor")
                status = StringAsset(description="Device status")

            # 1. Create client
            client = Client(mock_token)
            assert client.token == mock_token

            # 2. Create and connect device
            device = SensorDevice(client=client, id=mock_device_id)
            assert device._connected is True

            # 3. Verify assets were created
            assert len(device.assets) == 2
            assert device.assets['temperature'].id == 'temp_asset'
            assert device.assets['status'].id == 'status_asset'

            # 4. Publish some states
            device.temperature = 23.5
            device.status = "operational"

            # 5. Verify HTTP calls were made
            assert len(responses.calls) == 5  # GET + 2 POST + 2 PUT (updated expectation)

            # Verify the PUT calls had correct data
            put_calls = [call for call in responses.calls if call.request.method == 'PUT']
            temp_call = next(call for call in put_calls if 'temperature' in call.request.url)
            status_call = next(call for call in put_calls if 'status' in call.request.url)

            temp_data = json.loads(temp_call.request.body)
            status_data = json.loads(status_call.request.body)

            assert temp_data['value'] == 23.5
            assert status_data['value'] == "operational"
