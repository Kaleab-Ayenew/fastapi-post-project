from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from . import models
from .database import engine, SessionLocal, get_db

from .schemas import Post, PostResponse, UserCreate, UserResponse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # Main application instance

hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/")  # Index Endpoint
def index(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# *** API endpoints ***


""" Retrive all of the posts """


@app.get("/posts", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


""" Retrive a single post from the database """


@app.get("/posts/{id}", response_model=PostResponse)
def get_single_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist!")
    return post


"""--- Create a new post ---"""


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(payload: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


"""--- Delete an existing post ---"""


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return None


"""--- Update an existing post ---"""


@app.put("/posts/{id}", response_model=PostResponse)
def update(id: int, payload: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist!")
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post


@app.post("/users", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    hashed_pass = hasher.hash(payload.password)
    payload.password = hashed_pass
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
