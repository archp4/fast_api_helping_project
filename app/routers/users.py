

from fastapi import status, HTTPException, Depends, APIRouter
# ORM Files
from .. import models, formatting, utils
from ..database import getDB
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",  # prefix attach to path operation with router
    tags=['User']  # Grouping
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=formatting.UserResponse)
def create_User(payload: formatting.UserRequest, db: Session = Depends(getDB)):
    # hashing the password
    hash_password = utils.hash(payload.password)
    # replacing hash with password
    payload.password = hash_password
    # converting payload into dictonary then unzipping data
    new_post = models.User(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=formatting.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(getDB)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"your requested user by id : {id} is not found")
    return user
