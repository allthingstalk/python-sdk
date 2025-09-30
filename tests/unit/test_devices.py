import pytest
from unittest.mock import Mock, patch
import json
from datetime import datetime
from allthingstalk import Device, IntegerAsset, StringAsset, NumberAsset


class TestDeviceBase:
    """Test cases for DeviceBase metaclass"""

    def test_metaclass_asset_registration(self):
        """Test that assets are properly registered by metaclass"""
        class TestDevice(Device):
            temperature = IntegerAsset(name="temp")
            status = StringAsset(name="device_status")

        # Check assets are collected
        assert len(TestDevice._assets) == 2

        # Check asset names are set from variable names when not specified
        for asset in TestDevice._assets:
            if hasattr(asset, '_internal_id') and asset._internal_id == 'temperature':
                assert asset.name == "temp"  # Explicitly set name
            elif hasattr(asset, '_internal_id') and asset._internal_id == 'status':
                assert asset.name == "device_status"  # Explicitly set name

    def test_metaclass_handler_decorators(self):
        """Test that handler decorators are properly created"""
        class TestDevice(Device):
            counter = IntegerAsset()

        # Check that handler decorator collections exist
        assert hasattr(TestDevice, 'state')
        assert hasattr(TestDevice, 'feed')
        assert hasattr(TestDevice, 'command')
        assert hasattr(TestDevice, 'event')

        # Check that handlers dict is initialized
        assert hasattr(TestDevice, '_handlers')
        assert 'state' in TestDevice._handlers
        assert 'feed' in TestDevice._handlers
        assert 'command' in TestDevice._handlers
        assert 'event' in TestDevice._handlers


