from ..schemas import UserLogin, TokenSchema
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from .. import models
from .. import utils

from .. import oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=TokenSchema)
# def login_user(payload: UserLogin, db: Session = Depends(get_db)):
def login_user(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please provide valid credentials. Email")
    if not utils.verify(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please provide valid credentials. Password")
    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "email": user.email})
    return {"token_type": "bearer", "auth_token": access_token}
