from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # Main application instance

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")  # Index Endpoint
def index(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
