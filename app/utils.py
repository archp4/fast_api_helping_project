from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto")  # bcrypt object


def hash(text: str):
    return pwd_context.hash(text)  # hashing password


def verify(plain_password: str, hash_password: str):
    # checking password is correct or not
    return pwd_context.verify(plain_password, hash=hash_password)
