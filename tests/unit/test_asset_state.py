from datetime import datetime
from allthingstalk import AssetState


class TestAssetState:
    """Test cases for AssetState class"""

    def test_asset_state_creation_with_value(self):
        """Test creating AssetState with just a value"""
        state = AssetState(value=42)

        assert state.value == 42
        assert isinstance(state.at, datetime)

    def test_asset_state_creation_with_timestamp(self):
        """Test creating AssetState with value and timestamp"""
        from dateutil.tz import tzutc
        timestamp = datetime(2023, 9, 19, 12, 0, 0)
        state = AssetState(value="test_value", at=timestamp)

        assert state.value == "test_value"
        # AssetState converts naive datetime to timezone-aware, so compare the underlying values
        expected_with_tz = timestamp.replace(tzinfo=tzutc())
        assert state.at == expected_with_tz

    def test_asset_state_with_different_value_types(self):
        """Test AssetState with various value types"""
        # Integer
        int_state = AssetState(value=123)
        assert int_state.value == 123

        # String
        str_state = AssetState(value="hello")
        assert str_state.value == "hello"

        # Boolean
        bool_state = AssetState(value=True)
        assert bool_state.value is True

        # Float
        float_state = AssetState(value=3.14)
        assert float_state.value == 3.14

        # Dictionary
        dict_state = AssetState(value={"lat": 51.5, "lon": -0.1})
        assert dict_state.value["lat"] == 51.5
        assert dict_state.value["lon"] == -0.1

    def test_asset_state_timestamp_defaults_to_now(self):
        """Test that AssetState defaults timestamp to current time"""
        from dateutil.tz import tzutc
        before = datetime.utcnow().replace(tzinfo=tzutc())
        state = AssetState(value="test")
        after = datetime.utcnow().replace(tzinfo=tzutc())

        assert before <= state.at <= after

    def test_asset_state_none_value(self):
        """Test AssetState can handle None values"""
        state = AssetState(value=None)

        assert state.value is None
        assert isinstance(state.at, datetime)
