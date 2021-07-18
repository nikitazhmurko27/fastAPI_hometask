from typing import Any, List, Dict

import aiohttp as aiohttp

from .models import Post, CreatePostParams, SinglePost, UpdatedPost, UpdatePostParams


class PostRepository:
    def __init__(self):
        self._posts = []
        self._serial = len(self._posts)

    async def list_posts(self) -> list[Post]:
        return self._posts.copy()

    async def create_post(self, params: CreatePostParams) -> Post:
        post = Post(
            id=self._serial,
            **params.dict()
        )
        self._serial += 1
        self._posts.append(post)
        return post

    async def single_post(self, post_id: int) -> Post:
        pass

    async def update_post(self, post_id: int, params: UpdatePostParams) -> UpdatedPost:
        pass


class JSONPlaceholderPostRepository(PostRepository):
    def __init__(self):
        self._posts_endpoint = "https://jsonplaceholder.typicode.com/posts"
        self._authors_endpoint = "https://jsonplaceholder.typicode.com/users"

    async def list_posts(self) -> List[Post]:
        raw_posts = await self._list_posts()
        await self._get_post_author(raw_posts)
        return [self._convert_post(raw_post) for raw_post in raw_posts]

    async def _list_posts(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._posts_endpoint)
            raw_posts = await resp.json()
            return raw_posts

    async def _list_authors(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._authors_endpoint)
            raw_authors = await resp.json()
            return raw_authors

    async def _dict_authors(self) -> Dict[str, Any]:
        authors = {}
        raw_authors = await self._list_authors()
        for raw_author in raw_authors:
            authors[raw_author["id"]] = {
                "name": raw_author["name"],
                "email": raw_author["email"],
            }
        return authors

    async def _get_post_author(self, posts: List[Dict[str, Any]]):
        authors = await self._dict_authors()
        for post in posts:
            author_id = post["userId"]
            post["author"] = {
                "id": author_id,
                "name": authors[author_id]["name"],
                "email": authors[author_id]["email"],
            }

    async def _get_author_by_id(self, author_id: str) -> Dict[str, Any]:
        authors = await self._dict_authors()
        if author_id in authors:
            author_dict = {
                "id": author_id,
                "name": authors[author_id]["name"],
                "email": authors[author_id]["email"],
            }
            return author_dict
        return {}

    async def create_post(self, params: CreatePostParams) -> Post:
        raw_post = await self._create_post(params)
        return self._convert_post(raw_post)

    async def _create_post(self, params: CreatePostParams) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.post(self._posts_endpoint, json=params.dict())
            raw_post = await resp.json()
            raw_post["author"] = await self._get_author_by_id(raw_post["userId"])
            return raw_post

    async def single_post(self, post_id: int) -> SinglePost:
        raw_post = await self._single_post(post_id)
        return SinglePost(**raw_post)

    async def _single_post(self, post_id: int) -> dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._posts_endpoint + f"/{post_id}")
            raw_post = await resp.json()
            raw_post["author"] = await self._get_author_by_id(raw_post["userId"])
            raw_post["comments"] = await self._post_comments(post_id)
            return raw_post

    async def _post_comments(self, post_id: int) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._posts_endpoint + f"/{post_id}/comments")
            raw_comments = await resp.json()
            return raw_comments

    async def update_post(self, post_id: int, params: UpdatePostParams) -> UpdatedPost:
        raw_post = await self._update_post(post_id, params)
        return UpdatedPost(**raw_post)

    async def _update_post(self, post_id: int, params: UpdatePostParams) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.put(self._posts_endpoint + f"/{post_id}", json=params.dict())
            raw_post = await resp.json()
            return raw_post

    def _convert_post(self, raw_post: Dict[str, Any]) -> Post:
        return Post(**raw_post)


class PostRepositoryFactory:
    def __init__(self):
        self._repo = None

    def __call__(self):
        if self._repo is None:
            self._repo = JSONPlaceholderPostRepository()
        return self._repo


get_post_repository = PostRepositoryFactory()
