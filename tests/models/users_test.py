import pytest
from core import db
from core.models.users import User

@pytest.fixture
def setup_user():
    user = User(username="testuser", email="testuser@example.com")
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()

def test_user_creation(setup_user):
    user = setup_user
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"

def test_user_repr(setup_user):
    user = setup_user
    assert repr(user) == "<User 'testuser'>"

def test_user_get_by_id(setup_user):
    user = setup_user
    fetched_user = User.get_by_id(user.id)
    assert fetched_user is not None
    assert fetched_user.id == user.id

def test_user_get_by_email(setup_user):
    user = setup_user
    fetched_user = User.get_by_email(user.email)
    assert fetched_user is not None
    assert fetched_user.email == user.email