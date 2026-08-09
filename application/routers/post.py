from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
     prefix = "/posts",
     tags = ['post'] #in the swagger docs aall these functions will be under post tag
)

@router.get("/mypost/mypost")
def get_own_post(current_user = Depends(oauth2.get_current_user), db : Session=Depends(get_db)):
    res = (db.query(models.Post, func.count(models.Votes.post_id))
    .join(models.Votes, models.Post.id==models.Votes.post_id, isouter=True)
    .filter(models.Post.owner_id==current_user.id).group_by(models.Post.id).all())
    return res

@router.get("/", response_model = List[schemas.PostByUserId2])  #without list it will only return one dic, so we need to use list
def get_post(db : Session = Depends(get_db),  current_user : int = Depends(oauth2.get_current_user), limit : int = 10,
            search : Optional[str] = ""):
    # res = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    res=(db.query(models.Post, func.count(models.Votes.posts_id)).join(models.Votes, models.Votes.posts_id==models.Post.id,isouter=True)
    .filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).all())

    posts = []
    for r in res:
        post_obj, count = r
        data = schemas.PostByUserId.model_validate(post_obj).model_dump()
        data["count"] = count
        posts.append(data)
    return posts

@router.get("/{username}", response_model = List[schemas.PostByUserId2])
def get_posts_by_username(username : str, db : Session = Depends(get_db),  current_user = Depends(oauth2.get_current_user)):  # converts the id coming as string in the url to int
        owner = db.query(models.Users).filter(models.Users.username == username).first()
        if owner == None:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"no owner, named : {username}"  #detail amd status_code is inbuilt
            )
        owner_id = owner.id
        post = (db.query(models.Post, func.count(models.Votes.posts_id)).join(models.Votes, models.Post.id==models.Votes.posts_id)
        .filter(models.Post.owner_id==owner.id).group_by(models.Post.id).all())
        if not post: #.all() in query returns empty list if not found
            raise HTTPException(
                            status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"no owner, named : {username}"  #detail amd status_code is inbuilt
            )
        posts = []
        for p in post:
            post_obj, count = p
            data = schemas.PostByUserId.model_validate(post_obj).model_dump()
            data["count"] = count
            posts.append(data)
        return posts

 
@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.Post)
def create_post(post : schemas.CreateSchema,db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) #we are passing owner_id directly 
    #insertion gets passed to constructor that builds the table, thats why we need to decrypt it before passing to the class to create table
    db.add(new_post)
    db.commit()
    db.refresh(new_post)   #model object thats why refresh works
    return  new_post
    

@router.delete("/{id}")
def delete_post(id : int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id) #here post is query object look line  61

    if post.first() == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id : {id} not found"
        )
    if post.first().owner_id == current_user.id:
        post.delete()
        db.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)
        #response doesnt have detail 
        
    raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = f"why are you trying to delete others post?"
        )

@router.put("/{id}", response_model = schemas.Post)
def update_post(id : int, post : schemas.CreateSchema, db : Session = Depends(get_db),  current_user : int = Depends(oauth2.get_current_user)):
    res = db.query(models.Post).filter(models.Post.id == id) #it doesnt update it just returns matched rows

    if(res.first() == None):
    
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"post with id : {id} does not exist"
        )
    
    if res.first().owner_id != current_user.id:
        raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = f"cant update others post"
        )
 
    res.update(post.model_dump()) 
        #"Take the rows matched by the db.query and update them."
        #insertion gets passed to constructor thats why we need to decrypt it
        #but update directly gets to sqlalchemy and it only works with dictionary
    db.commit()
        #res is a query object, res2 is a model object
    return res.first()
