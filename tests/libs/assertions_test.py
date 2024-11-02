import pytest
from core.libs.assertions import assert_true, assert_valid, assert_auth, assert_found, base_assert
from core.libs.exceptions import FyleError

def test_assert_true():
    assert_true(True)
    with pytest.raises(FyleError) as excinfo:
        assert_true(False)
    assert excinfo.value.status_code == 403
    assert excinfo.value.message == 'FORBIDDEN'

def test_assert_valid_true():
    assert_valid(True, "This should not raise an error")

def test_assert_valid_false():
    with pytest.raises(FyleError) as excinfo:
        assert_valid(False, "This should raise an error")
    assert excinfo.value.status_code == 400
    assert excinfo.value.message == "This should raise an error"

def test_assert_auth_true():
    assert_auth(True)
    
def test_assert_auth_false():
    with pytest.raises(FyleError) as excinfo:
        assert_auth(False, "This should raise an error")
    assert excinfo.value.status_code == 401
    assert excinfo.value.message == "This should raise an error"

def test_assert_found_true():
    assert_found(object())
    
def test_assert_found_false():
    with pytest.raises(FyleError) as excinfo:
        assert_found(None, "This should raise an error")
    assert excinfo.value.status_code == 404
    assert excinfo.value.message == "This should raise an error"

def test_base_assert():
    with pytest.raises(FyleError) as excinfo:
        base_assert(500, "Internal Server Error")
    assert excinfo.value.status_code == 500
    assert excinfo.value.message == "Internal Server Error"