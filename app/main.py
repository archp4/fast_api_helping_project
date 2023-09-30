from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange


# for db connection
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# ORM Files
from . import models
from .database import engine, getDB
from sqlalchemy.orm import Session

# checking models existing into db
models.Base.metadata.create_all(bind=engine)


class Post(BaseModel):  # post schema for valdating post
    title: str
    content: str
    published: bool = True


app = FastAPI()  # fastAPI instance

# # connecting with db
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='FastAPI',
#                                 user='postgres', password='admin', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Conneted With DB")
#         break
#     except Exception as error:
#         print("Connection Failed")
#         print("Error :", error)
#         time.sleep(2)


@app.get("/")
def root():  # this is root/home
    return {"message": "Welcome to My API"}


@app.get("/posts")  # this is for getting all post
def get_all_Posts(db: Session = Depends(getDB)):
    # getting all post form table/database
    posts = db.query(models.Post).all()
    return {
        "message": "All Posts",
        "data": posts
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_Post(payload: Post, db: Session = Depends(getDB)):
    # converting payload into dictonary then unzipping data
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {
        "message": "Created New Post",
        "data": new_post
    }


# @app.get("/posts/latest")
# def get_lastest_post():
#     # getting lastest post by using length function to find length and subtracting with one for last index
#     post = my_post[len(my_post)-1]
#     return {
#         "message": "lastest post",
#         "data": post
#     }


@app.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(getDB)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your requested post by id : {id} is not found")
    return {
        "message": f"your requested post by id : {id}",
        "data": post
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(getDB)):
    # Creating Query for getting Post
    post = db.query(models.Post).filter(models.Post.id == id)
    # check if post is found or not if not then 404
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post by id : {id} is not found")

    # deleting post from Table via orm
    post.delete(synchronize_session=False)

    # saving the change
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post_by_id(id: int, payload: Post, db: Session = Depends(getDB)):
    # Creating Query for getting Post
    post = db.query(models.Post).filter(models.Post.id == id)
    # check if post is found or not if not then 404
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post by id : {id} is not found")

    # updating post from Table via orm
    post.update(payload.model_dump(), synchronize_session=False)

    # saving the change
    db.commit()
    return {
        "message": "Post Updated",
        "data": post.first()
    }
