import pytest
from httpx import AsyncClient

from main import app

base_url = "http://127.0.0.1:8000/posts"
create_valid_post = {
    "title": "New Title",
    "body": "New Content",
    "userId": 1,
}

create_invalid_post = {
    "title": 1,
    "body": 2,
    "userId": "some text",
}

update_post = {
    "title": "Updated Title",
    "body": "Updated Content",
}


@pytest.mark.asyncio
async def test_get_posts():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    post = response.json()[0]
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str)
    assert isinstance(post["body"], str)
    assert isinstance(post["author"], dict)


@pytest.mark.asyncio
async def test_create_valid_post():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/", json=create_valid_post)
    assert response.status_code == 201
    post = response.json()
    assert post["title"] == create_valid_post["title"]
    assert post["body"] == create_valid_post["body"]
    assert isinstance(post["id"], int)
    assert isinstance(post["author"], dict)
    assert post["author"]["id"] == create_valid_post["userId"]


@pytest.mark.asyncio
async def test_create_invalid_post():
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.post("/", json=create_invalid_post)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_post():
    post_id = 1
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.put(f"/{post_id}", json=update_post)
    assert response.status_code == 200
    post = response.json()
    assert post["title"] == update_post["title"]
    assert post["body"] == update_post["body"]
    assert post["id"] == post_id


@pytest.mark.asyncio
async def test_get_single_post():
    post_id = 1
    async with AsyncClient(app=app, base_url=base_url) as ac:
        response = await ac.get(f"/{post_id}")
    assert response.status_code == 200
    post = response.json()
    assert isinstance(post["id"], int)
    assert isinstance(post["title"], str)
    assert isinstance(post["body"], str)
    assert isinstance(post["author"], dict)
    assert isinstance(post["comments"], list)