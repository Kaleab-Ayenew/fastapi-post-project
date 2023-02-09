from ..schemas import UserLogin
from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException, Depends, APIRouter

from ..database import get_db
from .. import models
from .. import utils

from .. import oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please provide valid credentials.")
    if not utils.verify(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Please provide valid credentials.")
    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "email": user.email})
    return {"token_type": "bearer", "auth_token": access_token}
