from pydantic import BaseModel
from typing import Dict, Any, List


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: Dict[str, Any]


class CreatePostParams(BaseModel):
    title: str
    body: str
    userId: int


class SinglePost(BaseModel):
    id: int
    title: str
    body: str
    author: Dict[str, Any]
    comments: List[Dict[str, Any]]


class UpdatedPost(BaseModel):
    id: int
    title: str
    body: str


class UpdatePostParams(BaseModel):
    title: str
    body: str
