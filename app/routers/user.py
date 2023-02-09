from typing import List
from ..schemas import UserCreate, UserResponse
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

from ..database import get_db
from .. import models

from ..utils import hash


router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    hashed_pass = hash(payload.password)
    payload.password = hashed_pass
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{id}", response_model=UserResponse)
def get_single_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="This user doesn't exist.")
    return user
