from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()

my_post = [
    {
        "title": "post 1",
        "content": "content 1",
        "id": 1
    },
    {
        "title": "post 2",
        "content": "content 2",
        "id": 2
    }
]


def find_post(id):
    for p in my_post:
        if (p['id'] == id):
            return p


@app.get("/")
def root():
    return {"message": "Welcome to My API"}


@app.get("/posts")
def getPosts():
    return {
        "message": "All Posts",
        "data": my_post
    }


@app.post("/create-post")
def createPost(payload: Post):
    post = payload.model_dump()
    post['id'] = randrange(0, 999999)
    my_post.append(post)
    return {
        "message": "Created New Post",
        "data": post
    }


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    post = find_post(id)
    return {
        "message": f"your request post by id :{id}",
        "data": post
    }
