import pytest
from pymongo import MongoClient
from src.util.dao import DAO

@pytest.fixture(scope="module")
def dao():
    client = MongoClient("mongodb://localhost:27017")
    db = client["edutask_test"]
    collection_name = "user"  # matches user.json
    db[collection_name].drop()  # Clear test collection before tests
    return DAO(collection_name)

@pytest.mark.ass2
def test_create_valid_document(dao):
    valid_user = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com"
    }
    inserted_user = dao.create(valid_user)
    assert inserted_user["email"] == "john.doe@example.com"

@pytest.mark.ass2
def test_create_missing_required_field(dao):
    # Missing 'lastName'
    invalid_user = {
        "firstName": "Alice",
        "email": "alice@example.com"
    }
    with pytest.raises(Exception):
        dao.create(invalid_user)

@pytest.mark.ass2
def test_create_wrong_type(dao):
    # 'lastName' is an integer (should be string)
    invalid_user = {
        "firstName": "Bob",
        "lastName": 123,
        "email": "bob@example.com"
    }
    with pytest.raises(Exception):
        dao.create(invalid_user)

@pytest.mark.ass2
def test_create_document_with_duplicate_email(dao):
    # 'email' is a uniqueItem
    user1 = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com"
    }
    user2 = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com"
    }
    dao.create(user1)
    with pytest.raises(Exception):
        dao.create(user2)
