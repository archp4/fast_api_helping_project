from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import formatting, models, database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# IGN in MD5
SECRET_KEY = "b08ada4fb66a9108dbc585e044b03fb1"
# Algorithm
ALGORITHM = "HS256"
# Expriation time
TOKEN_EXPIRED_TIME = 30


def create_access_token(payload: dict):
    # creating copy of payload
    to_encode = payload.copy()
    # creating expire time for token
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRED_TIME)
    # creating adding expire time in payload
    to_encode.update({"exp": expire})
    # creating token
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # returning token
    return token


def verfiy_access_token(token: str, exception):
    try:
        # decoding token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # taking user id for decoded_token
        user_id: int = decoded_token.get('user_id')
        if user_id is None:  # if token does not id throw error
            raise exception
        token_data = formatting.TokenModel(user_id=user_id)
    except JWTError as e:
        print(e)  # if token problem while decode token error will raise
        raise exception
    # returning token_payload / data if everything is ok
    return token_data


def get_cuurent_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(database.getDB)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validae credentials", headers={"WWW-Authenticate": "Bearer"})
    # verify user token and get user id
    access_token = verfiy_access_token(token, credentials_exception)
    # getting user by id
    user = db.query(models.User).filter(
        models.User.id == access_token.user_id).first()
    # returning user
    return user
