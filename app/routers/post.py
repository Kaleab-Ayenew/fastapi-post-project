from typing import List
from ..schemas import Post, PostResponse
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

from ..database import get_db
from .. import models


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


""" Retrive all of the posts """


@router.get("/", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


""" Retrive a single post from the database """


@router.get("/{id}", response_model=PostResponse)
def get_single_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist!")
    return post


"""--- Create a new post ---"""


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(payload: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


"""--- Delete an existing post ---"""


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=PostResponse)
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
