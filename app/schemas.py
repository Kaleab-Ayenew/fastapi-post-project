from pydantic import BaseModel, EmailStr
from datetime import datetime


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


class Post(BaseModel):  # Pydantic Data Model
    title: str
    content: str
    draft: bool = False

# We can create different Models for different requests based on the kind of Data we expect from each request


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    draft: bool
    owner: int
    created_at: datetime
    owner_info: UserResponse

    class Config:
        orm_mode = True


class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    auth_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    email: EmailStr


class VoteRequest(BaseModel):
    post_id: int
