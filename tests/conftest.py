# Test configuration for AllThingsTalk Python SDK
import pytest
import os
import sys
from unittest.mock import Mock

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import allthingstalk


@pytest.fixture
def mock_token():
    """Fixture providing a mock authentication token"""
    return "mock_device_token_12345"


@pytest.fixture
def mock_device_id():
    """Fixture providing a mock device ID"""
    return "mock_device_123"


@pytest.fixture
def mock_http_client():
    """Fixture providing a mocked HTTP client"""
    mock_client = Mock()
    mock_client.get.return_value.status_code = 200
    mock_client.get.return_value.json.return_value = []
    mock_client.post.return_value.json.return_value = {
        'Id': 'asset_123',
        'Name': 'test_asset',
        'Title': 'Test Asset',
        'Description': 'Test Description',
        'Is': 'sensor',
        'Profile': {'type': 'integer'}
    }
    return mock_client


@pytest.fixture
def mock_mqtt_client():
    """Fixture providing a mocked MQTT client"""
    mock_mqtt = Mock()
    mock_mqtt.connect.return_value = None
    mock_mqtt.loop_start.return_value = None
    mock_mqtt.subscribe.return_value = None
    return mock_mqtt


@pytest.fixture
def sample_asset_dict():
    """Fixture providing sample asset dictionary data"""
    return {
        'id': 'asset_123',
        'name': 'temperature',
        'title': 'Temperature Sensor',
        'description': 'Room temperature measurement',
        'is': 'sensor',
        'profile': {'type': 'number'},
        'deviceId': 'device_123'
    }


@pytest.fixture
def sample_device_class():
    """Fixture providing a sample device class for testing"""
    class TestDevice(allthingstalk.Device):
        temperature = allthingstalk.IntegerAsset()
        humidity = allthingstalk.NumberAsset()
        status = allthingstalk.StringAsset()

    return TestDevice
