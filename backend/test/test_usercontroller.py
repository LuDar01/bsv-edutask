"""Unit tests for UserController email functionality."""

from unittest import mock
import pytest

from src.controllers.usercontroller import UserController


@pytest.fixture
def user_controller(users):
    """Create UserController with mocked DAO returning provided users."""
    dao = mock.Mock()
    dao.find.return_value = users 
    controller = UserController(dao=dao)
    return controller


@pytest.mark.lab1
@pytest.mark.parametrize('users, email, expected', [
    # Single user match
    ([{"username": "Jhon", "email": "jhon@exempel.com","age":25}], "jhon@exempel.com", {"username": "Jhon", "email": "jhon@exempel.com","age":25}),
    # Multiple users - return first
    ([{"username": "Jhon", "email": "jhon@exempel.com"},{"username": "Jhon2", "email": "jhon@exempel.com"}], "jhon@exempel.com", {"username": "Jhon", "email": "jhon@exempel.com"}),
    # No users found
    ([], "jhon@exempel.com", None)
])
def test_get_user_by_email(user_controller, email, expected):
    """Test email lookup with single match, multiple matches, and no matches."""
    result = user_controller.get_user_by_email(email)
    assert result == expected


@pytest.mark.lab1
@pytest.mark.parametrize('users, email', [
    # Multiple users with same email
    ([{"username": "Jhon", "email": "jhon@exempel.com"},{"username": "Jhon2", "email": "jhon@exempel.com"}],"jhon@exempel.com")
])
def test_multiple_users_warning(user_controller, email, capsys):
    """Test warning message when multiple users share email."""
    user_controller.get_user_by_email(email)
    captured = capsys.readouterr()
    assert f'Error: more than one user found with mail {email}' in captured.out


@pytest.mark.lab1
@pytest.mark.parametrize('users, email', [
    # Invalid email format
    ([{"username": "Jhon", "email": "jhon@exempel.com"}],"not-vaild-email")
])
def test_invalid_email(user_controller, email):
    """Test ValueError raised for invalid email format."""
    with pytest.raises(ValueError):
        user_controller.get_user_by_email(email)


@pytest.mark.lab1
@pytest.mark.parametrize('users, email', [
    # Database failure scenario
    ([{"username": "Jhon", "email": "jhon@exempel.com"}],"not-vaild-email")
])
def test_database_failure(user_controller, email):
    """Test Exception raised when database operation fails."""
    user_controller.dao.find.side_effect = Exception("db error")
    with pytest.raises(Exception):
        user_controller.get_user_by_email(email)
