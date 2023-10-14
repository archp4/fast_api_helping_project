
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# ORM Files
from .. import models, formatting, utils, oauth2
from ..database import getDB
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['Authentication']  # Grouping
)


@router.post("/login", response_model=formatting.Token)
def get_user_by_id(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getDB)):
    # find user by email
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    # Checking User exist or not
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    # Checking password is valid or not
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    # Creating Token
    token = oauth2.create_access_token(payload={'user_id': user.id})
    # Sending Token to user
    return {"access_token": token, "token_type": "bearer"}
