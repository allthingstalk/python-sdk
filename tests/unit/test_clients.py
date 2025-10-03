import pytest
from unittest.mock import Mock, patch
from allthingstalk import Client, BaseClient, AssetState
from allthingstalk.exceptions import AccessForbiddenException, AssetStateRetrievalException


class TestBaseClient:
    """Test cases for BaseClient abstract class"""

    def test_base_client_abstract_methods(self):
        """Test that BaseClient methods raise NotImplementedError"""
        client = BaseClient()

        with pytest.raises(NotImplementedError):
            client.get_assets("device_id")

        with pytest.raises(NotImplementedError):
            client.create_asset("device_id", Mock())

        with pytest.raises(NotImplementedError):
            client.get_asset_state("device_id", "asset_name")

        with pytest.raises(NotImplementedError):
            client.publish_asset_state("device_id", "asset_name", "value")

    def test_attach_device_does_nothing(self):
        """Test that _attach_device does nothing in base class"""
        client = BaseClient()
        result = client._attach_device(Mock())
        assert result is None


class TestClient:
    """Test cases for Client class"""

    def test_client_initialization_default(self, mock_token):
        """Test Client initialization with default parameters"""
        with patch('paho.mqtt.client.Client') as mock_mqtt_client:
            mock_mqtt_instance = Mock()
            mock_mqtt_client.return_value = mock_mqtt_instance

            client = Client(mock_token)

            assert client.token == mock_token
            assert client.http == "https://api.allthingstalk.io"
            # Verify MQTT client was created and methods were called
            mock_mqtt_client.assert_called_once()
            mock_mqtt_instance.username_pw_set.assert_called_once_with(mock_token, mock_token)
            mock_mqtt_instance.connect.assert_called_once()
            mock_mqtt_instance.loop_start.assert_called_once()

    def test_client_initialization_custom_endpoints(self, mock_token):
        """Test Client initialization with custom endpoints"""
        with patch('paho.mqtt.client.Client') as mock_mqtt_client:
            mock_mqtt_client.return_value = Mock()

            client = Client(
                mock_token,
                api="custom.allthingstalk.com",
                http="https://custom-http.com",
                mqtt="custom-mqtt.com:8883"
            )

            assert client.token == mock_token
            assert client.http == "https://custom-http.com"

    def test_client_initialization_mqtt_fails_gracefully(self, mock_token):
        """Test Client initialization when MQTT connection fails"""
        with patch('paho.mqtt.client.Client') as mock_mqtt_client:
            mock_mqtt_instance = Mock()
            mock_mqtt_client.return_value = mock_mqtt_instance
            mock_mqtt_instance.connect.side_effect = Exception("Connection failed")

            client = Client(mock_token, api="localhost:8001")

            assert client.mqtt is None  # Should be None due to connection failure

    def test_version_detection(self, mock_token):
        """Test version detection mechanism"""
        with patch('paho.mqtt.client.Client') as mock_mqtt_client:
            mock_mqtt_client.return_value = Mock()

            # Test successful version detection
            with patch('allthingstalk.clients.version', return_value='0.3.0'):
                client = Client(mock_token)
                assert client._get_version() == '0.3.0'

            # Test fallback version
            with patch('allthingstalk.clients.version', side_effect=Exception('Version error')):
                client = Client(mock_token)
                assert client._get_version() == '0.3.0'

    @patch('requests.get')
    def test_get_assets_success(self, mock_get, mock_token, sample_asset_dict):
        """Test successful asset retrieval"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [sample_asset_dict]
        mock_get.return_value = mock_response

        with patch('paho.mqtt.client.Client'):
            client = Client(mock_token)
            assets = client.get_assets("device_123")

            assert len(assets) == 1
            assert assets[0].name == "temperature"
            mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_assets_forbidden(self, mock_get, mock_token):
        """Test asset retrieval with forbidden access"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        with patch('paho.mqtt.client.Client'):
            client = Client(mock_token)

            with pytest.raises(AccessForbiddenException):
                client.get_assets("device_123")

    @patch('requests.post')
    def test_create_asset_success(self, mock_post, mock_token, sample_asset_dict):
        """Test successful asset creation"""
        mock_response = Mock()
        mock_response.json.return_value = sample_asset_dict
        mock_post.return_value = mock_response

        with patch('paho.mqtt.client.Client'):
            client = Client(mock_token)

            from allthingstalk import IntegerAsset
            asset = IntegerAsset(name="test_asset", kind="sensor")
            created_asset = client.create_asset("device_123", asset)

            assert created_asset.name == "temperature"
            mock_post.assert_called_once()

    @patch('requests.get')
    def test_get_asset_state_success(self, mock_get, mock_token):
        """Test successful asset state retrieval"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'state': {'value': 25.5, 'at': '2023-09-19T12:00:00Z'}
        }
        mock_get.return_value = mock_response

        with patch('paho.mqtt.client.Client'):
            client = Client(mock_token)
            state = client.get_asset_state("device_123", "temperature")

            assert state.value == 25.5
            # The AssetState parses the ISO string into a datetime object
            from dateutil.parser import parse as parse_date
            expected_datetime = parse_date('2023-09-19T12:00:00Z')
            assert state.at == expected_datetime

    @patch('requests.get')
    def test_get_asset_state_failure(self, mock_get, mock_token):
        """Test asset state retrieval failure"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with patch('paho.mqtt.client.Client'):
            client = Client(mock_token)

            with pytest.raises(AssetStateRetrievalException):
                client.get_asset_state("device_123", "nonexistent")

    @patch('requests.put')
    def test_publish_asset_state_with_asset_state(self, mock_put, mock_token):
        """Test publishing asset state with AssetState object"""
        with patch('paho.mqtt.client.Client'):
            client = Client(mock_token)

            state = AssetState(value=42)
            client.publish_asset_state("device_123", "counter", state)

            mock_put.assert_called_once()
            call_args = mock_put.call_args
            assert call_args[1]['json']['value'] == 42
            assert 'at' in call_args[1]['json']

    @patch('requests.put')
    def test_publish_asset_state_with_raw_value(self, mock_put, mock_token):
        """Test publishing asset state with raw value"""
        with patch('paho.mqtt.client.Client'):
            client = Client(mock_token)

            client.publish_asset_state("device_123", "counter", 42)

            mock_put.assert_called_once()
            call_args = mock_put.call_args
            assert call_args[1]['json']['value'] == 42
            assert 'at' not in call_args[1]['json']

    def test_get_headers(self, mock_token):
        """Test HTTP headers generation"""
        with patch('paho.mqtt.client.Client'):
            client = Client(mock_token)
            headers = client._get_headers()

            assert headers['Authorization'] == f'Bearer {mock_token}'
            assert 'ATTalk-PythonSDK' in headers['User-Agent']

    def test_attach_device_with_mqtt(self, mock_token):
        """Test device attachment with MQTT enabled"""
        with patch('paho.mqtt.client.Client') as mock_mqtt_client:
            mock_mqtt_instance = Mock()
            mock_mqtt_client.return_value = mock_mqtt_instance

            client = Client(mock_token)
            mock_device = Mock()
            mock_device.id = "device_123"

            client._attach_device(mock_device)

            # Should subscribe to feed and command topics
            assert mock_mqtt_instance.subscribe.call_count == 2
            calls = mock_mqtt_instance.subscribe.call_args_list
            topics = [call[0][0] for call in calls]
            assert 'device/device_123/asset/+/feed' in topics
            assert 'device/device_123/asset/+/command' in topics

    def test_attach_device_without_mqtt(self, mock_token):
        """Test device attachment without MQTT"""
        client = Client(mock_token, mqtt=None)
        mock_device = Mock()
        mock_device.id = "device_123"

        client._attach_device(mock_device)

        assert client._devices["device_123"] == mock_device
