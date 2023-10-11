from jose import JWTError, jwt
from datetime import datetime, timedelta


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
