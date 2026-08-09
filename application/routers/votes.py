from fastapi import status, HTTPException, Depends,APIRouter, Response
from .. import schemas, oauth2, database, models
from sqlalchemy.orm import Session

router = APIRouter(
    # prefix = "/votes",
    tags = ['votes']
)

@router.post("/votes", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.vote, db : Session = Depends(database.get_db), current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post_query is None:
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    vote_query = db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.posts_id == vote.post_id)
    if(vote.dir == 1):    #user is trying to like
        if vote_query.first() is None:
            like_query = models.Votes(user_id = current_user.id, posts_id = vote.post_id )
            db.add(like_query)
            db.commit()
            db.refresh(like_query)
            raise HTTPException(detail=f"you have liked the post with id : {vote.post_id}")
        else:
            raise HTTPException(detail=f"you have already liked the post with id : {vote.post_id}")
    else:
        if vote_query.first() is None:
            raise HTTPException(detail=f"you have already unliked the post with id : {vote.post_id}")
        else:
            vote_query.delete()
            db.commit()
            raise HTTPException(detail=f"you have unliked the post with id : {vote.post_id}")