
from fastapi import status, HTTPException, Depends, APIRouter
# ORM Files
from .. import models, formatting, utils
from ..database import getDB
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['Authentication']  # Grouping
)


@router.post("/login")
def get_user_by_id(user_credentials: formatting.UserLogin, db: Session = Depends(getDB)):
    # find user by email
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()
    # Checking User exist or not
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    # Checking password is valid or not
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    # Creating Token

    # Sending Token to user
    return {"token": "Example token"}
