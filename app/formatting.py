# These File is responsable for validating request and response
from datetime import datetime
from pydantic import BaseModel, EmailStr  # formatting Request and Response


class PostBase(BaseModel):  # Post schema for valdating post and It's Base Class
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):  # Format for Response of a Single Post
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class UserRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenModel(BaseModel):
    user_id: int
