import pytest
from core import app
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_ready(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ready'

def test_handle_fyle_error(client):
    @app.route('/fyle_error')
    def fyle_error_route():
        raise FyleError(status_code=400, message="Test FyleError")

    response = client.get('/fyle_error')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'FyleError'
    assert data['message'] == 'Test FyleError'

def test_handle_validation_error(client):
    @app.route('/validation_error')
    def validation_error_route():
        raise ValidationError("Test ValidationError")

    response = client.get('/validation_error')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'ValidationError'
    assert data['message'][0] == 'Test ValidationError'

def test_handle_integrity_error(client):
    @app.route('/integrity_error')
    def integrity_error_route():
        raise IntegrityError("Test IntegrityError", None, None)

    response = client.get('/integrity_error')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'IntegrityError'
    assert data['message'] == 'Integrity error'

def test_handle_http_exception(client):
    @app.route('/not_found')
    def not_found_route():
        raise NotFound("Test NotFound")

    response = client.get('/not_found')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'NotFound'
    assert data['message'] == '404 Not Found: Test NotFound'

def test_handle_generic_exception(client):
    @app.route('/generic_error')
    def generic_error_route():
        raise Exception("Test Exception")

    with pytest.raises(Exception) as excinfo:
        client.get('/generic_error')
    assert str(excinfo.value) == "Test Exception"