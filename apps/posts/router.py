from typing import List

from fastapi import APIRouter, Depends
from .dependencies import get_post_repository, PostRepository
from .models import Post, CreatePostParams, SinglePost, UpdatedPost, UpdatePostParams

router = APIRouter()


@router.get("/", response_model=List[Post])
async def list_posts(repository: PostRepository = Depends(get_post_repository)):
    posts = await repository.list_posts()
    return posts


@router.post("/", response_model=Post, status_code=201)
async def create_post(
        params: CreatePostParams,
        repository: PostRepository = Depends(get_post_repository)
):
    post = await repository.create_post(params)
    return post


@router.get("/{post_id}", response_model=SinglePost)
async def single_post(
        post_id: int,
        repository: PostRepository = Depends(get_post_repository)):
    post = await repository.single_post(post_id)
    return post


@router.put("/{post_id}", response_model=UpdatedPost, status_code=200)
async def update_post(
        post_id: int,
        params: UpdatePostParams,
        repository: PostRepository = Depends(get_post_repository)):
    post = await repository.update_post(post_id, params)
    return post
