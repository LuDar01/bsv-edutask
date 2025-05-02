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

def test_create_valid_document(dao):
    valid_user = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com"
    }
    inserted_user = dao.create(valid_user)
    assert inserted_user["email"] == "john.doe@example.com"
    assert inserted_user["firstName"] == "John"
    assert inserted_user["lastName"] == "Doe"

def test_create_missing_required_field(dao):
    # Missing 'lastName'
    invalid_user = {
        "firstName": "Alice",
        "email": "alice@example.com"
    }
    with pytest.raises(Exception):
        dao.create(invalid_user)

def test_create_wrong_type(dao):
    # 'lastName' is an integer (should be string)
    invalid_user = {
        "firstName": "Bob",
        "lastName": 123,
        "email": "bob@example.com"
    }
    with pytest.raises(Exception):
        dao.create(invalid_user)

def test_create_with_extra_field(dao):
    # 'role' is not defined in schema, but schema allows extra fields
    user_with_extra = {
        "firstName": "Eve",
        "lastName": "Smith",
        "email": "eve@example.com",
        "role": "admin"  # allowed because additionalProperties is not restricted
    }
    inserted_user = dao.create(user_with_extra)
    assert inserted_user["role"] == "admin"

def test_create_in_non_existent_collection():
    client = MongoClient("mongodb://localhost:27017")
    db = client["edutask_test"]
    dao = DAO("user")  # 'user.json' schema exists
    user = {
        "firstName": "Ghost",
        "lastName": "User",
        "email": "ghost@example.com"
    }
    inserted_user = dao.create(user)
    assert inserted_user["email"] == "ghost@example.com"
