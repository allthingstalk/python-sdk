import pytest
import sys
from allthingstalk import Client, Device, IntegerAsset


class TestPythonCompatibility:
    """Test Python version compatibility"""

    def test_python_version_supported(self):
        """Test that Python version is supported"""
        major, minor = sys.version_info[:2]
        assert major == 3, "Only Python 3 is supported"
        assert minor >= 6, f"Python 3.{minor} detected, minimum required is 3.6"

    def test_basic_imports(self):
        """Test that all main components can be imported"""
        from allthingstalk import (
            Client, Device, IntegerAsset, NumberAsset,
            BooleanAsset, StringAsset, AssetState, BaseClient
        )

        # All imports should succeed without error
        assert Client is not None
        assert Device is not None
        assert IntegerAsset is not None

    def test_client_creation_python_versions(self):
        """Test client creation works across Python versions"""
        client = Client("test_token", mqtt=None)  # No MQTT to avoid connection
        assert client.token == "test_token"
        assert client._get_version() is not None

    def test_device_metaclass_python_versions(self):
        """Test device metaclass works across Python versions"""
        from allthingstalk import StringAsset

        class TestDevice(Device):
            sensor = IntegerAsset()
            status = StringAsset()

        # Metaclass should work properly
        assert hasattr(TestDevice, '_assets')
        assert len(TestDevice._assets) == 2
        assert hasattr(TestDevice, '_handlers')

    @pytest.mark.skipif(sys.version_info < (3, 8), reason="importlib.metadata requires Python 3.8+")
    def test_modern_import_mechanism(self):
        """Test modern importlib.metadata works"""
        from importlib.metadata import version
        # Should not raise an error
        assert version is not None
