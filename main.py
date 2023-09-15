from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange


class Post(BaseModel):  # post schema for valdating post
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()  # fastAPI instance


# temp array to store post on server
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


def find_post(id):  # function to find post by id
    for p in my_post:
        if (p['id'] == id):
            return p


def find_post_index(id):  # function to find post index by id
    for index, post in enumerate(my_post):
        if (post['id'] == id):
            return index


@app.get("/")
def root():  # this is root/home
    return {"message": "Welcome to My API"}


@app.get("/posts")  # this is for getting all post
def getPosts():
    return {
        "message": "All Posts",
        "data": my_post
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(payload: Post):
    # storing post data as dict
    post = payload.model_dump()

    # giving random id using randrange function
    post['id'] = randrange(0, 999999)

    # storing new post with id in list
    my_post.append(post)

    return {
        "message": "Created New Post",
        "data": post
    }


@app.get("/posts/latest")
def get_lastest_post():
    # getting lastest post by using length function to find length and subtracting with one for last index
    post = my_post[len(my_post)-1]
    return {
        "message": "lastest post",
        "data": post
    }


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    post = find_post(id)  # getting post by id and storing in post(variable)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your requested post by id : {id} is not found")
    return {
        "message": f"your requested post by id : {id}",
        "data": post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int):
    # getting post index by id and storing in post(variable)
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post by id : {id} is not found")
    my_post.pop(index)  # deleting post for array
    return Response(status_code=status.HTTP_204_NO_CONTENT)
