from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database
from sqlalchemy.orm import Session

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, ):
    data_to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})

    # The token is created here.
    jwt_token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_token(token: str, error_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str | None = payload.get("user_id")
        email: str | None = payload.get("email")
        if id is None:
            raise error_exception

        token_data = schemas.TokenData(user_id=id, email=email)
    except JWTError:
        raise error_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    error_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide valid credentials.", headers={
            "WWW-Authenticate": "Bearer"
        })
    return verify_token(token, error_exception)
