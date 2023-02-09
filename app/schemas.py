from pydantic import BaseModel, EmailStr
from datetime import datetime


class Post(BaseModel):  # Pydantic Data Model
    title: str
    content: str
    draft: bool = False

# We can create different Models for different requests based on the kind of Data we expect from each request


class PostResponse(BaseModel):
    title: str
    content: str
    draft: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
