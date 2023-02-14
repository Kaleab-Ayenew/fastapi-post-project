from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from .. import models
from .. import oauth2

router = APIRouter(
    prefix="/votes",
    tags=["Like"]
)


@router.post("/")
def vote(payload: schemas.VoteRequest, db: Session = Depends(get_db), token_user_data: schemas.TokenData = Depends(oauth2.get_current_user)):
    user_id = token_user_data.user_id
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == payload.post_id, models.Votes.user_id == user_id)
    vote = vote_query.first()
    if vote:
        vote_query.delete()
        db.commit()
        return {"message": "Vote removed succesfully", "vote": vote}
    else:
        new_vote = models.Votes(post_id=payload.post_id,
                                user_id=user_id)
        db.add(new_vote)
        db.commit()
        return {"message": "New vote added succesfully", "vote": new_vote}