class TestDevice:
    """Test cases for Device class"""

    def test_device_initialization_no_connect(self, mock_token, mock_device_id):
        """Test device initialization without auto-connection"""
        mock_client = Mock()

        class TestDevice(Device):
            temperature = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )

        assert device.id == mock_device_id
        assert device.client == mock_client
        assert device._connected is False
        # Assets should be copied to instance
        assert len(device.assets) == 1
        assert 'temperature' in device.assets

    def test_device_asset_properties_created(self, mock_token, mock_device_id):
        """Test that asset properties are dynamically created"""
        mock_client = Mock()

        class TestDevice(Device):
            temperature = IntegerAsset()
            status = StringAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )

        # Check that properties exist
        assert hasattr(device, 'temperature')
        assert hasattr(device, 'status')

        # Properties should be property objects
        assert isinstance(type(device).__dict__['temperature'], property)
        assert isinstance(type(device).__dict__['status'], property)

    def test_device_asset_getter_not_connected(self, mock_token, mock_device_id):
        """Test asset getter calls client when device is connected"""
        mock_client = Mock()
        mock_client.get_asset_state.return_value = Mock(value=25.5)

        class TestDevice(Device):
            temperature = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )
        device._connected = True  # Simulate connected state

        # Getting property should call client
        result = device.temperature
        mock_client.get_asset_state.assert_called_once_with(mock_device_id, 'temperature')

    def test_device_asset_setter_connected(self, mock_token, mock_device_id):
        """Test asset setter publishes when device is connected"""
        mock_client = Mock()

        class TestDevice(Device):
            temperature = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )
        device._connected = True

        # Setting property should publish state
        device.temperature = 23.5
        mock_client.publish_asset_state.assert_called_once_with(
            mock_device_id, 'temperature', 23.5
        )

    def test_device_asset_setter_not_connected(self, mock_token, mock_device_id):
        """Test asset setter raises error when device not connected"""
        mock_client = Mock()

        class TestDevice(Device):
            temperature = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )
        # Device is not connected

        with pytest.raises(RuntimeError, match="Device not started"):
            device.temperature = 23.5

    @patch('allthingstalk.devices.Device.connect')
    def test_device_auto_connect(self, mock_connect, mock_token, mock_device_id):
        """Test device auto-connects during initialization"""
        mock_client = Mock()

        class TestDevice(Device):
            temperature = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=True  # Should auto-connect
        )

        mock_connect.assert_called_once()

    def test_device_connect_without_id_raises_error(self, mock_token):
        """Test that connecting without device ID raises NotImplementedError"""
        mock_client = Mock()

        class TestDevice(Device):
            temperature = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=None,
            connect=False
        )

        with pytest.raises(NotImplementedError, match="Device creation not implemented"):
            device.connect()

    def test_device_connect_success(self, mock_token, mock_device_id, sample_asset_dict):
        """Test successful device connection"""
        mock_client = Mock()
        # Mock getting existing assets
        mock_client.get_assets.return_value = []  # No existing assets
        # Mock asset creation
        mock_asset = Mock()
        mock_asset.id = "asset_123"
        mock_asset.thing_id = "thing_123"
        mock_client.create_asset.return_value = mock_asset

        class TestDevice(Device):
            temperature = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )

        device.connect()

        assert device._connected is True
        mock_client.get_assets.assert_called_once_with(mock_device_id)
        mock_client.create_asset.assert_called_once()
        mock_client._attach_device.assert_called_once_with(device)

    def test_device_connect_existing_assets(self, mock_token, mock_device_id):
        """Test device connection with existing assets"""
        mock_client = Mock()

        # Mock existing asset
        existing_asset = Mock()
        existing_asset.name = "temperature"
        existing_asset.id = "existing_asset_123"
        existing_asset.thing_id = "thing_123"
        mock_client.get_assets.return_value = [existing_asset]

        class TestDevice(Device):
            temperature = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )

        device.connect()

        # Should not create asset since it exists
        mock_client.create_asset.assert_not_called()

        # Asset should be updated with cloud info
        assert device.assets['temperature'].id == "existing_asset_123"
        assert device.assets['temperature'].thing_id == "thing_123"

    def test_device_on_message_handling(self, mock_token, mock_device_id):
        """Test device message handling"""
        mock_client = Mock()

        # Create handler mock
        handler_called = False
        received_value = None
        received_timestamp = None

        def mock_handler(device, value, at):
            nonlocal handler_called, received_value, received_timestamp
            handler_called = True
            received_value = value
            received_timestamp = at

        class TestDevice(Device):
            temperature = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )

        # Register handler
        device._handlers['state']['temperature'] = mock_handler

        # Simulate message
        message_data = json.dumps({'value': 25.5, 'at': '2023-09-19T12:00:00Z'})
        device._on_message('state', 'temperature', message_data.encode('utf-8'))

        assert handler_called is True
        assert received_value == 25.5
        assert isinstance(received_timestamp, datetime)

    def test_device_on_message_simple_value(self, mock_token, mock_device_id):
        """Test device message handling with simple value"""
        mock_client = Mock()

        handler_called = False
        received_value = None

        def mock_handler(device, value, at):
            nonlocal handler_called, received_value
            handler_called = True
            received_value = value

        class TestDevice(Device):
            counter = IntegerAsset()

        device = TestDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )

        # Register handler
        device._handlers['command']['counter'] = mock_handler

        # Simulate simple value message
        message_data = json.dumps(42)
        device._on_message('command', 'counter', message_data.encode('utf-8'))

        assert handler_called is True
        assert received_value == 42

    def test_device_multiple_assets(self, mock_token, mock_device_id):
        """Test device with multiple different asset types"""
        mock_client = Mock()

        class ComplexDevice(Device):
            temperature = IntegerAsset(title="Temperature")
            humidity = NumberAsset(title="Humidity")
            status = StringAsset(title="Status")

        device = ComplexDevice(
            client=mock_client,
            id=mock_device_id,
            connect=False
        )

        assert len(device.assets) == 3
        assert 'temperature' in device.assets
        assert 'humidity' in device.assets
        assert 'status' in device.assets

        # Check titles are preserved
        assert device.assets['temperature'].title == "Temperature"
        assert device.assets['humidity'].title == "Humidity"
        assert device.assets['status'].title == "Status"
