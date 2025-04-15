import pytest
from pydantic import ValidationError
from datetime import datetime
from uuid import uuid4
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, LoginRequest


@pytest.fixture
def user_base_data():
    return {
        "username": "john_doe_123",
        "email": "john.doe@example.com",
        "full_name": "John Doe",
        "bio": "Software engineer with 5+ years of experience.",
        "profile_picture_url": "https://example.com/john_doe.png"
    }


@pytest.fixture
def user_create_data(user_base_data):
    return {
        **user_base_data,
        "password": "SecurePass123!"
    }


@pytest.fixture
def user_update_data():
    return {
        "email": "new.doe@example.com",
        "full_name": "New John Doe",
        "bio": "Updated bio here.",
        "profile_picture_url": "https://example.com/john_doe_updated.jpg"
    }


@pytest.fixture
def user_response_data():
    return {
        "id": str(uuid4()),
        "username": "john_doe_123",
        "email": "john.doe@example.com",
        "full_name": "John Doe",
        "bio": "Software engineer",
        "profile_picture_url": "https://example.com/profile.png",
        "last_login_at": datetime.utcnow(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "links": []
    }


@pytest.fixture
def login_request_data():
    return {
        "username": "john_doe_123",
        "password": "SecurePass123!"
    }


def test_user_base_valid(user_base_data):
    user = UserBase(**user_base_data)
    assert user.username == user_base_data["username"]
    assert user.email == user_base_data["email"]


def test_user_create_valid(user_create_data):
    user = UserCreate(**user_create_data)
    assert user.username == user_create_data["username"]
    assert user.password == user_create_data["password"]


def test_user_update_valid(user_update_data):
    user = UserUpdate(**user_update_data)
    assert user.email == user_update_data["email"]
    assert user.full_name == user_update_data["full_name"]


def test_user_response_valid(user_response_data):
    user = UserResponse(**user_response_data)
    assert user.id == user_response_data["id"]
    assert user.username == user_response_data["username"]


def test_login_request_valid(login_request_data):
    login = LoginRequest(**login_request_data)
    assert login.username == login_request_data["username"]
    assert login.password == login_request_data["password"]


@pytest.mark.parametrize("username", ["valid_user", "user123", "john_doe", "user-name"])
def test_user_base_username_valid(username, user_base_data):
    user_base_data["username"] = username
    user = UserBase(**user_base_data)
    assert user.username == username


@pytest.mark.parametrize("username", ["", "us", "user*", "user name"])
def test_user_base_username_invalid(username, user_base_data):
    user_base_data["username"] = username
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)


@pytest.mark.parametrize("url", [
    "https://example.com/pic.jpg",
    "https://example.com/photo.png",
    None
])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url


@pytest.mark.parametrize("url", [
    "http://example.com/image.jpg",
    "https://example.com/image.txt",
    "ftp://example.com/image.png"
])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValidationError):
        UserBase(**user_base_data)
