import pytest
from allthingstalk.exceptions import (
    AssetStateRetrievalException,
    AccessForbiddenException,
    AssetMismatchException
)


class TestExceptions:
    """Test cases for custom exceptions"""

    def test_asset_state_retrieval_exception(self):
        """Test AssetStateRetrievalException creation and inheritance"""
        exception = AssetStateRetrievalException("Failed to retrieve asset state")

        assert str(exception) == "Failed to retrieve asset state"
        assert isinstance(exception, Exception)

    def test_asset_state_retrieval_exception_no_message(self):
        """Test AssetStateRetrievalException without message"""
        exception = AssetStateRetrievalException()

        # Should not raise error
        assert isinstance(exception, Exception)

    def test_access_forbidden_exception(self):
        """Test AccessForbiddenException creation and inheritance"""
        exception = AccessForbiddenException("Access denied to resource")

        assert str(exception) == "Access denied to resource"
        assert isinstance(exception, Exception)

    def test_asset_mismatch_exception(self):
        """Test AssetMismatchException creation and inheritance"""
        exception = AssetMismatchException("Asset definitions do not match")

        assert str(exception) == "Asset definitions do not match"
        assert isinstance(exception, Exception)

    def test_exception_raising(self):
        """Test that exceptions can be properly raised and caught"""

        with pytest.raises(AssetStateRetrievalException):
            raise AssetStateRetrievalException("Test error")

        with pytest.raises(AccessForbiddenException):
            raise AccessForbiddenException("Access denied")

        with pytest.raises(AssetMismatchException):
            raise AssetMismatchException("Mismatch error")
