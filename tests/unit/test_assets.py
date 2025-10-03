import pytest
from allthingstalk import assets


class TestAsset:
    """Test cases for the base Asset class"""

    def test_asset_initialization_with_profile(self):
        """Test basic asset initialization with profile"""
        profile = {'type': 'number'}
        asset = assets.Asset(
            name="test_asset",
            title="Test Asset",
            description="A test asset",
            kind="sensor",
            profile=profile
        )

        assert asset.name == "test_asset"
        assert asset.title == "Test Asset"
        assert asset.description == "A test asset"
        assert asset.kind == "sensor"
        assert asset.profile == profile

    def test_asset_from_dict(self, sample_asset_dict):
        """Test Asset creation from dictionary"""
        asset = assets.Asset.from_dict(sample_asset_dict)

        assert asset.name == "temperature"
        assert asset.title == "Temperature Sensor"
        assert asset.description == "Room temperature measurement"
        assert asset.kind == "sensor"
        assert asset.id == "asset_123"
        assert asset.thing_id == "device_123"

    def test_asset_initialization_without_profile_raises_error(self):
        """Test that Asset without profile raises exception"""
        with pytest.raises(Exception):  # InvalidAssetProfileException
            assets.Asset(name="test_asset")


class TestIntegerAsset:
    """Test cases for IntegerAsset"""

    def test_integer_asset_creation(self):
        """Test IntegerAsset initialization"""
        asset = assets.IntegerAsset(
            name="counter",
            title="Counter Asset"
        )

        assert asset.name == "counter"
        assert asset.title == "Counter Asset"
        assert hasattr(asset, 'profile')
        assert asset.profile is not None

    def test_integer_asset_inheritance(self):
        """Test that IntegerAsset inherits from NumberAsset"""
        asset = assets.IntegerAsset()

        assert isinstance(asset, assets.NumberAsset)
        assert isinstance(asset, assets.Asset)


class TestNumberAsset:
    """Test cases for NumberAsset"""

    def test_number_asset_creation(self):
        """Test NumberAsset initialization"""
        asset = assets.NumberAsset(
            name="temperature",
            title="Temperature"
        )

        assert asset.name == "temperature"
        assert asset.title == "Temperature"
        assert hasattr(asset, 'profile')
        assert asset.profile is not None

    def test_number_asset_has_profile_class(self):
        """Test that NumberAsset has correct profile class"""
        assert assets.NumberAsset._PROFILE_CLASS is not None


class TestStringAsset:
    """Test cases for StringAsset"""

    def test_string_asset_creation(self):
        """Test StringAsset initialization"""
        asset = assets.StringAsset(
            name="status",
            title="Device Status"
        )

        assert asset.name == "status"
        assert asset.title == "Device Status"
        assert hasattr(asset, 'profile')


class TestBooleanAsset:
    """Test cases for BooleanAsset"""

    def test_boolean_asset_creation(self):
        """Test BooleanAsset initialization"""
        asset = assets.BooleanAsset(
            name="active",
            title="Device Active"
        )

        assert asset.name == "active"
        assert asset.title == "Device Active"
        assert hasattr(asset, 'profile')
