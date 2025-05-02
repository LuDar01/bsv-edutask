import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController

# Fixture to create a mock DAO and controller instance
@pytest.fixture
def mock_user_controller():
    mock_dao = MagicMock()
    controller = UserController(dao=mock_dao)
    return controller, mock_dao

def test_get_user_by_existing_email(mock_user_controller):
    controller, mock_dao = mock_user_controller
    mock_user = {"email": "existing@example.com"}
    mock_dao.find.return_value = [mock_user]

    result = controller.get_user_by_email("existing@example.com")
    assert result == mock_user

def test_get_user_by_non_existing_email(mock_user_controller):
    controller, mock_dao = mock_user_controller
    mock_dao.find.return_value = [{"email": "dummy@example.com"}, {"email": "dummy2@example.com"}]

    result = controller.get_user_by_email("nonexistent@example.com")
    assert result["email"].startswith("dummy")

def test_get_user_by_invalid_email_format(mock_user_controller):
    controller, _ = mock_user_controller
    with pytest.raises(ValueError):
        controller.get_user_by_email("invalid-email")

def test_get_user_by_none_email(mock_user_controller):
    controller, _ = mock_user_controller
    with pytest.raises(TypeError):
        controller.get_user_by_email(None)

def test_get_user_by_empty_email(mock_user_controller):
    controller, _ = mock_user_controller
    with pytest.raises(ValueError):
        controller.get_user_by_email("")
