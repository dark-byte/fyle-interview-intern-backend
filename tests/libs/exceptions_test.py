import pytest
from core.libs.exceptions import FyleError, ValidationError

def test_fyle_error():
    error = FyleError(status_code=400, message="Test error")
    assert error.status_code == 400
    assert error.message == "Test error"
    assert error.to_dict() == {"message": "Test error"}

def test_validation_error():
    error = ValidationError(message="Validation error")
    assert error.status_code == 400
    assert error.message == "Validation error"
    assert error.to_dict() == {"message": "Validation error"}