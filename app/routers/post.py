from typing import List
from ..schemas import Post, PostResponse, TokenSchema
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

from ..database import get_db
from .. import models
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


""" Retrive all of the posts """


@router.get("/", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db), limit: int = 5, skip: int = 0, search: str | None = ""):
    # posts = db.query(models.Post).all()
    # posts = db.query(models.Post).limit(limit).all()
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
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
def create_post(payload: Post, db: Session = Depends(get_db), token_user_data: dict = Depends(oauth2.get_current_user)):
    new_post = models.Post(
        **payload.dict(), owner=token_user_data.user_id)
    print(token_user_data, "This is what you stored in the token")
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


"""--- Delete an existing post ---"""


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), token_user_data: dict = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist")
    if post.owner != token_user_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to perform this action.")
    post_query.delete(synchronize_session=False)
    db.commit()
    return None


"""--- Update an existing post ---"""


@router.put("/{id}", response_model=PostResponse)
def update(id: int, payload: Post, db: Session = Depends(get_db), token_user_data: dict = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This post doesn't exist!")
    if post.owner != token_user_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to perform this action.")
    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
