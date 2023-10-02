# These File is responsable for validating request and response
from typing import Optional
from pydantic import BaseModel  # formatting Request and Response


class PostBase(BaseModel):  # post schema for valdating post
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass
