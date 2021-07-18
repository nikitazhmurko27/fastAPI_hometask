import pytest
from httpx import AsyncClient

from main import app

base_url = "http://127.0.0.1:8000/users"
create_valid_user = {
    "name": "adam lallana",
    "username": "al",
    "email": "al@liverpool.com",
    "phone": "1-2323-2131-435"
}

create_invalid_user = {
    "name": 1,
    "username": 1,
    "email": "al@liverpool.com",
}


@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    user = response.json()[0]
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
    assert isinstance(user["phone"], str)
    assert isinstance(user["email"], str)
    assert isinstance(user["username"], str)


@pytest.mark.asyncio
async def test_create_valid_user():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/", json=create_valid_user)
    assert response.status_code == 201
    user = response.json()
    assert user["name"] == create_valid_user["name"]
    assert user["phone"] == create_valid_user["phone"]
    assert user["email"] == create_valid_user["email"]
    assert user["username"] == create_valid_user["username"]


@pytest.mark.asyncio
async def test_create_invalid_user():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/", json=create_invalid_user)
    assert response.status_code == 422

