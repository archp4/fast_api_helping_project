from typing import List  # Import for pydantic to Tell response will be list
from fastapi import status, HTTPException, Response, Depends, APIRouter
# ORM Files
from .. import models, formatting, oauth2
from ..database import getDB
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",  # prefix attach to path operation with router
    tags=['Post']  # grouping
)


@router.get("/", response_model=List[formatting.PostResponse])
# this is for getting all post
def get_all_Posts(db: Session = Depends(getDB), current_user: int = Depends(oauth2.get_cuurent_user_id)):
    # getting all post form table/database
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=formatting.PostResponse)
def create_Post(payload: formatting.PostCreate, db: Session = Depends(getDB), current_user: int = Depends(oauth2.get_cuurent_user_id)):
    # converting payload into dictonary then unzipping data
    new_post = models.Post(user_id=current_user.id, ** payload.model_dump())
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
def get_post_by_id(id: int, db: Session = Depends(getDB), current_user: int = Depends(oauth2.get_cuurent_user_id)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your requested post by id : {id} is not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(getDB), current_user: int = Depends(oauth2.get_cuurent_user_id)):
    # Creating Query for getting Post
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()  # temp store post
    # check if post is found or not if not then 404
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post by id : {id} is not found")
    # check if user is owner of post or not
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"requested action is unauthorized")
    # deleting post from Table via orm
    post_query.delete(synchronize_session=False)

    # saving the change
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=formatting.PostResponse)
def update_post_by_id(id: int, payload: formatting.PostCreate, db: Session = Depends(getDB), current_user: int = Depends(oauth2.get_cuurent_user_id)):
    # Creating Query for getting Post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # temp store post
    post = post_query.first()
    # check if post is found or not if not then 404
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post by id : {id} is not found")

    # check if user is owner of post or not
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"requested action is unauthorized")
    # updating post from Table via orm
    post_query.update(payload.model_dump(), synchronize_session=False)

    # saving the change
    db.commit()
    return post_query.first()
