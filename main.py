from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to My API"}


@app.get("/posts")
def getPosts():
    return {"message": "there are no post avaiable yet"}


@app.post("/create-post")
def createPost(payload: Post):
    return {"message": "Creating New Post", "data": payload.model_dump}
