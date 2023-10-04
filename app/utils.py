from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto")  # bcrypt object


def hash(text: str):
    return pwd_context.hash(text)  # hashing password
