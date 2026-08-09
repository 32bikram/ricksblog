from fastapi import status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    tags= ['user']
)

@router.post("/createuser", status_code = status.HTTP_201_CREATED, response_model = schemas.ReturnUser)
def createUser(user : schemas.GetUser, db : Session = Depends(get_db)): #getuser = pydanticschema
    existing_user = db.query(models.Users).filter((models.Users.email == user.email) | (models.Users.username == user.username)).first()
    if existing_user is not None:
        raise HTTPException(
            status_code = status.HTTP_208_ALREADY_REPORTED 
        )
    user.password = utils.hash(user.password)
    res = models.Users(**user.model_dump())  #users = actual schema or table
    db.add(res)
    db.commit()
    db.refresh(res)
    return res


@router.get("/getuser/{id}", response_model = schemas.ReturnUser)
def getUser(id : int, db : Session = Depends(get_db)):
    res = db.query(models.Users).filter(models.Users.id == id).first()
    if res is None:
         raise HTTPException(
          status_code = status.HTTP_404_NOT_FOUND   
         )
    return res