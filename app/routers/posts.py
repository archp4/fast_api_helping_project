from typing import List  # Import for pydantic to Tell response will be list
from fastapi import status, HTTPException, Response, Depends, APIRouter
# ORM Files
from .. import models, formatting
from ..database import getDB
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",  # prefix attach to path operation with router
    tags=['Post']  # grouping
)


@router.get("/", response_model=List[formatting.PostResponse])
def get_all_Posts(db: Session = Depends(getDB)):  # this is for getting all post
    # getting all post form table/database
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=formatting.PostResponse)
def create_Post(payload: formatting.PostCreate, db: Session = Depends(getDB)):
    # converting payload into dictonary then unzipping data
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# @router.get("/posts/latest")
# def get_lastest_post():
#     # getting lastest post by using length function to find length and subtracting with one for last index
#     post = my_post[len(my_post)-1]
#     return {
#         "message": "lastest post",
#         "data": post
#     }


@router.get("/{id}", response_model=formatting.PostResponse)
def get_post_by_id(id: int, db: Session = Depends(getDB)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your requested post by id : {id} is not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=formatting.PostResponse)
def update_post_by_id(id: int, payload: formatting.PostCreate, db: Session = Depends(getDB)):
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
    return post.first()
