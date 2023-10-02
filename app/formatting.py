# These File is responsable for validating request and response
from datetime import datetime
from pydantic import BaseModel  # formatting Request and Response


class PostBase(BaseModel):  # Post schema for valdating post and It's Base Class
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):  # Format for Response of a Single Post
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
